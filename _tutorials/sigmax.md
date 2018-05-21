---
title: Measuring custom observables
permalink: /tutorials/sigmax/
description: Learn how to define a custom observable, analyze the output, and more.
---

In this tutorial we show how to define a custom [Observable]({{ site.baseurl }}{% link _docs/observables/custom_observables.md %}), and see the results during the learning
procedure. Here, we take again the transverse-field Ising model as an example:

$$
\mathcal{H}=-h\sum_{l}\sigma_{l}^{x} -J \sum_{\langle l,m \rangle}\sigma_{l}^{z}\sigma_{m}^{z},
$$

where the interaction term runs over pairs of nearest-neighbors on a given graph. In `Tutorials/Observables/` this model is studied in the case of a one-dimensional lattice with periodic boundary conditions.


## Input file
The Python script `sigmax.py` can be used to set up the JSON input file for the NetKet executable. The definition of the `Graph`, `Hamiltonian`, `Learning`, etc., closely follow those discussed
in the tutorial on the transverse-field Ising model. We do not discuss those in detail here, but focus instead on the relevant part concerning observables.

### Defining the observable
In this section of the input we specify what observable we want to measure. In this example, we choose the total transverse-field:

$$
\mathcal{O}=\sum_{l}\sigma_{l}^{x},
$$

thus the relevant [local operator]({{ site.baseurl }}{% link _docs/observables/custom_observables.md %}) is just $$ \sigma_{l}^x $$:

$$
o_l = \left(\begin{array}{cc}
0 & 1\\
1 & 0
\end{array}\right)
$$

and it is easily declared in the input file

```python
sigmaxop=[]
sites=[]
for i in range(L):
    #\sum_i sigma^x(i)
    sigmaxop.append([[0,1],[1,0]])
    sites.append([i])

pars['Observables']={
    'Operators'      : sigmaxop,
    'ActingOn'       : sites,
    'Name'           : 'SigmaX',
}
```

Notice that if you wanted to measure more than a single custom observable, you can simply make the `Observables` section a vector, each containing the `Name`,`Operators`,`ActingOn` specifications
for each of the needed observables.



## Running the simulation

Once you have finished preparing the input file in python, you can just run:

```shell
python sigmax.py
```

this will generate a JSON file called `sigmax.json` ready to be fed to the NetKet executable.
At this point then you can just run

```shell
netket sigmax.json
```

if you want to run your simulation on a single core, or

```shell
mpirun -n NP netket sigmax.json
```
if you want to run your simulation on `NP` cores (changes NP to the number of cores you want to use).

At this point, the simulation will be running and log files will be continuously updated, until NetKet finishes its tasks.

## Output files

Since in the `Learning` section we have specified ```'OutputFile'     : "test"```, two output files will be generated with the "test" prefix, i.e.
`test.log`, a JSON file containing the results of the learning procedure as it advances, and `test.wf` containing backups of the optimized wave function.

For each iteration of the learning, the output log contains important information which can visually inspected just opening the file.
Most importantly, it will contain information about our custom Observable:

```json
"SigmaX":{"Mean":14.34106514693015,"Sigma":0.20268003276971638,"Taucorr":0.718576491136981}
```

For example, you can see here that we have its expectation value (`Mean`), its statistical error (`Sigma`), and an estimate of the
[autocorrelation time](https://en.wikipedia.org/wiki/Autocorrelation) (`Taucorr`).

If you want, you can also plot these results while the learning is running, just using the convenience script:

```shell
python plot_ising.py
```

An example result is shown below, where you can see that the energy would converge to the exact result during the learning.

It is instructive to notice that statistical errors on general observables can be significantly larger than statistical errors on the `Hamiltonian`. This is due to the fact that the specific
observable used to measure the expectation value of the `Hamiltonian`, which is called the "local energy", has a special zero-variance property which other observables do not have.
See for example (1-2) for further information.

<br>

<img src="{{site.baseurl}}/img/ising_sigmax.png" class="img-fluid" alt="Responsive image" class="img-thumbnail">

## References
---------------
1. [Becca, F., & Sorella, S. (2017). Quantum Monte Carlo Approaches for Correlated Systems. Cambridge University Press.](https://doi.org/10.1017/9781316417041)
2. [Carleo, G. (2017). Lecture notes for the Advanced School on Quantum Science and Quantum technology.](https://gitlab.com/nqs/ictp_school/blob/7ff4fcc22a1685fec0972f291919090c79586012/notes.pdf)
