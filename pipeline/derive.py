"""Rebuild every derived artefact from data/extractions/ in order.

resolve (canonical ids) -> infer (inherited bounds) -> compare (profiles, tightness;
uses data/condition-classes.yaml from pipeline/classify_conditions.py)
-> report (poset, gap reports) -> acceptance (pilot facts) -> site_index (site analysis data). Validation is separate
(pipeline/validate.py) because it needs the gitignored paper sources.

Usage: uv run python pipeline/derive.py
"""

import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

for step in ("resolve", "infer", "compare", "report", "acceptance", "site_index"):
    print(f"== {step}")
    runpy.run_path(str(HERE / f"{step}.py"), run_name="__main__")
