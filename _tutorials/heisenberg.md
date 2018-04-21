---
title: Antiferromagnetic Heisenberg model
permalink: /tutorials/heisenberg/
description: Learn how to define conserved quantities, use Hamiltonian samplers, look at the energy variance, and more.
---

When you first get started with NetKet, it is also very instructive to look at the antiferromagnetic Heisenberg model,

$$
\mathcal{H}=J\sum_{i,j} \left(\sigma_{i}^{x}\sigma_{j}^{x}+\sigma_{i}^{y}\sigma_{j}^{y}+\sigma_{i}^{z}\sigma_{j}^{z}\right),
$$

where in this tutorial the exchange terms run over pairs of nearest-neighbors on lattice.

In `Tutorials/Heisenberg1d/` this model is studied in the case of a one-dimensional lattice with periodic boundary conditions.


## Input file
The Python script `heisenberg1d.py` can be used to set up the JSON input file for the NetKet executable. In the following we go through this script step by step, explaining the several fields.

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
    'Name'           : 'Heisenberg',
    'TotalSz'        : 0,
}
```

Here we specify the name of the Hamiltonian,
picking one of the [Built-in Hamiltonians]({{ site.baseurl }}{% link _docs/hamiltonians/hardcoded_hamiltonians.md %}). Notice that here we are also specifying that we want the ground-state
in the sector with total $$ \sigma^z =0 $$.

Finally notice that NetKet allows to define custom Hamiltonians, simply working at the level of input files, as explained [here]({{ site.baseurl }}{% link _docs/hamiltonians/custom_hamiltonians.md %}).



### Defining the Machine
In this section of the input we specify what wave function ansatz we wish to use. Here, we take a Restricted Boltzmann Machine `RbmSpinSymm` with spin $$ 1/2 $$ hidden units
and permutation symmetry (see Ref. 1 for further details).
Since we are working with a translation-invariant Hamiltonian, and we are interested in the $$ q=0 $$, zero momentum ground-state, this is a sensible choice.
To further use this machine we must also specify the number of hidden units we want to have.
In this machine we also must set `Alpha`, where $$ \alpha = N_{\mathrm{hidden}}/N_{\mathrm{visible}} $$, as done in the example input.

```python
pars['Machine']={
    'Name'           : 'RbmSpinSymm',
    'Alpha'          : 1.0,
}
```

Further details about the Restricted Boltzmann Machines and the other machines implemented in NetKet can be found [here]({{ site.baseurl }}{% link _docs/machines/rbm.md %}).

### Defining the Sampling scheme
Another crucial ingredient for the learning part is the Markov-Chain Monte Carlo scheme used for sampling. Here, we consider a Metropolis sampler implementing Hamiltonian moves
(see [here]({{ site.baseurl }}{% link _docs/sampling/metropolis_hamiltonian.md %}) for a description of this specific family of sampler).

```python
pars['Sampler']={
    'Name'           : 'MetropolisHamiltonian',
}
```
An important reason to chose this sampler in this case is that we want to make sure to preserve all the symmetries of the Hamiltonian during the sampling. Basically,
what the sampler does in this case is that it choses a pair of neighboring spins at random and proposes an exchange.

This is crucial for example if we want our specification ```'TotalSz'        : 0``` to be verified. If instead of Hamiltonian moves we chose local Metropolis moves, during the sampling our total magnetization would
fluctuate, thus violating the wanted constraint.

### Defining the Learning scheme
Finally, we must specify what learning algorithm we wish to use. Together with the choice of the machine, this is the most important part of the simulation.
The method of choice in NetKet is the Stochastic Reconfiguration `Sr`, developed by S. Sorella and coworkers. For an introduction to this method, you can have a look at the book (2).
The code snippet defining the learning methods is:

```python
pars['Learning']={
    'Method'         : 'Sr',
    'Nsamples'       : 1.0e3,
    'NiterOpt'       : 4000,
    'Diagshift'      : 0.1,
    'UseIterative'   : False,
    'OutputFile'     : 'test',
    'StepperType'    : 'AdaMax',
}
```
Also, notice that we need to specify a stepper, which in this case is AdaMax.
More details about the steppers can be found [here]({{ site.baseurl }}{% link _docs/learning/steppers.md %}),
whereas learning algorithms to find the ground state are discussed [here]({{ site.baseurl }}{% link _docs/learning/stochastic_reconfiguration.md %}).

## Running the simulation

Once you have finished preparing the input file in python, you can just run:

```shell
python heisenberg1d.py
```

this will generate a JSON file called `heisenberg1d.json` ready to be fed to the NetKet executable.
At this point then you can just run

```shell
./netket heisenberg1d.json
```

if you want to run your simulation on a single core, or

```shell
mpirun -n NP netket heisenberg1d.json
```
if you want to run your simulation on `NP` cores (changes NP to the number of cores you want to use).

At this point, the simulation will be running and log files will be generated in real time, until NetKet finishes its tasks.

## Output files

Since in the `Learning` section we have specified ```'OutputFile'     : "test"```, two output files will be generated with the "test" prefix, i.e.
`test.log`, a JSON file containing the results of the learning procedure as it advances, and `test.wf` containing backups of the optimized wave function.

For each iteration of the learning, the output log contains important information which can visually inspected just opening the file.


```json
"Energy":{"Mean":-35.627084266234725,"Sigma":0.005236470739979945,"Taucorr":0.016224299969381108}
```

For example, you can see here that we have the expectation value of the energy (`Mean`), its statistical error (`Sigma`), and an estimate of the
[autocorrelation time](https://en.wikipedia.org/wiki/Autocorrelation) (`Taucorr`). Apart from the `Energy`, the learning algorithm also records
the `EnergyVariance`, namely $$ \langle \mathcal{H}^2 \rangle - \langle\mathcal{H}\rangle^2 $$ which is smaller and smaller when converging to an exact eigenstate of the Hamiltonian.

If you want, you can also plot these results while the learning is running, just using the convenience script:

```shell
python plot_heisenberg.py
```

An example result is shown below, where you can see that the energy would converge to the exact result during the learning.
<br>

<img src="{{site.baseurl}}/img/heisenberg.png" class="img-fluid" alt="Responsive image" class="img-thumbnail">

<br>
<hr>

It is also interesting to look at the energy variance, to see how it is systematically reduced (by several orders of magnitude) during the learning.
An example plot is given below.
<br>

<img src="{{site.baseurl}}/img/heis_variance.png" class="img-fluid" alt="Responsive image" class="img-thumbnail">

## References
---------------
1. [Carleo, G., & Troyer, M. (2017). Solving the quantum many-body problem with artificial neural networks. Science, 355 602](http://science.sciencemag.org/content/355/6325/602)
2. [Becca, F., & Sorella, S. (2017). Quantum Monte Carlo Approaches for Correlated Systems. Cambridge University Press.](https://doi.org/10.1017/9781316417041)
