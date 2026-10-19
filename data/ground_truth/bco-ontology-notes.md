# What bandits ontology v0.1 cannot say about BCO

Source: Lattimore, *Bandit Convex Optimisation*, arXiv:2402.06535v5. Ground truth is in [`bco.yaml`](bco.yaml).
Order convention follows [schema.md](../../schema.md): **a ⊑ b means "a is a special case of b"**, so upper bounds flow from b to a and lower bounds from a to b.

## Summary

v0.1 has a single `action_space: convex` value. In the book, the whole content of the BCO tables sits *inside* that value. Settings differ along five axes that v0.1 does not model:

1. the function class (properties b, l, sm, sc, lin, quad and their parameters);
2. the domain/query model (constrained, improper, unconstrained);
3. the geometry and representation of K;
4. the noise model (noise-free vs conditionally subgaussian, action-dependent);
5. dimension restrictions (`d = 1`).

All but two of the 19 setting nodes in `bco.yaml` map to the same v0.1 tuple, up to `environment` and `noise`. The two exceptions differ only in `objective`. Without these additions the 29 upper bounds in Table 2.2 would all land on two v0.1 nodes and could not be compared (D2).

## Proposed changes (in priority order)

### 1. New dimension `function_class`: multi-select property set with a parameter vector

Values are the Definition 1.1 properties. Convexity is always assumed.

| value | meaning | parameter |
|---|---|---|
| `bounded` | f(x) ∈ [0,1] on K (Prop b) | range B (default 1) |
| `lipschitz` | f(x) − f(y) ≤ ‖x − y‖ on K (Prop l) | Lipschitz constant L (default 1) |
| `smooth` | f − (β/2)‖x‖² concave (Prop sm) | β ≥ 0, known |
| `strongly_convex` | f − (α/2)‖x‖² convex (Prop sc) | α > 0, known |
| `quadratic` | f = xᵀAx + bᵀx + c (Prop quad) | — |
| `linear` | f = bᵀx + c (Prop lin) | — |

Order: classes are intersections, so `F_P ⊑ F_Q iff Q ⊆ P` (more properties give a smaller class, i.e. a special case). This is the product order over boolean flags with `true ⊑ false`. The engine also needs these implication rules, so that the closure is correct:

- `linear ⇒ quadratic` (A = 0);
- `linear ⇒ smooth with β = 0`. The book uses this in Note 6.vi to transfer linear lower bounds to smooth classes;
- `quadratic ⇒ smooth`, with β = 2‖A‖;
- parameter monotonicity: smooth(β) ⊑ smooth(β′) if β ≤ β′, and strongly_convex(α) ⊑ strongly_convex(α′) if α ≥ α′.

Values to reserve for the book's other classes: `highly_smooth_p` (order-p smoothness, Note 1.i and Note 6.vi), `submodular_lovasz` (Ch. 13), `quasi_convex`, `polyak_lojasiewicz`, `non_convex_stationary` (Outlook 14.vi). Note the book's remark that quasi-convex and PL classes "are not closed under addition and hence are not amenable to the adversarial setting". The engine should therefore flag `adversarial × non-additive class` combinations as ill-posed rather than as gaps.

This supersedes `action_space: linear_infinite`. Add an explicit **equivalence edge**: `action_space=linear_infinite ≡ action_space=convex_body + function_class={bounded, linear}`, so that linear-bandit results from the wider corpus land on the BCO node `F_{b,lin}` (D1, equivalent nodes).

### 2. New dimension `domain` (query and comparison model)

Values:

- `improper`: the learner may query anywhere in ℝᵈ but is compared with the best point in K. b/l hold only on K, sm/sc on ℝᵈ.
- `constrained`: query and compare in K.
- `unconstrained`: K = ℝᵈ.

Order (Note 1.iii; §2.4 bullet 1): `improper ⊑ constrained` and `improper ⊑ unconstrained`; constrained and unconstrained are incomparable. Validity scope: in the improper setting the property flags are evaluated on different sets (b and l on K, sm and sc everywhere), so the edge carries a note rather than an identity on `function_class`.

### 3. New node-parameter dimension `constraint_set` (D11 parameterised settings)

Lower bounds in Table 2.1 are proved for *specific* bodies (B₁, a product of circles, [−1,1]ᵈ). Upper bounds depend on geometry through D = diam(K), the barrier parameter ϑ, and positioning.

- `shape`: `any_convex_body` (Assumption 1.2) ⊒ `rounded` (B₁ ⊂ K ⊂ B_{2d}, Assumptions 10.1 and 11.2) ⊒ `ball`, `hypercube`, `polytope`; plus `nonconvex` (allowed for linear lower bounds only, via the conv(K) reduction).
- `position`: `arbitrary`, `john`, `lowner`, `isotropic`. Every body has an affine image in each position (Theorem 3.14). This is a computational cost, not a statistical assumption, for classes that are affine-invariant (b, lin, quad), but *not* for l, sm, sc.
- `representation`: `polytope`, `separation_oracle`, `membership_oracle`, `point_cloud`. This affects computation only.

A lower bound on K = B₁ is a lower bound on the family "all convex bodies", since the worst case over K includes B₁. It is not a lower bound for every K. Lower-bound transfer along `shape` must therefore go from specific to general only.

### 4. Extend `noise`

- Add `noise_free` (most adversarial results: Assumptions 5.1, 6.1, 7.14, 8.1).
- Add `conditionally_subgaussian` (Assumption 1.4): a martingale difference with ψ₂-norm ≤ 1 that may depend on the action and history. It is not iid, and the action dependence is essential for the submodular reduction.
- Keep `gaussian`.

Order: `noise_free ⊑ conditionally_subgaussian`, `gaussian ⊑ conditionally_subgaussian`. Add a `log_factor_transfer` edge `gaussian → bounded` for lower bounds (Shamir's scaling and truncation argument; §2.4 bullets 3–4).

### 5. Fix the meaning of `environment` for BCO

- `stochastic` in BCO means f_t = f plus conditionally subgaussian noise. Mapping it to `stochastic_iid` is approximate; consider a value `stochastic_fixed_function`.
- `adversarial` in the book allows noise and does not fix obliviousness in the tables. Add `adversarial_unspecified`, or default to oblivious with a flag.
- Validity scope of `stochastic ⊑ adversarial`: it holds exactly only for the book's *noisy* adversarial model. It holds up to log factors for noise-free adversarial models with bounded losses. Encode the two as different edge kinds.

### 6. Dimension restriction as a node parameter

`d = 1` appears as a subscript on classes (`F_{b,d=1}`, `F^(s)_{l,d=1}`). Model it as a parameter constraint on the node (`params: {d: 1}`). The edge `d = 1 ⊑ general d` comes with the parameter map d ↦ 1, so general-d upper bounds instantiate at d = 1.

### 7. Extend `feedback`

Add `two_point` (or `multi_point_k`), with `full_information ⊑ two_point ⊑ bandit` (Note 1.vi; ADX10's title is "multi-point bandit feedback").

### 8. Objectives and quantities

- `pac_epsilon_best` is phrased for arms. Generalise it to `epsilon_optimal_point` (sample complexity of finding x with f(x) ≤ inf f + ε w.p. ≥ 1 − δ). Table 2.2 mixes regret rows (in n) and sample-complexity rows (in ε) in one table.
- The book's `Reg_n = sup_x Σ (f_t(X_t) − f_t(x))` puts the sup inside the expectation. It is *not* pseudo-regret. Keep `expected_regret` distinct from `pseudo_regret`. Add a way to say "unspecified expectation/high-probability": Table 2.2 never says, so `bco.yaml` uses quantity `regret` with `probability: null`.
- Add `minimax_bayesian_regret` (Theorem 8.17 equates it with adversarial minimax regret).
- Add complexity measures `information_ratio` (Ψ*) and `exp_by_opt_ratio` (Λ*). Theorem 8.22 and Exercise 8.24 relate them. The book warns that their lower bounds do **not** transfer to regret lower bounds, so this needs a `non_transfer` edge kind.

### 9. Result-level fields that BCO needs (schema, not ontology)

- **`compute`**: per-round complexity, with `infinity` for non-constructive results (BDKP15, BEL18, Lat20-cvx). "Best bound" and "best polynomial-time bound" are different regimes (D2). Example: for adversarial F_b, the polynomial-time d^2.5 bound (LFMV24, Ch. 11) only recently caught up with the non-constructive d^2.5 bound (Lat20-cvx). Before that, the best polynomial-time bound was d^10.5 (BEL16). For stochastic F_b, d^1.5 needs Löwner positioning, and Exercise 10.17 asks whether that can be done in polynomial time for general K. d^2 needs isotropic positioning. Without `compute` and `positioning_required` these trade-offs disappear.
- **`positioning_required`** (Löwner or isotropic) and **`non_constructive: bool`**.
- **`errata`** (D5): ADX10's proof is "only sketched" with "minor issues".
- **Book re-derivations vs originals**: the book's hyperlinked theorem often differs from the original paper's statement (constants, logs, probability). `bco.yaml` keeps `original_citation` and `book_theorem` separate. The schema should support "this result is restated in X with a different proof" (two provenance records on one result).

### 10. Canonical variable table

- `D` is already "delay" in v0.1 but the book uses it for diam(K). Add `diam_K`.
- Add `vartheta` (self-concordance parameter), `alpha` and `beta` (curvature parameters), `p` (smoothness order), `M_K` (the book's M(K) width parameter) and `d_2` (quadratic-to-linear lifted dimension).
- `L` is overloaded in v0.1 (action norm or Lipschitz). The book also uses L for a logarithmic factor in Theorems 10.8 and 11.8. Split it into `L_lip` and `L_feat`.
- Record that the book uses `n` for the horizon (canonical `T`).

### 11. Transfer-rule (edge) kinds needed beyond D1's list

D1 lists inclusion, reduction, metric_transfer and log_factor_transfer. BCO also needs:

- **`easier_harder_ordering` without set inclusion**: improper vs constrained is not an inclusion of environment classes. The learner gets more power.
- **reductions that ignore computation**: quadratic → linear with d ↦ d₂ = (d² + 3d + 2)/2 (§7.6). The edge needs a `statistical_only: true` flag, since it does not preserve the `compute` field.
- **metric transfers with a known non-tightness witness**: cumulative → simple regret. §2.4 shows that it is not tight (Θ(d√n) cumulative vs O(d²/n) simple for quadratic sm+sc, improper). Store the witness as a separation (D1 first-class separations).
- **cross-problem reductions**: bandit submodular minimisation → BCO on [0,1]ᵈ via the Lovász extension (Prop. 13.9), with an additive √(2n log(1/δ)) cost and parameter map diam = √d, ϑ = Θ(d).
- **`non_transfer`**: complexity-measure lower bounds do not give regret lower bounds (§8.7). This is worth storing so that the engine never infers it.

## Minimal v0.2 diff (concrete)

```yaml
action_space:
  + convex_body            # replaces `convex`; curvature/regularity moves to function_class
function_class:            # NEW, multi-select, order = reverse set inclusion
  values: [bounded, lipschitz, smooth, strongly_convex, quadratic, linear,
           highly_smooth_p, submodular_lovasz, quasi_convex, polyak_lojasiewicz]
  implications: [linear => quadratic, linear => smooth(beta=0), quadratic => smooth]
  params: {B: 1, L_lip: 1, beta: ">=0 known", alpha: ">0 known", p: ">=2"}
domain:                    # NEW
  values: [improper, constrained, unconstrained]
  order: [improper ⊑ constrained, improper ⊑ unconstrained]
constraint_set:            # NEW node parameter (D11)
  shape: [any_convex_body, rounded, ball, hypercube, polytope, nonconvex]
  position: [arbitrary, john, lowner, isotropic]
  representation: [polytope, separation_oracle, membership_oracle, point_cloud]
noise:
  + noise_free             # noise_free ⊑ conditionally_subgaussian
  + conditionally_subgaussian
environment:
  + stochastic_fixed_function   # f_t = f, martingale-difference noise
  + adversarial_unspecified
feedback:
  + two_point              # full_information ⊑ two_point ⊑ bandit
objective:
  + epsilon_optimal_point  # generalises pac_epsilon_best to continuous K
quantity:
  + regret_unspecified_probability
  + minimax_bayesian_regret
  + information_ratio
  + exp_by_opt_ratio
node_params:
  + d_fixed                # e.g. d = 1
learner_knows:
  + alpha
  + beta
  + n                      # = T
variables:
  + diam_K
  + vartheta
  + alpha
  + beta
  + p
  + M_K
  + d_2
  + L_lip                  # split of overloaded L
edge_kinds:
  + easier_harder_ordering
  + statistical_only_reduction
  + cross_problem_reduction
  + non_transfer
result_fields:
  + compute
  + non_constructive
  + positioning_required
  + errata
  + book_restatement
```

## Things that went wrong or were ambiguous while extracting (for the gold set, D6)

- Table 2.1 and Table 2.2 use the same superscripts `(s)` and `(i)` with *different* semantics. In the lower-bound table they mean "holds already in the easier setting"; in the upper-bound table they mean "only covers / needs". An LLM extractor will likely conflate them, so this is a good gold-set probe.
- Missing `(s)` in Table 2.2 means adversarial. Missing `(i)` means constrained. Neither is written; both are defaults.
- The BLN15 row has class `F^(s)` (no `b`), but Note 2.v says `F_b`, and the table uses Õ where the note uses O. Recorded as a conflict.
- The BEL18 row cites a bib entry for a Langevin Monte Carlo paper. It is probably meant to be BE18 (Bubeck–Eldan, "Exploratory distributions"). Recorded as a low-confidence citation.
- The LFMV24 adversarial row hyperlinks to Theorem 10.8 (stochastic), but the chapter column says Ch. 11. The matching statement is Theorem 11.8.
- The HL14 row has a misplaced parenthesis in the LaTeX (`\sqrt{(\vartheta + \beta/\alpha)n)}`).
- Outlook 14.i has a stray `§` after the adversarial bound.
- In the book, `L` in Theorems 10.8 and 11.8 is a logarithmic factor, not a Lipschitz constant. A naive extractor will map it to the canonical `L`.
