---
title: Compiling
permalink: /docs/compiling/
---

In the main folder, look for the file `Makefile` and edit the following two lines according to your system configuration.
```
CXX           = mpicxx

EIGEN_INCLUDE = /usr/local/include/eigen3/

```

I.e. substitute `mpicxx` with your mpi compiler, and `/usr/local/include/eigen3/` with the directory containing the headers for the Eigen library.
Once you are done, just type `make` in the command line. This will generate the executable `netket.o`.
