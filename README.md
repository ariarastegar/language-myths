# Language myths, answered

**[language-myths.github.io](https://language-myths.github.io)**

People ask the same questions about language again and again: whether Latin is dead, whether some languages are primitive, whether texting is ruining how young people write. This project answers those myths with academic research. Each myth gets a short answer that sums up what the studies find, a longer explanation, and the evidence itself, grouped by whether it supports the answer, complicates it, or contradicts it.

The myths change rarely. The evidence keeps growing, and anyone can add to it.

## Contributing

You don't need to know anything about GitHub code to help.

- **Add evidence to a myth.** Open a myth on the site and choose *Add evidence*, or go to *Issues → New issue → Add evidence*. Studies that complicate an answer are as welcome as ones that support it.
- **Propose a new myth.** Use *Issues → New issue → Propose a myth*, and include at least one academic study whose findings answer it.
- **Check a source.** Entries marked "Not yet checked" were added from abstracts or summaries. If you can read the original, open an issue saying whether it confirms the summary.
- **Discuss.** To question an answer or a source, open an issue whose title starts with the myth's ID in brackets, for example `[latin-died]`.

Every submission is reviewed by a maintainer before it appears on the site. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## What gets published

A myth appears on the site only when at least one academic study (a peer-reviewed article or a scholarly book) answers it, and its short answer summarizes what that research finds. Myths still waiting for such a study are kept in [`_archive/`](_archive/) until one is contributed.

## How the content is organized

```
_myths/       one file per myth: the claim, a short answer, and a longer explanation
_evidence/    one file per source, each pointing at a myth
_archive/     myths waiting for a supporting study
data.json     bundles the myths and evidence for the site (don't edit by hand)
index.html    the site itself
```

A myth file:

```yaml
---
claim: "Latin is a dead language."
one_liner: "Latin is still spoken. These days it's called French, Spanish, Italian…"
topic: "History & change"
order: 3
---

The longer explanation in Markdown, with optional "## Caveats" and "## Examples" sections.
```

An evidence file:

```yaml
---
myth: latin-died                    # the myth's file name, without .md
stance: supports                    # supports, complicates or counterexample
type: "Study"                       # Study, Primary text, Data or corpus, Reference work, News or popular writing
citation: "Author, A. (Year). Title. *Journal* 1(2): 3–4."
title: "Title"                      # optional: the exact title, used for the Google Scholar button
link: "https://doi.org/…"           # publisher page or DOI
languages: ["Old French"]
contributor: "github-username"
checked: false                      # true once someone has read the original source
added: 2026-11-21
---

One to three sentences on what it shows.
```

## For maintainers

**Reviewing a submission**

1. Read the issue and discuss it with the contributor if needed.
2. To accept it, add the `accepted` label. A bot turns it into a file and opens a pull request.
3. Check the pull request, edit the file there if needed, and merge it. The site updates within a couple of minutes and the issue closes.
4. To reject a submission, close the issue with a short note.

When you accept a new myth, add its supporting study as an evidence file too.

**Editing directly**

Edit or add files in `_myths/` and `_evidence/`, then commit and push. Pull first, since accepted submissions arrive on GitHub, not on your computer. If you add or archive a myth by hand, update the list in the evidence form:

```
KIND=refresh-form python3 .github/scripts/issue_to_file.py
```

**Bringing back an archived myth**

See [`_archive/README.md`](_archive/README.md).

## Licence

The content of this project (the myths, short answers, explanations and evidence summaries) is shared under the [Creative Commons Attribution 4.0 International licence (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). You may share and adapt it for any purpose, as long as you credit "Language myths, answered" and link to [language-myths.github.io](https://language-myths.github.io).

The studies and other works cited remain the property of their authors and publishers; the licence covers only this project's own text.
