---
title: Requirements
permalink: /getstarted/requirements/
---

NetKet is a light-weight framework with minimal dependencies on external libraries.
Dependencies are discussed below, together with common strategies to install them on your machine.
In a nutshell, the only strict requirements are a working `MPI` C++ compiler, `CMake`, and a modern
Python interpreter.

<h2 class="bg-primary">MPI and CMake</h2>
In order to install NetKet you need to have a working C++11 compiler installed on your computer.
NetKet relies on [MPI](https://en.wikipedia.org/wiki/Message_Passing_Interface) to provide seamless parallelism on multiples computing cores.

Below you can find more detailed, platform-dependent steps to install those requirements.

### Mac

On Mac Os, one of the simplest strategy to get `MPI` and `CMake` is to first get [https://brew.sh](https://brew.sh) and then either do:

```shell
brew install cmake open-mpi
```
to get [Open MPI](https://www.open-mpi.org), or if you prefer [MPICH](https://www.mpich.org) :

```shell
brew install cmake mpich
```

### Ubuntu

On Ubuntu you can get [Open MPI](https://www.open-mpi.org) and the needed development headers doing:

```shell
sudo apt-get install cmake libopenmpi-dev openmpi-bin openmpi-doc
```

Alternatively, you can have [MPICH](https://www.mpich.org):

```shell
sudo apt-get install cmake libmpich-dev mpich
```
### Other platforms
On other platforms/Linux distributions, it is fairly easy to find pre-compiled packages, for example you can have a look at these installation guidelines: [CMake](https://cmake.org/download/), [MPICH](http://www.mpich.org/downloads/).


<h2 class="bg-primary">Optional Python Libraries</h2>

For some functionalities, NetKet relies on [numpy](http://www.numpy.org/).
It is also suggested to have [IPython][https://ipython.readthedocs.io/en/stable/],
and [matplotlib](https://matplotlib.org/) installed, to fully enjoy our Tutorials and Examples.

```shell
pip install numpy matplotlib jupyter
```

<h2 class="bg-primary">Other Dependencies</h2>
NetKet also relies on a few header-only external libraries:

1. [Eigen](eigen.tuxfamily.org/), one of the best modern C++ library for linear algebra and matrix manipulation
2. [Pybind11](https://pybind11.readthedocs.io/en/master/), a great library to create Python bindings of existing C++ code
3. [JSON for modern C++](https://github.com/nlohmann/json), an excellent light-weight library to handle JSON input/output and serialization/deserialization
4. [Catch 2](https://github.com/catchorg/Catch2), a great library for unit testing

For your convenience, those three libraries are already included in NetKet, and you don't need to take further action to download/install them.
If you wanted to use another version of the external libraries, you can always link them to your project when manually compiling NetKet. To do so, please have a look at the variables defined in `CMakelists.txt`.
