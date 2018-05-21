---
title: Requirements
permalink: /getstarted/requirements/
---

NetKet is a light-weight framework with minimal dependencies on external libraries.
Dependencies are discussed below, together with common strategies to install them on your machine.
In a nutshell, the only strict requirement is `CMake` and a working `MPI` installation, whereas other external libraries
ship already with NetKet, substantially reducing the installation burden.

<h2 class="bg-primary">CMake and MPI</h2>
In order to install NetKet you need to have a working C++11 compiler installed on your computer.
NetKet relies on [CMake](https://cmake.org) to build, and test the library,
as well as on [MPI](https://en.wikipedia.org/wiki/Message_Passing_Interface) to provide seamless parallelism on multiples computing cores.

Below you can find more detailed, platform-dependent steps to install those requirements.

### Mac

On Mac Os, one of the simplest strategy to get `CMake` and `MPI` is to first get [https://brew.sh](https://brew.sh) and then either do:

```shell
brew install cmake open-mpi
```
to get [Open MPI](https://www.open-mpi.org), or if you prefer [MPICH](https://www.mpich.org) :

```shell
brew install cmake mpich
```

### Ubuntu

On Ubuntu you can get [CMake](https://cmake.org), [Open MPI](https://www.open-mpi.org) and the needed development headers doing:

```shell
sudo apt-get install cmake libopenmpi-dev openmpi-bin openmpi-doc
```

Alternatively, you can have [CMake](https://cmake.org) and [MPICH](https://www.mpich.org):

```shell
sudo apt-get install cmake libmpich-dev mpich
```
### Other platforms
On other platforms/Linux distributions, it is fairly easy to find pre-compiled packages, for example you can have a look at these installation guidelines: [CMake](https://cmake.org/download/), [MPICH](http://www.mpich.org/downloads/).

<h2 class="bg-primary">Other Libraries</h2>
NetKet also relies on a few header-only external libraries:

1. [Eigen](eigen.tuxfamily.org/), one of the best modern C++ library for linear algebra and matrix manipulation
2. [JSON for modern C++](https://github.com/nlohmann/json), an excellent light-weight library to handle JSON input/output and serialization/deserialization
3. [Catch 2](https://github.com/catchorg/Catch2), a great library for unit testing

For your convenience, those three libraries are already included in NetKet, in the `External/` folder, and you don't need to take further action to download/install them.
If you wanted to use another version of the external libraries, you can always link them to your project when compiling NetKet. To do so, please have a look at the variables
defined in `CMakelists.txt`. 


<h2 class="bg-primary">Python Libraries</h2>

NetKet relies on Python for input operations. Also, it is suggested to have [matplotlib](https://matplotlib.org) installed, to fully enjoy our Tutorials.

Most modern operating systems come with Python pre-installed, whereas you can find detailed instructions on how to install matplotlib [here](https://matplotlib.org/users/installing.html).
