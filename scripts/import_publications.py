"""Merge a Web of Science CV export and rebuild the static publications page."""

import argparse
import html
import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data" / "publications.json"
PAGE = ROOT / "publications.html"
START = "          <!-- publications:start -->"
END = "          <!-- publications:end -->"
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def publication_date(value):
    """Keep the month/year precision supplied by WoS; never invent a day."""
    if re.fullmatch(r"\d{4}(?:-\d{2})?(?:-\d{2})?", value):
        date.fromisoformat((value + "-01-01")[:10])
        return value
    month, year = value.split()
    return publication_date(f"{int(year):04d}-{MONTHS.index(month) + 1:02d}")


def render(publications):
    rows = []
    for number, item in zip(range(len(publications), 0, -1), publications):
        doi = html.escape(item["doi"], quote=True)
        journal = html.escape(item["journal"])
        published = html.escape(item["date"])
        rows.append(f'''          <div class="c-article-compact__item">
            <div class="c-article-compact__body">
              <div>
                <h2>{number}.</h2>
              </div>
              <div>
                <h3 class="c-article-compact__header">{item["title_html"]}</h3>
                <div class="c-article-compact__cell">
                  <div class="c-article-compact__cite">{journal} ({published})</div>
                  <div class="c-article-compact__doi"><a href="https://doi.org/{doi}" class="c-button c-button--simple-text">doi:{doi}</a><i class="icofont icofont-external-link"></i></div>
                </div>
              </div>
            </div>
          </div>''')
    return "\n".join(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", type=Path, help="Web of Science Researcher CV JSON export")
    args = parser.parse_args()
    export = json.loads(args.export.read_text(encoding="utf-8-sig"))
    if export["author"]["orcid"] != "0000-0002-4176-6905":
        raise ValueError("The export belongs to a different ORCID profile")
    data = json.loads(DATA.read_text(encoding="utf-8"))
    publications = {item["doi"].casefold(): item for item in data["publications"]}
    added = skipped = 0
    for record in export["records"]["publication"]["list"]:
        doi = (record.get("doi") or "").strip()
        if not doi:
            skipped += 1
            continue
        published = publication_date(record["publication_date"].strip())
        key = doi.casefold()
        if key not in publications:
            publications[key] = {
                "doi": doi,
                "title_html": html.escape(record["title"]),
                "journal": record.get("journal") or "",
                "date": published,
            }
            added += 1
        else:
            item = publications[key]
            if record.get("journal"):
                item["journal"] = record["journal"]
            # Preserve curated formula markup and more precise existing dates.
            if len(published) >= len(item["date"]):
                item["date"] = published

    data["publications"] = sorted(
        publications.values(), key=lambda item: (item["date"], item["doi"]), reverse=True
    )
    data["last_export"] = export["date_generated"]
    page = PAGE.read_text(encoding="utf-8")
    if page.count(START) != 1 or page.count(END) != 1:
        raise ValueError("Expected exactly one pair of publication markers")
    before, rest = page.split(START)
    _, after = rest.split(END)
    generated = START + "\n" + render(data["publications"]) + "\n" + END
    updated = before + generated + after
    updated, count = re.subn(
        r'(<span id="publications-updated">)[^<]*(</span>)',
        lambda match: match[1] + html.escape(data["last_export"]) + match[2],
        updated,
    )
    if count != 1:
        raise ValueError("Expected exactly one publication update date")
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PAGE.write_text(updated, encoding="utf-8")
    print(f"Added {added}; skipped {skipped} without DOI; total {len(publications)} publications.")


if __name__ == "__main__":
    main()
