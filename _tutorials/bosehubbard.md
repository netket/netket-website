---
title: Bose-Hubbard model
permalink: /tutorials/bosehubbard/
description: Learn how to deal with bosons, use a symmetric Restricted Boltzmanm machine, and more.
---

NetKet can be applied also to bosonic systems. To get acquainted with this kind of calculations,
you can have a look at the tutorial on the one-dimensional Bose-Hubbard model, in
`Tutorials/BoseHubbard1d`.

There, we study the Hamiltonian

$$
\mathcal{H}= -J \sum_{i,j} b^{\dagger}_i b_j + \frac{U}{2} \sum_i n_i(n_i-1),
$$

where the hopping term runs over pairs of nearest-neighbors on the one-dimensional lattice.

The steps to be followed are very similar to the spin Hamiltonians we have seen so far, but
for completeness we repeat them here.


## Input file
The Python script `bosehubbard1d.py` can be used to set up the JSON input file for the NetKet executable. In the following we go through this script step by step, explaining the several fields.

### Defining the lattice
In this section of the input we specify the graph on which our spins live.

```python
pars['Graph']={
    'Name'           : 'Hypercube',
    'L'              : 12,
    'Dimension'      : 1 ,
    'Pbc'            : True,
}
```

The name of the parameters should be self-explanatory, for example here we are taking a `Hypercube` in one `Dimension` with periodic boundaries (`Pbc`) and with a linear extent of `L` 12 sites.
If you wanted to study instead a $$ L \times L $$ square lattice, you would just set  `Dimension : 2`.

Apart from [Built-in Graphs]({{ site.baseurl }}{% link _docs/graphs/hardcoded_graphs.md %}) (such as the Hypercube),
you can easily specify virtually any other custom graph, as explained [here]({{ site.baseurl }}{% link _docs/graphs/custom_graphs.md %}).


### Defining the Hamiltonian
Next, we specify the Hamiltonian we want to simulate.

```python
pars['Hamiltonian']={
    'Name'           : 'BoseHubbard',
    'U'              : 4.0,
    'Nmax'           : 3,
    'Nbosons'        : 12,
}
```

Here we specify the name of the Hamiltonian and also the fact the we want to study,
picking one of the [Built-in Hamiltonians]({{ site.baseurl }}{% link _docs/hamiltonians/hardcoded_hamiltonians.md %}).
Notice that here we specify the maximum number of bosons allowed per site (with the field `Nmax`) and also specify that we want the ground-state
in the sector with total number of particles fixed, in this specific case we work at unit filling, i.e. $$N_{\mathrm{bosons}} = L $$.

Further notice that NetKet allows to define custom Hamiltonians, simply working at the level of input files, as explained
[here]({{ site.baseurl }}{% link _docs/hamiltonians/custom_hamiltonians.md %}).



### Defining the Machine
In this section of the input we specify what wave function ansatz we wish to use. Here, we take a Restricted Boltzmann Machine `RbmSpinSymm` with spin $$ 1/2 $$ hidden units
and permutation symmetry. Since we are working with a translation-invariant Hamiltonian, and we are interested in the $$ q=0 $$, zero momentum ground-state, this is a sensible choice.
To further use this machine we must also specify the number of hidden units we want to have.
In this machine we also must set `Alpha`, where $$ \alpha = N_{\mathrm{hidden}}/N_{\mathrm{visible}} $$, as done in the example input.

```python
pars['Machine']={
    'Name'           : 'RbmSpinSymm',
    'Alpha'          : 4.0,
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
what the sampler does in this case is that it choses a pair of neighboring spins at random and proposes an hopping of particles, if allowed.

This is crucial for example if we want our specification ```'Nbosons'        : 12``` to be verified at all times during the sampling.
If instead of Hamiltonian moves we chose local Metropolis moves, during the sampling our total number of particles would
fluctuate, thus violating the wanted constraint. In that case however you can specify a chemical potential to control the average number of particles.

### Defining the Learning scheme
Finally, we must specify what learning algorithm we wish to use. Together with the choice of the machine, this is the most important part of the simulation.
The method of choice in NetKet is the Stochastic Reconfiguration `Sr`, developed by S. Sorella and coworkers. For an introduction to this method, you can have a look at the book (2).
The code snippet defining the learning methods is:

```python
pars['Learning']={
    'Method'         : 'Sr',
    'Nsamples'       : 1.0e3,
    'NiterOpt'       : 4000,
    'Diagshift'      : 5.0e-3,
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
python bosehubbard1d.py
```

this will generate a JSON file called `bosehubbard1d.json` ready to be fed to the NetKet executable.
At this point then you can just run

```shell
netket bosehubbard1d.json
```

if you want to run your simulation on a single core, or

```shell
mpirun -n NP netket bosehubbard1d.json
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
python plot_bose.py
```

An example result is shown below, where you can see that the energy would converge to the exact result during the learning.
<br>

<img src="{{site.baseurl}}/img/bosehubbard.png" class="img-fluid" alt="Responsive image" class="img-thumbnail">

It is also an interesting exercise to compare the accuracy on the energies obtained here with the Restricted Boltzmann machine with the accuracy obtained with Feed-Forward neural networks
on the same system, for example in Reference (3).

## References
---------------
1. [Carleo, G., & Troyer, M. (2017). Solving the quantum many-body problem with artificial neural networks. Science, 355 602](http://science.sciencemag.org/content/355/6325/602)
2. [Becca, F., & Sorella, S. (2017). Quantum Monte Carlo Approaches for Correlated Systems. Cambridge University Press.](https://doi.org/10.1017/9781316417041)
3. [Saito, H., & Kato, M. (2018). Machine learning technique to find quantum many-body ground states of bosons on a lattice. J. Phys. Soc. Jpn. 87, 014001](https://arxiv.org/pdf/1709.05468v1.pdf)
