"""Turn an accepted issue-form submission into a myth or evidence file.

Run by .github/workflows/accept.yml. Reads the issue from environment variables:
  KIND          "evidence" or "myth"
  ISSUE_BODY    the issue text GitHub's form produced
  ISSUE_NUMBER  the issue number
  ISSUE_AUTHOR  the GitHub username of whoever opened it
Writes the new file, and for a new myth also adds it to the evidence form's list.
Prints a pull request title to $GITHUB_OUTPUT as "title".
"""
import datetime
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MYTHS = ROOT / "_myths"
EVIDENCE = ROOT / "_evidence"
FORM = ROOT / ".github" / "ISSUE_TEMPLATE" / "evidence.yml"

EVIDENCE_FIELDS = {
    "Which myth is this about?": "myth",
    "What does it do to the answer?": "stance",
    "Type of evidence": "type",
    "Citation": "citation",
    "Link or DOI": "url",
    "Languages it concerns": "languages",
    "What it shows": "summary",
    "Source check": "checked",
}
MYTH_FIELDS = {
    "The myth, as people say it": "claim",
    "Short answer": "one_liner",
    "Topic": "topic",
    "Longer explanation": "explanation",
    "Short ID (optional)": "slug",
}
STANCES = {"Supports the answer": "supports", "Complicates it": "complicates", "Counterexample": "counterexample"}


def fail(msg):
    print(f"::error::{msg}")
    sys.exit(1)


def parse(body, fields):
    """Issue forms render as '### Label' followed by the answer."""
    out = {}
    parts = re.split(r"^### (.+?)\s*$", body.replace("\r\n", "\n"), flags=re.M)
    for label, value in zip(parts[1::2], parts[2::2]):
        key = fields.get(label.strip())
        if key:
            value = value.strip()
            out[key] = "" if value == "_No response_" else value
    return out


def slugify(text, limit=6):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    words = re.findall(r"[a-z0-9]+", text.lower())
    return "-".join(words[:limit]) or "item"


def q(value):
    return json.dumps(value, ensure_ascii=False)


def myth_ids():
    return sorted(p.stem for p in MYTHS.glob("*.md"))


def refresh_form():
    """Rewrite the myth list in the evidence form from the files in _myths."""
    lines = []
    for path in sorted(MYTHS.glob("*.md")):
        m = re.search(r'^claim:\s*(.+)$', path.read_text(), re.M)
        claim = json.loads(m.group(1)) if m and m.group(1).startswith('"') else (m.group(1) if m else path.stem)
        if len(claim) > 90:
            claim = claim[:87].rstrip() + "…"
        lines.append(f"        - {q(path.stem + ' · ' + claim)}")
    text = FORM.read_text()
    new = re.sub(
        r"(# MYTHS-START[^\n]*\n).*?(\n\s*# MYTHS-END)",
        lambda m: m.group(1) + "\n".join(lines) + m.group(2),
        text, flags=re.S,
    )
    FORM.write_text(new)


def evidence(body, number, author):
    f = parse(body, EVIDENCE_FIELDS)
    myth = (f.get("myth") or "").split(" · ")[0].strip()
    if myth not in myth_ids():
        fail(f"Unknown myth '{myth}'.")
    stance = STANCES.get(f.get("stance", ""))
    if not stance:
        fail("Missing or unknown stance.")
    if not f.get("citation") or not f.get("summary"):
        fail("Citation and summary are required.")
    first_author = slugify(f["citation"], 1)
    year = re.search(r"\b(1[5-9]\d\d|20\d\d)\b", f["citation"])
    name = f"{myth}--{first_author}-{year.group(1) if year else 'nd'}-{number}"
    langs = [x.strip() for x in (f.get("languages") or "").split(",") if x.strip()]
    checked = bool(re.search(r"^- \[[xX]\]", f.get("checked", ""), re.M))
    front = [
        "---",
        f"myth: {myth}",
        f"stance: {stance}",
        f"type: {q(f.get('type') or 'Study')}",
        f"citation: {q(f['citation'])}",
        f"link: {q(f.get('url', ''))}",
        f"languages: {q(langs)}",
        f"contributor: {q(author)}",
        f"checked: {'true' if checked else 'false'}",
        f"added: {datetime.date.today().isoformat()}",
        f"issue: {number}",
        "---",
    ]
    (EVIDENCE / f"{name}.md").write_text("\n".join(front) + "\n\n" + f["summary"].strip() + "\n")
    return f"Add evidence to '{myth}' (#{number})"


def myth(body, number, author):
    f = parse(body, MYTH_FIELDS)
    for k in ("claim", "one_liner", "topic", "explanation"):
        if not f.get(k):
            fail(f"Missing field: {k}")
    slug = slugify(f.get("slug") or f["claim"])
    base, n = slug, 2
    while (MYTHS / f"{slug}.md").exists():
        slug, n = f"{base}-{n}", n + 1
    orders = [int(m.group(1)) for p in MYTHS.glob("*.md") for m in [re.search(r"^order:\s*(\d+)", p.read_text(), re.M)] if m]
    front = [
        "---",
        f"claim: {q(f['claim'])}",
        f"one_liner: {q(f['one_liner'])}",
        f"topic: {q(f['topic'])}",
        f"order: {max(orders, default=0) + 1}",
        f"proposed_by: {q(author)}",
        f"issue: {number}",
        "---",
    ]
    (MYTHS / f"{slug}.md").write_text("\n".join(front) + "\n\n" + f["explanation"].strip() + "\n")
    refresh_form()
    return f"Add myth '{slug}' (#{number})"


def main():
    kind = os.environ.get("KIND", "")
    if kind == "refresh-form":
        refresh_form()
        return
    body = os.environ["ISSUE_BODY"]
    number = int(os.environ["ISSUE_NUMBER"])
    author = os.environ.get("ISSUE_AUTHOR", "")
    title = evidence(body, number, author) if kind == "evidence" else myth(body, number, author)
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as fh:
            fh.write(f"title={title}\n")
    print(title)


if __name__ == "__main__":
    main()
