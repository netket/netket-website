---
title: Transverse-field Ising model
permalink: /tutorials/ising/
description: Learn how to set up a simulation, define common input parameters, analyze the output, and more.
---

The transverse-field Ising model is one of the first things you should look at in order to acquaint yourself with NetKet.

It is a very instructive example to see how a basic NQS simulation is set up, and also to understand the several parameters controlling both the machine and the learning part.
The Hamiltonian of this model reads:  

$$
\mathcal{H}=-h\sum_{l}\sigma_{l}^{x} -J \sum_{\langle l,m \rangle}\sigma_{l}^{z}\sigma_{m}^{z},
$$

where the interaction terms runs over pairs of nearest-neighbors on a given graph. In `Tutorials/Ising1d/` this model is studied in the case of a one-dimensional lattice with periodic boundary conditions.


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
If you wanted to study instead a $$ L \times L $$ square lattice, you would just set  `Dimension : 2`.

Apart from [Built-in Graphs]({{ site.baseurl }}{% link _docs/graphs/hardcoded_graphs.md %}) (such as the Hypercube),
you can easily specify virtually any other custom graph, as explained [here]({{ site.baseurl }}{% link _docs/graphs/custom_graphs.md %}).


### Defining the Hamiltonian
Next, we specify the Hamiltonian we want to simulate.

```python
pars['Hamiltonian']={
    'Name'           : 'Ising',
    'h'              : 1.0,
}
```

Here we specify the name of the Hamiltonian and also the fact the we want to study the model at the critical point, i.e. for transverse field $$ h=1 $$.
If you would like to find out what other parameters you can pass to this Hamiltonian,
you can have a look at the section on [Built-in Hamiltonians]({{ site.baseurl }}{% link _docs/hamiltonians/hardcoded_hamiltonians.md %}).

NetKet also allows to define custom Hamiltonians, simply working at the level of input files, as explained [here]({{ site.baseurl }}{% link _docs/hamiltonians/custom_hamiltonians.md %}).

### Defining the Machine
In this section of the input we specify what wave function ansatz we wish to use. Here, we take a Restricted Boltzmann Machine `RbmSpin` with spin $$ 1/2 $$ hidden units.
To further use this machine we must also specify the number of hidden units we want to have. This can be done either setting `Nhidden`,
or alternatively setting the hidden unit density `Alpha`, where $$ \alpha = N_{\mathrm{hidden}}/N_{\mathrm{visible}} $$, as done in the example input.

```python
pars['Machine']={
    'Name'           : 'RbmSpin',
    'Alpha'          : 1.0,
}
```

Further details about the Restricted Boltzmann Machines and the other machines implemented in NetKet can be found [here]({{ site.baseurl }}{% link _docs/machines/rbm.md %}).

### Defining the Sampling scheme
Another crucial ingredient for the learning part is the Markov-Chain Monte Carlo scheme used for sampling. Here, we consider a local Metropolis sampler
(see [here]({{ site.baseurl }}{% link _docs/sampling/introduction.md %}) for a description of the available samplers).

```python
pars['Sampler']={
    'Name'           : 'MetropolisLocal',
}
```
In general, choosing a good sampling scheme is crucial to guarantee that the quantum expectation values over the variational states are computed with a small autocorrelation time.

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
Also, notice that we need to specify a stepper, which in this case is a simple Stochastic Gradient Descent (Sgd).
More details about the steppers can be found [here]({{ site.baseurl }}{% link _docs/learning/steppers.md %}),
whereas learning algorithms to find the ground state are discussed [here]({{ site.baseurl }}{% link _docs/learning/stochastic_reconfiguration.md %}).

## Running the simulation

Once you have finished preparing the input file in python, you can just run:

```shell
python ising1d.py
```

this will generate a JSON file called `ising1d.json` ready to be fed to the NetKet executable.
At this point then you can just run

```shell
./netket ising1d.json
```

if you want to run your simulation on a single core, or

```shell
mpirun -n NP netket ising1d.json
```
if you want to run your simulation on `NP` cores (changes NP to the number of cores you want to use).

At this point, the simulation will be running and log files will be generated in real time, until NetKet finishes its tasks.

## Output files

Since in the `Learning` section we have specified ```'OutputFile'     : "test"```, two output files will be generated with the "test" prefix, i.e.
`test.log`, a JSON file containing the results of the learning procedure as it advances, and `test.wf` containing backups of the optimized wave function.

For each iteration of the learning, the output log contains important information which can visually inspected just opening the file.


```json
"Energy":{"Mean":-14.817586644611739,"Sigma":0.1613372500177537,"Taucorr":0.012691835598671597}
```

For example, you can see here that we have the expectation value of the energy (`Mean`), its statistical error (`Sigma`), and an estimate of the
[autocorrelation time](https://en.wikipedia.org/wiki/Autocorrelation) (`Taucorr`). Apart from the `Energy`, the learning algorithm also records
the `EnergyVariance`, namely $$ \langle \mathcal{H}^2 \rangle - \langle\mathcal{H}\rangle^2 $$ which is smaller and smaller when converging to an exact eigenstate of the Hamiltonian.

If you want, you can also plot these results while the learning is running, just using the convenience script:

```shell
python plot_ising.py
```

An example result is shown below, where you can see that the energy would converge to the exact result during the learning.

<br>

<img src="{{site.baseurl}}/img/ising.png" class="img-fluid" alt="Responsive image" class="img-thumbnail">

## References
---------------
1. [Becca, F., & Sorella, S. (2017). Quantum Monte Carlo Approaches for Correlated Systems. Cambridge University Press.](https://doi.org/10.1017/9781316417041)
