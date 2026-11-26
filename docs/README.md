# MATRO documentation

The installed solver is `matro.minimize`, implemented in `src/matro` and
identified as `matro-official-python-fullq-001`.

- [Solver API and numerical contract](../SOLVER.md): installation, input and
  output conventions, evaluation counting, and arithmetic backends.
- [Algorithm](algorithm.md): a short description of the quadratic model,
  metric construction, and spherical configuration.
- [Implementation](implementation.md): radius rules, coordinate changes,
  model storage, interpolation-factor reconstruction, and numerical checks.
- [Experimental protocol and reproduction](experiments.md): the fixed
  147-instance study, paired initialization, reference values, profiles,
  controlled anisotropy, and mechanism figures.

Use the [reproduction instructions](../reproduction/README.md) to rebuild
the manuscript tables and figures from the included data.
