---
title: Requirements
permalink: /docs/requirements/
---

NetKet is a light-weight framework with minimal dependencies on external libraries.
Dependencies are discussed below, together with common strategies to install them on your machine.
In a nutshell, the only strict requirement is a working MPI installation, whereas other external libraries
ship already with NetKet, substantially reducing the installation burden.

<h2 class="bg-primary">MPI</h2>
NetKet relies on [MPI](https://en.wikipedia.org/wiki/Message_Passing_Interface) to provide seamless parallelism on multiples computing cores.
In order to install NetKet you need to have a working MPI/C++11 compiler installed on your computer.
Once those steps are completed, you will get an MPI compiler `mpicxx` ready for use, as well as the development libraries included with your MPI distribution of choice.

### Mac

On Mac Os, one of the simplest strategy to get MPI is to first get [https://brew.sh](https://brew.sh) and then either do:

```shell
brew install open-mpi
```
to get [Open MPI](https://www.open-mpi.org), or if you prefer [MPICH](https://www.mpich.org):

```shell
brew install mpich
```

### Ubuntu

On Ubuntu you can get [Open MPI](https://www.open-mpi.org) and the needed development headers doing:

```shell
sudo apt-get install libopenmpi-dev openmpi-bin openmpi-doc
```

to get [Open MPI](https://www.open-mpi.org), or if you prefer [MPICH](https://www.mpich.org):

```shell
sudo apt-get install libmpich-dev mpich
```
### Other platforms
On other platforms/Linux distributions, it is fairly easy to find pre-compiled packages, for example you can have a look at this [MPICH](http://www.mpich.org/downloads/)
installation guide.

<h2 class="bg-primary">Other Libraries</h2>
NetKet also relies on two header-only external libraries:

1. [Eigen](eigen.tuxfamily.org/), one of the best modern C++ library for linear algebra and matrix manipulation
2. [JSON for modern C++](https://github.com/nlohmann/json), an excellent light-weight library to handle JSON input/output and serialization/deserialization

For your convenience, those two libraries are already included in NetKet, in the `External/` folder, and you don't need to take further action to download/install them.
If you wanted to use another version of the external libraries, you can always link them to your project when compiling NetKet.  


<h2 class="bg-primary">Python Libraries</h2>

NetKet relies on Python for input operations. Also, it is suggested to have [matplotlib](https://matplotlib.org) installed, to fully enjoy our Tutorials.

Most modern operating systems come with Python pre-installed, whereas you can find detailed instructions on how to install matplotlib [here](https://matplotlib.org/users/installing.html). 
