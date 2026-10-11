"""Static checks for manuscript.tex (no compilation): environments, braces, citations, labels, inputs, figures.
Run from manuscript_latex/:  python tools/lint_latex.py
"""
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
tex = (root / "manuscript.tex").read_text(encoding="utf8")
problems = []

def strip_comments(t):
    return "\n".join(re.sub(r"(?<!\\)%.*", "", ln) for ln in t.split("\n"))

body = strip_comments(tex)
parts = {"manuscript.tex": body}
for m in re.finditer(r"\\input\{([^}]+)\}", body):
    f = root / (m.group(1) + ".tex")
    if not f.exists():
        problems.append(f"missing input file {f}")
    else:
        parts[m.group(1)] = strip_comments(f.read_text(encoding="utf8"))
full = "\n".join(parts.values())

# braces per file
for name, t in parts.items():
    t2 = re.sub(r"\\[{}]", "", t)
    if t2.count("{") != t2.count("}"):
        problems.append(f"{name}: unbalanced braces {t2.count('{')} vs {t2.count('}')}")
# environments
stack = []
for m in re.finditer(r"\\(begin|end)\{([^}]+)\}", full):
    kind, env = m.groups()
    if kind == "begin":
        stack.append(env)
    else:
        if not stack or stack.pop() != env:
            problems.append(f"environment mismatch at \\end{{{env}}}")
if stack:
    problems.append(f"unclosed environments: {stack}")
# math delimiters: odd number of unescaped $ per paragraph
for i, para in enumerate(re.split(r"\n\s*\n", full)):
    q = re.sub(r"\\\$", "", para)
    q = q.replace("$$", "")
    if q.count("$") % 2:
        problems.append(f"odd number of $ in paragraph starting: {para.strip()[:70]!r}")
# citations vs bib
bib = (root / "references.bib").read_text(encoding="utf8")
keys = set(re.findall(r"@\w+\{([^,]+),", bib))
cited = set()
for m in re.finditer(r"\\cite[a-z]*\{([^}]+)\}", full):
    cited |= {k.strip() for k in m.group(1).split(",")}
for k in sorted(cited - keys):
    problems.append(f"cited key not in bib: {k}")
for k in sorted(keys - cited):
    problems.append(f"bib entry never cited: {k}")
# labels / refs
labels = set(re.findall(r"\\label\{([^}]+)\}", full))
for m in re.finditer(r"\\(?:ref|eqref)\{([^}]+)\}", full):
    if m.group(1) not in labels:
        problems.append(f"undefined reference {m.group(1)}")
dup = [l for l in labels if len(re.findall(r"\\label\{" + re.escape(l) + r"\}", full)) > 1]
problems += [f"duplicate label {l}" for l in dup]
# constructs that break inside the sn-jnl table environment (seen in Overleaf, 2026-10-11)
for bad in (r"\resizebox", r"\parbox", r"\begin{threeparttable}"):
    if bad in full:
        problems.append(f"{bad} found: breaks inside sn-jnl tables")
# figures
for m in re.finditer(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", full):
    if not (root / m.group(1)).exists():
        problems.append(f"missing figure {m.group(1)}")
# abstract length
a = re.search(r"\\abstract\{(.*?)\}\n\\keywords", tex, re.S).group(1)
words = len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", re.sub(r"\\[a-zA-Z]+|\$[^$]*\$", " ", a)))
print(f"abstract words (approx): {words}; cited keys: {len(cited)}; bib keys: {len(keys)}; labels: {len(labels)}")
print("PROBLEMS:" if problems else "no problems found")
for p in problems:
    print(" -", p)
sys.exit(1 if problems else 0)
