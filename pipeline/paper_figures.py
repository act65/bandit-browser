"""Figures for the paper, rendered from the data (vector PDF), not screenshotted from the site.

settings-map-action.pdf, settings-map-status.pdf: the settings similarity map (site/layout.py, the same
seeded t-SNE the site's graph uses), coloured by action space and by the status of each setting's main
regime (site/analysis.py setting_status). Print colours: the site's light-mode palette, with the
"no comparable ..." statuses kept muted so verdicts stand out, but darker than on screen.

Usage: uv run --with matplotlib python pipeline/paper_figures.py --out ../bandit-browser-paper/figures
"""

from __future__ import annotations

import argparse
import collections
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "site"))
sys.path.insert(0, str(ROOT / "pipeline"))
sys.argv, _argv = sys.argv[:1], sys.argv  # site/build.py parses argv on import in some paths
import analysis  # noqa: E402
import build  # noqa: E402
import layout  # noqa: E402
from order import Order  # noqa: E402

sys.argv = _argv
SLOTS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]  # --s1..--s8
OTHER = "#9a9a9f"
STATUS = {"tight": "#0ca30c", "log_gap": "#f2a900", "poly_gap": "#e8703f", "conflict": "#c62828",
          "no_lower": "#8fb3e3", "no_upper": "#b5a9e0", "none": "#cfcfcc"}
STATUS_LABEL = {"tight": "tight", "log_gap": "log gap", "poly_gap": "polynomial gap", "conflict": "conflict",
                "no_lower": "no comparable lower bound", "no_upper": "no comparable upper bound",
                "none": "no comparable bounds"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT.parent / "bandit-browser-paper" / "figures"))
    args = ap.parse_args()
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    site = build.Site(build.REPO)
    site.analysis = analysis.Analysis(build.REPO, site)
    ids = list(site.nodes)
    orders = Order(site.onto.data).orders if site.onto.data.get("dimensions") else {}
    pos = layout.similarity({i: site.nodes[i]["key"] for i in ids}, orders, gap=60)
    acts = [site.nodes[i]["key"].get("action_space", "") for i in ids]
    slots = build.colour_slots(acts)
    size = {i: sum(site.counts(site.nodes[i])) for i in ids}
    status = {i: site.analysis.setting_status(i)[0] for i in ids}
    xs = [pos[i][0] for i in ids]
    ys = [-pos[i][1] for i in ids]  # screen coordinates have y downwards
    ss = [6 + 4 * (size[i] ** 0.5) for i in ids]
    out = Path(args.out)

    def panel(colours, handles, name, zorder=None):
        fig, ax = plt.subplots(figsize=(4.2, 4.0))
        order = sorted(range(len(ids)), key=(zorder or (lambda k: 0)))
        ax.scatter([xs[k] for k in order], [ys[k] for k in order], s=[ss[k] for k in order],
                   c=[colours[k] for k in order], linewidths=0.3, edgecolors="white")
        ax.set_aspect("equal")
        ax.axis("off")
        ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=2, fontsize=6.5,
                  frameon=False, handletextpad=0.2, columnspacing=0.8)
        fig.tight_layout(pad=0.2)
        fig.savefig(out / f"{name}.pdf", bbox_inches="tight")
        plt.close(fig)

    dot = lambda c, lab: Line2D([], [], marker="o", ls="", color=c, markersize=4.5, label=lab)  # noqa: E731
    act_col = [SLOTS[slots[a] - 1] if slots.get(a) else OTHER for a in acts]
    seen, act_handles = set(), []
    for a, s in sorted(slots.items(), key=lambda t: (t[1] == 0, t[1])):
        lab = "other" if s == 0 else build.value_label("action_space", a)
        if lab not in seen and s:
            seen.add(lab)
            act_handles.append(dot(SLOTS[s - 1], lab))
    act_handles.append(dot(OTHER, "other"))
    panel(act_col, act_handles, "settings-map-action")

    st_col = [STATUS[status[i]] for i in ids]
    rank = {k: r for r, k in enumerate(["none", "no_upper", "no_lower", "log_gap", "poly_gap", "tight", "conflict"])}
    counts = collections.Counter(status.values())
    st_handles = [dot(STATUS[k], f"{STATUS_LABEL[k]} ({counts[k]})") for k in
                  ["tight", "log_gap", "poly_gap", "conflict", "no_lower", "no_upper", "none"] if counts[k]]
    panel(st_col, st_handles, "settings-map-status", zorder=lambda k: rank[status[ids[k]]])  # verdicts on top
    print(f"{len(ids)} settings -> {out}/settings-map-{{action,status}}.pdf", dict(counts))


if __name__ == "__main__":
    main()
