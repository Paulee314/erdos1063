# Erdős problem 1063: density of admissible n, a Lean-verified lower bound, and n_k for k ≤ 110

For k ≥ 2, n_k is the least n ≥ 2k such that n − i divides C(n,k) for all but exactly one 0 ≤ i < k
([erdosproblems.com/1063](https://www.erdosproblems.com/1063), OEIS [A389360](https://oeis.org/A389360), Guy B31).

**Paper:** [`paper/erdos1063.pdf`](paper/erdos1063.pdf), *The density of admissible n in Erdős–Selfridge
problem 1063, with a growth conjecture for n_k* (P. Lee, 2026). Main results:

* For each prime p ≤ k, an exact description of which index fails, in terms of Kummer carries.
* The lower bound n_k ≥ W'_k = ∏_{p^a ∥ k} p^(a + ⌊log_p(k−1)⌋). The failing element n − i₀ is
  divisible by W'_k, with equality n_k − i₀ = W'_k exactly for k = 4, 6, 14 among k ≤ 110. In
  particular the failing index is i₀ = n mod k. Both facts are **formally verified in Lean 4** (`lean/`).
* The admissible n form a periodic set. Its density δ(k) is an explicit finite sum, with
  log(1/δ(k)) = C·k/log k + c₂·k/log²k + O(k/log³k), where C = Σ_{j≥1} (1/j)·log(1+1/j) = 1.2577…
  and c₂ = 1.00166….
* Conjecture: log n_k ~ C·k/log k. Two pre-registered out-of-sample tests support it.
* Values of n_k for 60 ≤ k ≤ 110, of which 76 ≤ k ≤ 110 are new.

## Related work

* **rickyc**, in the [discussion thread](https://www.erdosproblems.com/forum/thread/1063): proved the k/2
  version of the lower bound (26 June 2026), then the k−1 version in a sharper form (10 July 2026). Our proof
  of the k−1 bound is independent; the equality cases and the Lean formalization are new.
* **jbell31**, in the same thread (28 July 2026), with code at
  [Jaybell31/dreamwalk](https://github.com/Jaybell31/dreamwalk/tree/master/erdos1063): n_k for
  60 ≤ k ≤ 75, from a search that assumes rickyc's divisibility result. Our independently computed values
  agree on all 16. Our Lean file formalizes the "failing index = n mod k" half of that result; the sharper
  exponent is not formalized here.
* **R. Cipollini**: two proof claims on the problem page, an upper bound
  log n_k ≤ (k/log k)(log log k + log log log k + log 2 + o(1)) and a lower bound c(log k)².
  **P. White** (erdosproblemaday.com) gives an upper bound of the same shape. The upper bound is recorded in
  DeepMind's formal-conjectures as formalized in Lean by the LEAP agent (Kung et al., arXiv:2606.03303).

## Contents

| Path | What |
|---|---|
| `paper/` | LaTeX source and PDF. |
| `lean/Erdos1063Lower.lean` | Lean 4 + Mathlib proof that W'_k divides n − i₀, that i₀ = n mod k, and that W'_k ≤ n_k for all k ≥ 3. It also proves Erdős–Selfridge and Cambie's bound n_k ≤ k·lcm(1,…,k−1). It uses the definition of n_k from Google DeepMind's [formal-conjectures](https://github.com/google-deepmind/formal-conjectures) verbatim. `#print axioms` lists only `propext`, `Classical.choice` and `Quot.sound`. See `lean/README.md` to re-check it (about 7 seconds after setup). |
| `notes/theorem8_proof.md` | Full proof of log(1/δ(k)) = (C+o(1)) k/log k. |
| `notes/second_order_proof.md` | Proof of the second-order term c₂·k/log²k, plus the expansion to any order. |
| `notes/lemmas.md`, `notes/CROSSCHECK_PACKET.md` | Complete statements and proofs, with the record of independent review. |
| `data/A389360_extended_2_110.txt` | n_k for 2 ≤ k ≤ 110 ("k n" per line). The values for k ≤ 59 agree with the OEIS b-file. |
| `data/all_values_2_110.txt` | The same, with the failing index i₀. |
| `data/PREDICTIONS_60_100.txt`, `data/PREDICTIONS_101_110.txt` | Model predictions, written **before** the corresponding n_k were computed (timestamps inside). |
| `data/density2_*.txt` | Exact log(1/δ(k)) from the density formula. |
| `data/lists/` | The first 139–168 admissible n for k ∈ {40, 45, 50, 61, 64, 67}, with the trajectory analysis. |
| `code/` | Searches and checks: `wheel1063.c` (fast exhaustive search), `scan1063.c` (plain valuation scan), `density2.c` (exact δ(k)), `verify_exact.py` (big-integer verification), `ref.py` (brute force for k ≤ 29), and the statistics and numerics scripts. |
| `results/` | Raw run logs, including plain-scan minimality confirmations. |
| `review/` | Code written independently by AI reviewers to re-derive the values, δ(k) and the constants. |

Build the search: `gcc -O3 -march=native -fopenmp -o wheel1063 code/wheel1063.c`, then run
`QMAX=1e13 CNTMAX=1e6 ./wheel1063 k [lo hi]`.

## Provenance

The analysis, the code and the first drafts were produced with Claude (Anthropic) at the author's
direction. The mathematics was checked by further AI reviewers (other Claude instances, Gemini, Grok and a Meta AI model),
using independently written code. Every value of n_k was verified with exact integer arithmetic, and
minimality was confirmed by two independent exhaustive searches. The lower bound is machine-checked
in Lean. The remaining proofs have been refereed by AI reviewers but not yet by a human.
