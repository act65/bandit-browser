# Notes

Hand-maintained technical articles about the atlas's reference material. They are written for reading, not generated, and are not part of the static site. The data they describe live in [`data/`](../data/); when the data change, these notes must be updated by hand.

| Article | Contents |
|---|---|
| [bco-ground-truth.md](bco-ground-truth.md) | Lattimore's *Bandit Convex Optimisation* as ground truth: settings, upper and lower bounds, transfer rules and open problems, from [`data/ground_truth/bco.yaml`](../data/ground_truth/bco.yaml) |
| [pilot-facts.md](pilot-facts.md) | The 14 K-armed and linear bandit facts used as acceptance tests, how [`pipeline/acceptance.py`](../pipeline/acceptance.py) checks them, and their status in the latest report |
| [validation.md](validation.md) | How accurate the atlas is: a second-model audit of 200 random results, a textbook gold set (Lattimore & Szepesvári) and a cross-check against how other papers cite each result |
