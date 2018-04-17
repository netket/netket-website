---
title: Local Moves
permalink: /docs/metropolis_local/
---

Local samplers propose to modify only a limited set of quantum numbers at the time.
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
This sampler performs [parallel-tempering](https://en.wikipedia.org/wiki/Parallel_tempering) moves in addition to
the local moves implemented in `MetropolisLocal`. The number of replicas can be $$ N_{\mathrm{rep}} $$ chosen by the user. 

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
