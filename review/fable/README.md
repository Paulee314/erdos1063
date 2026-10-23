Independent review of Erdős #1063 work by Claude Fable 5.1 (2026-10-21), written with fresh code only.
- verify_values.*: exact big-integer validity of all 99 values; W'_k | n_k - i0; comparison with the OEIS b-file.
- density_exact.*: exact rational delta(k) for k=2..110, computed without Lemma 3 (direct Legendre test per residue class).
- period_bruteforce.py / period_bf.c: counts over full periods reproduce delta(k) exactly.
  period_bf_2_8.out covers k=2..8. Fable's k=9..12 run was not saved to a file, so it was re-run later with the same
  period_bf.c; see period_bf_9_12.out and period_bf_9_12_compare.txt (11/630, 11/7560, 9803/831600, 1/1386).
- random_tests.*: Lemma 1+3, periodicity mod p^(2L), Corollary 5 and Lemma 6 against exact divisibility.
- plainscan.c: plain exhaustive scan (minimality) for k=61,64,67,71,73 and b-file values.
- wstep.c: W'-stepping search; confirms k=60,62,63,65,66,68,69,70,72,74. (wstep_new2.out is empty: the k=76 run was
  still going when the files were captured. k=76 is covered by mywheel_60_100.out.)
- mywheel.c / mywheel_60_100.out: independent wheel search; reproduces all 41 new values k=60..100.
- stats.*: out-of-sample and fit statistics. constants.py / bigS.py: C, c2 and S(k) ratios; no output was saved for
  these. The same quantities are recomputed, with output, in ../../code/S_checks.py -> ../../data/S_checks.txt.
