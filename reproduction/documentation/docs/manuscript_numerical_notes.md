# Numerical representation and diagnostic records

These details were retained from the v13.8 implementation appendix when the
v14.1 manuscript was edited for mathematical exposition. The numerical method
and experimental records are unchanged.

The NEWUOA Hessian is represented as `B = B_Q + Z.T @ diag(p) @ Z`, with an
explicit symmetric part and implicit coefficients. After a metric transformation,
the transformed Hessian is stored explicitly, the implicit coefficients are set
to zero, and the values and best-point index are retained.

For the inverse interpolation factors in Appendix C, the NEWUOA arrays are
`ZMAT = V.T`, `IDZ = 1`; the first `q_n` rows of `BMAT` are the transposed
linear rows of `U`, and its last `n` rows are zero. Candidate arrays are built
before replacing the current state. Controller event timing and the original
state-variable conventions remain specified in [implementation.md](implementation.md).

Across 2940 benchmark runs, 542266 of 644748 nontrivial metric proposals passed
the numerical checks (84.11 percent). Most rejections arose from the condition
number of the transformed design matrix or the existing-model residual.
The complete diagnostic summary and its verifier remain in the compact data
and reviews directories. These diagnostic counts are not additional optimizer runs.
