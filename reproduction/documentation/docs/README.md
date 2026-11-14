# MATRO documentation

These documents accompany manuscript v14.1. The solver maintained in the
Research/matro repository exposes `matro.minimize`, is implemented in
`src/matro`, and is identified as `matro-official-python-fullq-001`.
Source paths in the implementation reference are relative to that repository
root. The manuscript source archive supplies the documents and compact evidence;
the installation instructions use the Research/matro source tree.

- [Solver API and numerical contract](../SOLVER.md): installation, input and
  output conventions, evaluation counting, and arithmetic backends.
- [Algorithm](algorithm.md): a short description of the quadratic model,
  metric construction, and spherical configuration.
- [Implementation](implementation.md): radius rules, coordinate changes,
  model storage, interpolation-factor reconstruction, and numerical checks.
- [Experimental protocol and reproduction](experiments.md): the fixed
  147-instance study, paired initialization, reference values, profiles,
  controlled anisotropy, and mechanism figures.

The experimental documentation identifies the compact evidence in the
manuscript archive's `data/` and `statistics/` directories, used to reproduce
the current tables and figures. The legacy
`codes/` experiment scripts concern earlier studies. The mathematical results
and their complete proofs are retained in the manuscript and its appendix.
