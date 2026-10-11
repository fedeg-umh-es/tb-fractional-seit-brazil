"""Build BibTeX entries for the new references from Crossref metadata (verified 2026-10-11).

Only references that are cited in manuscript.tex are listed here (plan: no padding).
Run: python manuscript_latex/tools/build_bib_additions.py > manuscript_latex/tools/bib_additions.bib
"""
import html
import json
import re
import time
import urllib.parse
import urllib.request

REFS = {  # bibtex key: DOI (lookups return the metadata that is written; nothing is typed by hand)
    "tashman2000": "10.1016/s0169-2070(00)00065-0",
    "hyndman2006": "10.1016/j.ijforecast.2006.03.001",
    "petropoulos2022": "10.1016/j.ijforecast.2021.11.001",
    "funk2019": "10.1371/journal.pcbi.1006785",
    "reich2019": "10.1073/pnas.1812594116",
    "cramer2022": "10.1073/pnas.2113561119",
    "diebold1995": "10.1080/07350015.1995.10524599",
    "harvey1997": "10.1016/s0169-2070(96)00719-4",
    "raue2009": "10.1093/bioinformatics/btp358",
    "wieland2021": "10.1016/j.coisb.2021.03.005",
    "chowell2017": "10.1016/j.idm.2017.08.001",
    "vandendriessche2002": "10.1016/s0025-5564(02)00108-6",
    "storn1997": "10.1023/a:1008202821328",
}
MAX_AUTHORS = 10


def tex(s):
    s = html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
    s = re.sub(r"\s+", " ", s)
    return s.replace("&", r"\&")


def fetch(doi):
    for i in range(4):
        try:
            return json.load(urllib.request.urlopen("https://api.crossref.org/works/" + urllib.parse.quote(doi), timeout=30))["message"]
        except Exception:
            time.sleep(3 * (i + 1))
    raise SystemExit(f"Crossref lookup failed for {doi}")


for key, doi in REFS.items():
    m = fetch(doi)
    au = [a for a in m.get("author", []) if "family" in a]
    names = [f"{a['family']}, {a.get('given', '')}".strip().rstrip(",") for a in au]
    author = " and ".join(names) if len(names) <= MAX_AUTHORS else " and ".join(names[:1]) + " and others"
    fields = {"author": author, "title": "{" + tex(m["title"][0]) + "}", "journal": tex(m["container-title"][0]),
              "year": str(m["issued"]["date-parts"][0][0])}
    if m.get("volume"):
        fields["volume"] = m["volume"]
    if m.get("page"):
        fields["pages"] = m["page"].replace("-", "--")
    fields["doi"] = m["DOI"]
    note = ""
    if key == "cramer2022":
        note = "% NOTE: Crossref lists a 2023 correction notice (10.1073/pnas.2304076120); its content was not read. Record has no page or article number.\n"
    if key == "petropoulos2022" or key == "cramer2022" or key == "reich2019":
        note += f"% Author list truncated to the first author with 'and others' ({len(names)} authors in Crossref).\n" if len(names) > MAX_AUTHORS else ""
    print(note + f"@article{{{key},")
    print(",\n".join(f"  {k}={{{v}}}" for k, v in fields.items()))
    print("}\n")
    time.sleep(0.5)
