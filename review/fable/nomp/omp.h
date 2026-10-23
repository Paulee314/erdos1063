/* Empty stand-in for omp.h: Apple clang has no OpenMP, so the pragmas are ignored and each process runs
 * single-threaded. Parallelism comes from running many processes on disjoint [lo,hi) chunks (crosscheck_fable.sh). */
