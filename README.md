# cermak.science

This repository contains the static files served by the website.

## Teaching websites

Automation in Physics now lives at <https://automation.cermak.science/>. Only a
redirect remains in `teaching/automation/index.html`; `404.html` redirects old
lesson and other URLs under `/teaching/automation/` to the new homepage as well.
These are browser redirects because this repository is served as a static site.
Programming course materials remain in `teaching/p1m/`.

## Updating publications

Export a **Web of Science Researcher CV as JSON**, then run from this directory
(Python 3.10 or newer, no extra packages):

```powershell
python scripts/import_publications.py "PetrČermák_Web_of_Science_Researcher_CV_20261027.json"
```

The script merges publications by DOI into `assets/data/publications.json` and
updates `publications.html`. Older entries remain even when the export covers
only a limited period. Repeating the import does not create duplicates. Existing
formula markup and more precise publication dates are preserved. Records without
a DOI and the separate preprint list are not imported.

Commit and publish both changed files with the rest of the static website.
Uploading a WoS export alone does not update the website.

The original site was generated on
[MFF GitLab](https://gitlab.mff.cuni.cz/cermp5am/cermak.science), with a Publons API
import during each build. There is no such build/import job in this repository.
[Publons now marks its GET API endpoints as deprecated](https://publons.com/wos-op/api/v2/).
If the old GitLab build is used again, port these publication changes to its source
templates first so that it does not overwrite this page.
