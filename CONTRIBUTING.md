# Contributing corrections

Every result in the atlas was extracted from a paper by an LLM. Most are not human-verified, so corrections are
the most valuable contribution.

## Reporting

- **On the site**: every setting page, paper page and result has a *Report a problem* link. It opens a GitHub issue
  ([correction form](.github/ISSUE_TEMPLATE/correction.yml)) with the page and the result id filled in.
- **By email**: write to the maintainer with the page link. That works too.

A one-line pointer ("Theorem 3 is a lower bound, not an upper bound") is enough; evidence (theorem number, quote)
speeds things up.

## How a report becomes a fix

Extractions in `data/extractions/` are never edited by hand: they are the reproducible output of
`pipeline/extract.py`. Fixes go into [`data/corrections.yaml`](data/corrections.yaml), which `pipeline/resolve.py`
applies on top of them. Each entry records the target, the operation, the reason, who made it and its review status:

```yaml
  - target: auer2002exp3:r14          # <paper id>:<result id>, or <paper id>:* for the whole paper
    op: multiply_expression_by        # set (field, value) | multiply_expression_by (factor) | add_condition (value)
    factor: T
    reason: >
      Theorem 9.1 bounds the average regret; multiplying by T states it for total regret.
    by: <name or handle>, <date>
    status: pending_human_review      # pending_human_review | verified (checked against the paper by a person)
```

`add_condition` is the usual fix for a result that is correct but mis-scoped (proved for a different feedback
protocol, a restricted instance class, a specific algorithm class): give the condition a class in
[`data/condition-classes.yaml`](data/condition-classes.yaml) (`model_change`, `instance_restriction`,
`algorithm_restriction`, ...) and `pipeline/compare.py` keeps the result out of the setting's rate while still
showing it.

After editing, run `uv run python pipeline/derive.py` (rebuilds the canonical layer, comparisons and reports) and
`uv run python site/build.py`, and open a pull request. Corrections from authors are marked
`status: verified` with a note.
