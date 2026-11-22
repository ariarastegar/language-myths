# Language myths, answered

Short answers to common misconceptions about language, with the evidence behind them. The myths stay fairly stable; the evidence grows as scholars and readers add studies, primary texts and counterexamples.

The site runs on GitHub Pages. There's no build step on your computer: GitHub turns the files in this repository into the website every time something changes.

## How the content is organized

```
_myths/       one file per myth: the claim, a one-line answer, and a longer explanation
_evidence/    one file per piece of evidence, each pointing at a myth
data.json     bundles both folders into one file for the website (don't edit by hand)
index.html    the website itself
```

A myth file looks like this:

```yaml
---
claim: "Latin is a dead language."
one_liner: "Latin is still spoken. These days it's called French, Spanish, Italian…"
topic: "History & change"
order: 3
---

The longer explanation in Markdown, with optional "## Caveats" and "## Examples" sections.
```

An evidence file looks like this:

```yaml
---
myth: latin-died                    # the myth's file name, without .md
stance: supports                    # supports, complicates or counterexample
type: "Primary text"                # Study, Primary text, Data or corpus, Reference work, News or popular writing
citation: "Ayres-Bennett, W. (1996). The Strasbourg Oaths, 842. In *A History of the French Language through Texts*."
link: "https://…"
languages: ["Old French"]
contributor: "github-username"
checked: false                      # true once someone has read the original source
added: 2026-11-21
---

One to three sentences on what it shows.
```

## What gets published

A myth appears on the site only when at least one academic study (a peer-reviewed article or a scholarly book) answers it, and its short answer summarizes what that research finds. Myths without such a study wait in `_archive/` until one is contributed; see `_archive/README.md` for how to bring one back.

## First-time setup with GitHub Desktop

1. **Set your repository name.** Open `_config.yml` in a text editor and change `YOUR-USERNAME/language-myths` to your GitHub username and the repository name you'll use.
2. **Create the repository.** In GitHub Desktop choose *File → Add Local Repository…*, pick this folder, and click *create a repository* when it says the folder isn't one yet. Keep the name, then click *Create Repository*.
3. **Publish it.** Click *Publish repository*. Untick *Keep this code private* (GitHub Pages needs a public repository on free accounts), then click *Publish Repository*.
4. **Turn on the website.** On github.com, open the repository and go to *Settings → Pages*. Under *Build and deployment*, choose *Deploy from a branch*, select `main` and `/ (root)`, and save. After a minute or two the site is live at `https://YOUR-USERNAME.github.io/language-myths/`.
5. **Let the review automation work.** In *Settings → Actions → General → Workflow permissions*, choose *Read and write permissions* and tick *Allow GitHub Actions to create and approve pull requests*. Save.
6. **Create three labels.** In *Issues → Labels*, create `evidence`, `new myth` and `accepted`.

## Reviewing contributions

1. Someone fills in *Add evidence* or *Propose a myth* on the site. This opens an issue with the right label.
2. Read it, and discuss it in the issue if needed.
3. To accept it, add the `accepted` label. An automatic step turns it into a file and opens a pull request.
4. Check the pull request, edit the file there if needed, and merge it. The site updates a minute or two later, and the issue closes.

To reject a submission, close the issue with a short note.

## Editing directly

You can also edit files yourself: change or add files in `_myths/` and `_evidence/`, then *Commit* and *Push* in GitHub Desktop. Always *Fetch / Pull* first, since accepted submissions arrive on GitHub, not on your computer.

If you add a myth by hand, update the list of myths in the evidence form by running:

```
KIND=refresh-form python3 .github/scripts/issue_to_file.py
```

(Myths accepted through the form update that list automatically.)

## Previewing on your computer

`index.html` won't show any myths if you just open it, because GitHub builds `data.json` when it publishes. Check changes on the live site after pushing.

## Licence

Add a licence before inviting contributors, so they know how their work can be reused. CC BY 4.0 is common for scholarly reference material: add a `LICENSE` file with its text.
