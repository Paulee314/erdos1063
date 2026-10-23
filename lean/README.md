# Lean 4 formalization: Erdős problem 1063, lower bound

`Erdos1063Lower.lean` is a machine-checked proof (Lean 4 + Mathlib, toolchain
leanprover/lean4:v4.36.0-rc1) of:

| Lean name | Statement |
|---|---|
| `valuation_bound` | If every `n - i` (`0 ≤ i < k`, `i ≠ i0`) divides `C(n,k)` and `p` is a prime dividing `k`, then `v_p(k) + ⌊log_p(k-1)⌋ ≤ v_p(n - i0)`. (Paper: Proposition 5 / Corollary 5. It does not even need `i0 < k`.) |
| `W_dvd` | Under the same hypothesis, `W'_k = ∏_{p∣k} p^(v_p(k)+⌊log_p(k-1)⌋)` divides `n - i0`. |
| `k_dvd`, `index_eq_mod` | Under the same hypothesis, `k ∣ n - i0`; so the failing index is `i0 = n mod k`. |
| `sharp_valuation_bound`, `D_dvd` | rickyc's sharper exponent (erdosproblems.com thread, 10 July 2026): for `p ∣ k`, `v_p(k) + v_p(C(k-1,e)) + ⌊log_p max(e, k-1-e)⌋ ≤ v_p(n - e)`, and the product `D(k,e)` divides `n - e`. With `index_eq_mod`, this is exactly the structural input of jbell31's exhaustive search for 60 ≤ k ≤ 75, so their minimality claims no longer rest on an unformalized step. |
| `exists_exception'` | Erdős–Selfridge: for `k ≥ 2`, `n ≥ 2k`, some `n - i` fails to divide `C(n,k)`. |
| `cambie_mem`, `cambie_upper_bound` | `k·lcm(1..k-1)` is admissible, so `n_k ≤ k·lcm(1..k-1)` for `k ≥ 3`. |
| `W_le_n_of_three_le` | **Main result:** `W'_k ≤ n_k` for every `k ≥ 3`. |

The definition of `n_k` is copied verbatim from DeepMind's
`FormalConjectures/ErdosProblems/1063.lean`. `#print axioms` reports only Lean's standard
axioms (`propext`, `Classical.choice`, `Quot.sound`): no `sorry`. Sanity check in the file:
`W'_4, W'_6, W'_14, W'_30 = 8, 72, 784, 324000`.

Context: DeepMind's LEAP agent (Kung et al., arXiv:2606.03303) has formalized the upper
bounds for this problem (Erdős–Selfridge, Monier, Cambie, and the subexponential bound).
No lower bound appears in that file.

## Re-checking

```
# one-time setup (≈7 GB; prebuilt Mathlib downloaded, not compiled)
./setup.sh
# check the proof (≈7 s)
./check.sh Erdos1063Lower.lean && cat Erdos1063Lower.out   # expect EXIT=0
```
`setup.sh` installs `elan` into `~/.elan` without modifying shell profiles and creates the
Mathlib project `erdos1063/`.
