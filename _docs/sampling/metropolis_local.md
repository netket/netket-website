---
title: Local Moves
permalink: /docs/metropolis_local/
---

A central task in several learning applications is the ability to sample from a given machine.
For example, in the variational learning one samples quantum numbers $$ s_1\dots s_N $$
from the probability distribution given by the square modulus of the wave-function:

$$
P(s_1\dots s_N) = |\Psi(s_1\dots s_N) | ^2.
$$

NetKet implements several local [Metropolis-Hastings](https://en.wikipedia.org/wiki/Metropolis–Hastings_algorithm) moves.
The samplers describe below can be used for any quantum system with a local (and finite) discrete Hilbert space.

<h2 class="bg-primary">MetropolisLocal</h2>
This sampler acts locally only on one local degree of freedom $$ s_i $$, and proposes a new state: $$ s_1 \dots s^\prime_i \dots s_N $$,
where $$ s^\prime_i \neq s_i $$.

The transition probability associated to this sampler can be decomposed into two steps:

1. One of the site indices $$ i = 1\dots N $$ is chosen with uniform probability.  
2. Among all the possible ($$ m $$) values that $$ s_i $$ can take, one of them is chosen with uniform probability.

For example, in the case of spin $$ 1/2 $$ particles, $$ m=2 $$ and the possible local values are $$ s_i = -1,+1 $$.
In this case then `MetropolisLocal` is equivalent to flipping a random spin.

In the case of bosons, with occupation numbers $$ s_i = 0, 1, \dots n_{\mathrm{max}} $$, `MetropolisLocal` would pick a random local occupation number uniformly between $$ 0 $$ and $$ n_{\mathrm{max}} $$.  

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| None | None |  None | None |
|===

### Example
```python
pars['Sampler']={
    'Name'           : 'MetropolisLocal',
}
```

<h2 class="bg-primary">MetropolisLocalPt</h2>
This sampler performs [parallel-tempering](https://en.wikipedia.org/wiki/Parallel_tempering) moves, effectively sampling from the a set of probability distributions

$$
P_\beta(s_1\dots s_N) \equiv P^\beta(s_1\dots s_N),
$$

each associated to an inverse *temperature* $$ 1 \leq \beta_k \leq 0 $$. During the sampling, configurations at different
*temperatures* are exchanged, to increase ergodicity. Only quantum numbers sampled from $$ \beta =1 $$ (corresponding to the original probability distribution) are retained
to compute the required expectation values.

In this version of the algorithm, inverse temperatures are chosen according to the simple form $$ \beta_k = 1 - k/N_{\mathrm{rep}} $$,
where $$ N_{\mathrm{rep}} $$ is a user-supplied number specifying how many temperatures are to be taken.
Upon increasing the number of temperatures (or replicas, in the jargon) one can improve the sampling efficiency.

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `Nreplicas` | Integer |  The number of effective temperatures for parallel tempering, $$ N_{\mathrm{rep}} $$ | None |
|===

### Example
```python
pars['Sampler']={
    'Name'           : 'MetropolisLocalPt',
    'Nreplicas'           : 64,
}
```
