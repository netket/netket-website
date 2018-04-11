---
title: Transverse-field Ising model
permalink: /docs/ising/
---

The transverse-field Ising model is one of the first things you should look at in order to acquaint yourself with NetKet.

It is a very instructive example to see how a basic NQS simulation is set up, and also to understand the several parameters controlling both the machine and the learning part.
The Hamiltonian of this model reads:  

$$
\mathcal{H}=-h\sum_{l}\sigma_{l}^{x} -J \sum_{\langle l,m \rangle}\sigma_{l}^{z}\sigma_{m}^{z},
$$

where the interaction terms runs over pairs of nearest-neighbors on a given graph. In `Examples/Ising1d/` this model is studied in the case of a one-dimensional lattice with periodic boundary conditions.


## Input file
The Python script `ising1d.py` can be used to set up the JSON input file for the NetKet executable. In the following we go through this script step by step, explaining the several fields.

### Defining the lattice
In this section of the input we specify the graph on which our spins live.

```python
pars['Graph']={
    'Name'           : 'Hypercube',
    'L'              : 20,
    'Dimension'      : 1 ,
    'Pbc'            : True,
}
```

The name of the parameters should be self-explanatory, for example here we are taking a `Hypercube` in one `Dimension` with periodic boundaries (`Pbc`) and with a linear extent of `L` 20 sites.
If you wanted to study instead a $$ L \times L $$ square lattice, you'd just set  `Dimension : 2`.
In this first release of NetKet only Hypercube geometries can be specified, however full support for arbitrary graphs will be added in the next releases (see also open Tasks).


### Defining the Hamiltonian
Next, we specify the Hamiltonian we want to simulate.

```python
pars['Hamiltonian']={
    'Name'           : 'Ising',
    'h'              : 1.0,
}
```

Here we specify again the name of the Hamiltonian and also the fact the we want to study the model at the critical point, i.e. for transverse field $$ h=1 $$.
If you would like to find out what other parameters you can pass to this Hamiltonian, you can have a look at `Hamiltonian/ising.hh`.
You will see that the JSON constructor in this case also takes the parameter `J` (the longitudinal interaction) which if not specified has a default value of 1.0.

```c++
Ising(const G & graph,const json & pars):
  nspins_(graph.Nsites()),
  h_(FieldVal(pars["Hamiltonian"],"h")),
  J_(FieldOrDefaultVal(pars["Hamiltonian"],"J",1.0)),
  graph_(graph){

  Init();
}
```

### Defining the Machine
In this section of the input we specify what wave function ansatz we wish to use. Here, we take a Restricted Boltzmann Machine `RbmSpin` with spin $ 1/2 $ hidden units.
To further use this machine we must also specify the number of hidden units we want to have. This can be done either setting `Nhidden`, or alternatively setting `Alpha`, where
$ \alpha = N_{\mathrm{hidden}}/N_{\mathrm{visible}} $, as done in the example input.

```python
pars['Machine']={
    'Name'           : 'RbmSpin',
    'Alpha'          : 1.0,
}
```


### Defining the Sampling scheme
Another crucial ingredient for the learning part is the Markov-Chain Monte Carlo scheme used for sampling. Here, we consider a local Metropolis sampler (see XXX for a description of the available samplers).

```python
pars['Sampler']={
    'Name'           : 'MetropolisLocal',
}
```
In general, choosing a good sampling scheme is crucial to guarantee that the quantum expectation values over the variational states are computed with a small autocorrelation time (see XXX for a description of the statistical analysis performed by NetKet).

### Defining the Learning scheme
Finally, we must specify what learning algorithm we wish to use. Together with the choice of the machine, this is the most important part of the simulation.
The method of choice in NetKet is the Stochastic Reconfiguration `Sr`, developed by S. Sorella and coworkers. For an introduction to this method, you can have a look at the book (1).
The code snippet defining the learning methods is:

```python
pars['Learning']={
    'Method'         : 'Sr',
    'Nsamples'       : 1.0e3,
    'NiterOpt'       : 500,
    'Diagshift'      : 0.1,
    'UseIterative'   : False,
    'OutputFile'     : "test",
    'StepperType'    : 'Sgd',
    'LearningRate'   : 0.1,
}
```
Also, notice that we need to specify a stepper.

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| *Method* | `Sr` : The Stochastic reconfiguration method |  The chosen method to learn the parameters of the wave-function  | `Sr` |
| *Nsamples* | Integer value | How many Markov Chain Monte Carlo samples should be performed at each step of the optimization | None |
| *OutputFile* | A string | The prefix for the output files (the output is then stored in chosen_prefix.log) | None |
| *StepperType* | One of the Steppers XXX | *Stepper* updates the parameters using the gradient information provided by *Method* | None |
| *UseIterative* | Boolean | Wheter to use the iterative solver in the Sr method (this is extremely useful when the number of parameters to optimize is very large) | False |
|===




## References
---------------
1. [Becca, F., & Sorella, S. (2017). Quantum Monte Carlo Approaches for Correlated Systems. Cambridge University Press.](https://doi.org/10.1017/9781316417041)
