"""Write the numbered reference list into docs/paper.md (between "## References" and the next heading) from
docs/references.py, numbering the dataset sources in Table 1 order. Fails if the paper cites a number that does not exist.

  python docs/render_references.py corpus/corpus.csv
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "docs"))
import references as R  # noqa: E402

datasets = list(dict.fromkeys(r["dataset"] for r in csv.DictReader(open(sys.argv[1], encoding="utf-8"))))
num, last = R.numbering(datasets)
refs = [R.ALLMETA if m == "ALLMETA" else m for m in R.METHODS]
refs += [R.DATASETS[d] for d in datasets if d not in R.SAME_AS]
refs += [R.ARCHIVE]
assert len(refs) == last, (len(refs), last)
listing = "\n".join(f"{i}. {t}" for i, t in enumerate(refs, 1))
p = ROOT / "docs" / "paper.md"
s = p.read_text(encoding="utf-8")
s = re.sub(r"(## References\n\n)(.*?)(\n\n## )", lambda m: m.group(1) + listing + m.group(3), s, count=1, flags=re.S)
cited = set()
for grp in re.findall(r"\[(\d[\d,–\- ]*)\]", s.split("## References")[0]):
    for part in grp.split(","):
        a, _, b = part.strip().replace("–", "-").partition("-")
        cited.update(range(int(a), int(b or a) + 1))
bad = sorted(c for c in cited if c < 1 or c > len(refs))
uncited = sorted(set(range(1, len(refs) + 1)) - cited)
p.write_text(s, encoding="utf-8")
print(f"{len(refs)} references written; cited {len(cited)}; uncited {uncited}; out of range {bad}")
if bad or uncited:
    sys.exit(1)
