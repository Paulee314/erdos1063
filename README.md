# Erdős problem 1063: density of admissible n, a Lean-verified lower bound, and n_k for k ≤ 140

For k ≥ 2, n_k is the least n ≥ 2k such that n − i divides C(n,k) for all but exactly one 0 ≤ i < k
([erdosproblems.com/1063](https://www.erdosproblems.com/1063), OEIS [A389360](https://oeis.org/A389360), Guy B31).

**Paper:** [`paper/erdos1063.pdf`](paper/erdos1063.pdf), *The density of admissible n in Erdős–Selfridge
problem 1063, with a growth conjecture for n_k* (P. Lee, 2026). Main results:

* For each prime p ≤ k, an exact description of which index fails, in terms of Kummer carries.
* The lower bound n_k ≥ W'_k = ∏_{p^a ∥ k} p^(a + ⌊log_p(k−1)⌋). The failing element n − i₀ is
  divisible by W'_k, with equality n_k − i₀ = W'_k exactly for k = 4, 6, 14 among k ≤ 140. In
  particular the failing index is i₀ = n mod k. Both facts are **formally verified in Lean 4** (`lean/`).
* The admissible n form a periodic set. Its density δ(k) is an explicit finite sum, with
  log(1/δ(k)) = C·k/log k + c₂·k/log²k + O(k/log³k), where C = Σ_{j≥1} (1/j)·log(1+1/j) = 1.2577…
  and c₂ = 1.00166….
* Conjecture: log n_k ~ C·k/log k. Four pre-registered out-of-sample tests support it: 78 of 86 values fell
  inside the predicted 90% ranges (77.4 expected).
* Values of n_k for 60 ≤ k ≤ 140 and for prime k ≤ 167. Those for k ≥ 76 are new.

## Related work

* **rickyc**, in the [discussion thread](https://www.erdosproblems.com/forum/thread/1063): proved the k/2
  version of the lower bound (26 June 2026), then the k−1 version in a sharper form (10 July 2026). Our proof
  of the k−1 bound is independent; the equality cases and the Lean formalization are new.
* **jbell31**, in the same thread (28 July 2026), with code at
  [Jaybell31/dreamwalk](https://github.com/Jaybell31/dreamwalk/tree/master/erdos1063): n_k for
  60 ≤ k ≤ 75, from a search that assumes rickyc's divisibility result. Our independently computed values
  agree on all 16. Our Lean file formalizes that divisibility result in full (`index_eq_mod`, `D_dvd`), so
  their minimality claims no longer rest on an unformalized step.
* **R. Cipollini**: two proof claims on the problem page, an upper bound
  log n_k ≤ (k/log k)(log log k + log log log k + log 2 + o(1)) and a lower bound c(log k)².
  **P. White** (erdosproblemaday.com) gives an upper bound of the same shape. The upper bound is recorded in
  DeepMind's formal-conjectures as formalized in Lean by the LEAP agent (Kung et al., arXiv:2606.03303).

## Contents

| Path | What |
|---|---|
| `paper/` | LaTeX source and PDF. |
| `lean/Erdos1063Lower.lean` | Lean 4 + Mathlib proof that W'_k divides n − i₀, that i₀ = n mod k, that rickyc's sharper D(k,i₀) divides n − i₀, and that W'_k ≤ n_k for all k ≥ 3. It also proves Erdős–Selfridge and Cambie's bound n_k ≤ k·lcm(1,…,k−1). It uses the definition of n_k from Google DeepMind's [formal-conjectures](https://github.com/google-deepmind/formal-conjectures) verbatim. `#print axioms` lists only `propext`, `Classical.choice` and `Quot.sound`. See `lean/README.md` to re-check it (about 7 seconds after setup). |
| `notes/theorem8_proof.md` | Full proof of log(1/δ(k)) = (C+o(1)) k/log k. |
| `notes/second_order_proof.md` | Proof of the second-order term c₂·k/log²k, plus the expansion to any order. |
| `notes/lemmas.md`, `notes/CROSSCHECK_PACKET.md` | Complete statements and proofs, with the record of independent review. |
| `data/A389360_extended_2_140.txt` | n_k for 2 ≤ k ≤ 140 ("k n" per line). The values for k ≤ 59 agree with the OEIS b-file. (`_2_110` is the earlier version.) |
| `data/all_values_2_140.txt` | The same, with the failing index i₀. |
| `data/primes_149_167.txt` | n_k for the primes k = 149, 151, 157, 163, 167. |
| `data/PREDICTIONS_*.txt` | Model predictions, each written and committed **before** the corresponding n_k were computed (timestamps inside): 60–100, 101–110, 111–120 with primes to 139, and 121–140 with primes to 199. |
| `data/density2_*.txt` | Exact log(1/δ(k)) from the density formula. |
| `data/lists/` | The first 139–168 admissible n for k ∈ {40, 45, 50, 61, 64, 67}, with the trajectory analysis. |
| `code/` | Searches and checks: `w4_1063.c` (current exhaustive search, 128-bit, multithreaded; used for k ≥ 111), `wheel1063.c` (the search used for k ≤ 110), `scan1063.c` (plain valuation scan), `density2.c` (exact δ(k)), `verify_exact.py` (big-integer verification), `score_predictions.py` (scores values against a predictions file), `ref.py` (brute force for k ≤ 29), and the statistics and numerics scripts. |
| `results/` | Raw run logs, including plain-scan minimality confirmations. `results/w4/` holds the k ≥ 111 runs: validation, run logs, scores and the independent cross-check (`fable_xcheck*`). |
| `review/` | Code written independently by AI reviewers to re-derive the values, δ(k) and the constants. |

Build the current search: `cc -O3 -o w4_1063 code/w4_1063.c -lpthread`, then run `./w4_1063 k lo hi`
(searches [lo, hi) on all cores; for k ≥ 121 we used `QMAX=4e18 CNTMAX=2e7`). It prints the least admissible n
in the range, or `none`. The older search: `gcc -O3 -march=native -fopenmp -o wheel1063 code/wheel1063.c`, then
`QMAX=1e13 CNTMAX=1e6 ./wheel1063 k [lo hi]`.

The new search uses rickyc's modulus D(k,e) (formally verified as `D_dvd` in the Lean file) and Lemma 4.1 of the
paper at every prime in (√k, k]. Before the new runs it reproduced all 109 values for 2 ≤ k ≤ 110 exactly.

## Provenance

The analysis, the code and the first drafts were produced with Claude (Anthropic) at the author's
direction. The mathematics was checked by further AI reviewers (other Claude instances, Gemini, Grok and a Meta AI model),
using independently written code. Every value of n_k was verified with exact integer arithmetic. Minimality was
confirmed by two independent exhaustive searches for every k ≤ 119 and k = 127; for the other new values it rests
on one search, validated as above. The lower bound is machine-checked
in Lean. The remaining proofs have been refereed by AI reviewers but not yet by a human.
