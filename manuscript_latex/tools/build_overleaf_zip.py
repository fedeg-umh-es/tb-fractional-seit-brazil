"""Build the Overleaf upload package (no compilation). Run from the repository root:
    python manuscript_latex/tools/build_overleaf_zip.py
Layout at the zip root: manuscript.tex, references.bib, sn-jnl.cls, sn-mathphys-ay.bst, figures/, tables/, README_OVERLEAF.txt
"""
import hashlib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "TB_SEIT_BMB_overleaf_2026-10-11.zip"
files = ["manuscript.tex", "references.bib", "sn-jnl.cls", "sn-mathphys-ay.bst"]
files += sorted(f"figures/{p.name}" for p in (ROOT / "figures").glob("*.pdf"))
files += sorted(f"tables/{p.name}" for p in (ROOT / "tables").glob("*.tex"))
readme = """TB-SEIT manuscript for Overleaf (author-review draft, not submission ready)

1. Upload this zip as a new Overleaf project.
2. Main document: manuscript.tex. Compiler: pdfLaTeX. Bibliography: BibTeX (the project must run
   pdflatex, bibtex, pdflatex, pdflatex; Overleaf does this automatically).
3. sn-mathphys-ay.bst is the Springer style with ONE local change (see the comment at the top of the file):
   it makes the reference list sort by surname (the stock file listed Kharazmi before Kalizhanova).
4. Placeholders left on purpose: [ZENODO_DOI] and [RELEASE_TAG] (Code and Data Availability).
5. LaTeX comments starting with "AUTHOR-ACTION" mark text that depends on a decision of the authors.
6. This package was assembled without compiling it. Please check the compile log for warnings,
   especially: overfull boxes in the tables, the appendix tables, and the reference order.
"""
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for f in files:
        assert (ROOT / f).exists(), f
        zi = zipfile.ZipInfo(f, date_time=(2026, 10, 11, 0, 0, 0))
        zi.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(zi, (ROOT / f).read_bytes())
    zi = zipfile.ZipInfo("README_OVERLEAF.txt", date_time=(2026, 10, 11, 0, 0, 0))
    z.writestr(zi, readme)
print(OUT.name, OUT.stat().st_size, "bytes;", len(files) + 1, "files; sha256", hashlib.sha256(OUT.read_bytes()).hexdigest())
