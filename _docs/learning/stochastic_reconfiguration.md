---
title: Learning the Ground State
permalink: /docs/stochastic_reconfiguration/
---

NetKet implements learning algorithms to find the ground-state of a given many-body quantum Hamiltonian $$ \mathcal{H} $$.
Here, given a wave-function $$ \Psi $$ depending on a set of variational parameters $$ \mathbf{p} = p_1 \dots p_m $$ the goal is to minimize
the expectation value of the Hamiltonian:

$$
E(\mathbf{p}) = \frac{\langle\Psi|\mathcal{H}|\Psi\rangle}{\langle\Psi|\Psi\rangle}.
$$

In NetKet, $$ E(\mathbf{p}) $$ is computed by means of stochastic estimates, and it is also minimized using stochastic estimates of its gradient $$ \nabla_{\mathbf{p}}E(\mathbf{p}) $$.
Further details can be found in the References (1-3) listed below.

Given the estimates of $$ E(\mathbf{p}) $$ and $$ \nabla_{\mathbf{p}}E(\mathbf{p}) $$, there are different methods to update the network parameters $$ p_k $$ at each learning iteration.
Each of the different methods yield a direction $$ \Delta_k $$, such that the parameters are updated according to:

$$

p^\prime_k = p_k + \mathcal{S}_k(\Delta),

$$

where $$ \mathcal{S}_k(\Delta) $$ is the parameter update given by one of the chosen Optimizers.

<h2 class="bg-primary">Common Parameters</h2>

Independently of the specific optimization method chosen, you have to specify a set of parameters that controls general aspects of the learning.

In addition to the choice of the `Method`, another crucial control parameter is the number of samples used to estimate $$ E(\mathbf{p}) $$ and its gradient.
The number of samples is fixed by the field `Nsamples`, which sets the number of sweeps that the `Sampler` should perform to sample from the probability distribution:

$$
P(\mathbf{s}) = |\Psi(\mathbf{s}) | ^2.
$$

The user must also specify a suitable `Optimizer`, which ultimately yields the parameters updates in combination with the information given by `Method` through the vector $$ \Delta_k $$ as defined above.
More information about Optimizers is found [here](../optimizers).

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `Method` | `Sr` or `Gd` |  The chosen method to learn the parameters of the wave-function  | `Sr` |
| `NiterOpt` | Integer |  Number of optimization steps (*epochs* in the Machine Learning parlance)  | None |
| `Nsamples` | Integer | Number of Markov Chain Monte Carlo sweeps to be performed at each step of the optimization | None |
| `DiscardedSamples`| Integer | Number of sweeps to be discarded at the beginning of the sampling, at each step of the optimization | 10% of sweeps/CPU core |
| `DiscardedSamplesOnInit`| Integer | Number of sweeps to be discarded in the first step of optimization, at the beginning of the sampling | 0 |
| `OutputFile` | String | The prefix for the output files (the output is then stored in prefix.log, the wave-function saved in prefix.wf) | None |
| `SaveEvery` | Integer | The wave function is saved every `SaveEvery` optimization steps  | 50 |
|===

<h2 class="bg-primary">Gradient Descent</h2>

The simplest optimization method is the Gradient Descent, and is obtained when:

$$
\Delta_k=-\partial_{p_k} E(\mathbf{p}),
$$

where the gradient of the energy is estimated through

$$
\partial_{p_k} E(\mathbf{p}) = 2\mathrm{Re}\left[\left(E_{\mathrm{loc}}(\mathbf{x})-\langle\langle E_{\mathrm{loc}}\rangle\rangle\right)D_{k}^{\star}(\mathbf{x})\right]
$$

where $$ D_k(\mathbf{s})=\partial_{p_k} \log(\Psi(\mathbf{s})) $$ are the log-derivatives of the wave-function, and

$$
E_{\mathrm{Loc}}(\mathbf{s})=\frac{\langle\mathbf{s}| \mathcal{H} | \Psi \rangle}{\langle\mathbf{s}| \Psi \rangle}
$$

is the so-called *local energy*.

The expectation values above are computed stochastically, using samples from the probability distribution  $$ P(\mathbf{s}) = |\Psi(\mathbf{s}) | ^2 $$.
See References (2-3) for further details.

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| None | None |  None  | None |
|===

### Example
```python
pars['Learning']={
    'Method'         : 'Gd',
    'Nsamples'       : 1.0e3,
    'NiterOpt'       : 1000,
    'OutputFile'     : "test",
}
pars['Optimizer']={
    'Name'           : 'AdaMax',
}
```

<h2 class="bg-primary">Stochastic Reconfiguration</h2>

The method of choice in NetKet is the Stochastic Reconfiguration `Sr`, developed by S. Sorella and coworkers. For an introduction to this method, you can have a look at the book (1).
In a nutshell, the vector $$ \Delta $$ is found as a solution of the following linear system:

$$
\sum_{k^{\prime}} S_{kk^\prime} \Delta_{k^\prime} = - \langle E_{\mathrm{Loc}} D_k^\star \rangle + \langle E_{\mathrm{Loc}}\rangle \langle D_k^\star \rangle,
$$

where the hermitian (Gram) matrix reads:

$$
S_{kk^\prime}=\langle D_k^\star D_{k^\prime} \rangle - \langle D_k^\star \rangle \langle D_{k^\prime} \rangle.
$$

In most cases, it is necessary to regularize the $$ S $$ matrix, in order to have a well-conditioned solution and avoid numerical instabilities.
The regularization procedure implemented in NetKet is a simple diagonal shift:

$$
S_{kk^\prime} \rightarrow S_{kk^\prime} + \Lambda  \delta_{kk^\prime},
$$

where the parameter $$ \Lambda $$ is chosen by the user, through the field `DiagShift`.

The Stochastic Reconfiguration is typically a more robust method than the simple Gradient Descent, however its computational cost
is at least quadratic in the number of parameter to be optimized, at variance with the linear cost of the Gradient Descent. In order to reduce the computational burden, NetKet implements
an iterative Conjugate Gradient solver to find $$ \Delta_{k} $$ without ever forming the $$ S $$ matrix (which is the computational bottleneck of the algorithm).
The iterative solver can be activated with the flag `UseIterative`, and should be used when optimizing a very large number of parameters $$ \gtrapprox 1000 $$.

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `DiagShift` | Double | The regularization parameter $$ \Lambda $$ for the Sr method | 0.01 |
| `UseIterative` | Boolean | Whether to use the iterative solver in the Sr method (this is extremely useful when the number of parameters to optimize is very large) | False |
|===

### Example
```python
pars['Learning']={
    'Method'         : 'Sr',
    'Nsamples'       : 1.0e3,
    'NiterOpt'       : 500,
    'Diagshift'      : 0.1,
    'UseIterative'   : False,
    'OutputFile'     : "test",
}

pars['Optimizer']={
    'Name'           : 'Sgd',
    'LearningRate'   : 0.1,
}
```





## References
---------------
1. [Becca, F., & Sorella, S. (2017). Quantum Monte Carlo Approaches for Correlated Systems. Cambridge University Press.](https://doi.org/10.1017/9781316417041)
2. [Carleo, G., & Troyer, M. (2017). Solving the quantum many-body problem with artificial neural networks. Science, 355 602](http://science.sciencemag.org/content/355/6325/602)
3. [Carleo, G. (2017). Lecture notes for the Advanced School on Quantum Science and Quantum technology.](https://gitlab.com/nqs/ictp_school/blob/7ff4fcc22a1685fec0972f291919090c79586012/notes.pdf)
