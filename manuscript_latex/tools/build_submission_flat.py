"""Build a flat, self-contained LaTeX package for the Springer Nature submission system.

Run from the repository root (needs pdflatex and bibtex):
    python manuscript_latex/tools/build_submission_flat.py

Differences from the Overleaf package (same text, tables, figures and references):
- one .tex file: the tables in tables/ are inlined and the bibliography is embedded
  (the .bbl produced by bibtex with sn-mathphys-ay.bst), so no .bib, .bst or \\input is needed;
- figures at the root, no subfolders;
- preamble reduced to the packages of the Springer template; hyperref and line numbers come
  from sn-jnl itself (class option "lineno"); no inputenc/fontenc/url/lineno packages;
- authoring comments removed; unique hyperref anchors for the appendix tables.
Output: manuscript_latex/submission_flat/ and TB_SEIT_BMB_submission_flat_2026-10-12.zip
"""
import hashlib
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "submission_flat"
OUTZIP = ROOT / "TB_SEIT_BMB_submission_flat_2026-10-12.zip"

PREAMBLE = r"""\documentclass[pdflatex,sn-mathphys-ay,lineno]{sn-jnl}
\usepackage{graphicx}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{booktabs}
\raggedbottom
\begin{document}
"""
ASCII = {"ü": r"{\"u}", "ö": r"{\"o}", "–": "--", "—": "---", "é": r"{\'e}", "á": r"{\'a}", "í": r"{\'i}"}


def run(cmd, cwd):
    subprocess.run(cmd, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)


def make_bbl():
    """Run the original project once to obtain the .bbl."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for name in ["manuscript.tex", "references.bib", "sn-jnl.cls", "sn-mathphys-ay.bst"]:
            shutil.copy(ROOT / name, tmp / name)
        shutil.copytree(ROOT / "figures", tmp / "figures")
        shutil.copytree(ROOT / "tables", tmp / "tables")
        run(["pdflatex", "-interaction=nonstopmode", "manuscript.tex"], tmp)
        run(["bibtex", "manuscript"], tmp)
        bbl = (tmp / "manuscript.bbl").read_text()
    for k, v in ASCII.items():
        bbl = bbl.replace(k, v)
    assert all(ord(c) < 128 for c in bbl), "non-ASCII character left in the bibliography"
    return bbl


def main():
    tex = (ROOT / "manuscript.tex").read_text()
    body = tex[tex.index(r"\begin{document}") + len("\\begin{document}\n"):]
    body = body.replace("\\linenumbers\n", "", 1)
    body = "\n".join(l for l in body.split("\n") if not l.lstrip().startswith("%")) + "\n"
    body = re.sub(r"\\input\{tables/([^}]+)\}",
                  lambda m: (ROOT / "tables" / (m.group(1) + ".tex")).read_text().rstrip("\n"), body)
    body = body.replace("{figures/", "{")
    body = body.replace("\\begin{appendices}\n", "\\begin{appendices}\n\\renewcommand{\\theHtable}{A\\arabic{table}}\n", 1)
    assert body.count("\\bibliography{references}") == 1
    body = body.replace("\\bibliography{references}", make_bbl().rstrip("\n"))
    out = PREAMBLE + body
    assert "\\input" not in out and "figures/" not in out and "linenumbers" not in out
    assert all(ord(c) < 128 for c in out), "non-ASCII character in the flat manuscript"

    if OUTDIR.exists():
        shutil.rmtree(OUTDIR)
    OUTDIR.mkdir()
    (OUTDIR / "manuscript.tex").write_text(out)
    shutil.copy(ROOT / "sn-jnl.cls", OUTDIR / "sn-jnl.cls")
    figs = sorted((ROOT / "figures").glob("*.pdf"))
    for p in figs:
        shutil.copy(p, OUTDIR / p.name)

    # compile the flat package twice (no bibtex needed) to check that it is self-contained
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for p in OUTDIR.iterdir():
            shutil.copy(p, tmp / p.name)
        run(["pdflatex", "-interaction=nonstopmode", "manuscript.tex"], tmp)
        run(["pdflatex", "-interaction=nonstopmode", "manuscript.tex"], tmp)
        log = (tmp / "manuscript.log").read_text(errors="ignore")
        errors = [l for l in log.split("\n") if l.startswith("!")]
        undefined = re.findall(r"(?:Citation|Reference) `[^']+' .*undefined", log)
        assert not errors, errors
        assert not undefined, undefined
        shutil.copy(tmp / "manuscript.pdf", ROOT / "TB_SEIT_BMB_submission_flat_2026-10-12.pdf")

    files = ["manuscript.tex", "sn-jnl.cls"] + [p.name for p in figs]
    with zipfile.ZipFile(OUTZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            zi = zipfile.ZipInfo(f, date_time=(2026, 10, 12, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, (OUTDIR / f).read_bytes())
    h = hashlib.sha256(OUTZIP.read_bytes()).hexdigest()
    print(f"{OUTZIP.name} {OUTZIP.stat().st_size} bytes; {len(files)} files; sha256 {h}")
    print("compiled: 0 errors, 0 undefined citations or references")


if __name__ == "__main__":
    main()
