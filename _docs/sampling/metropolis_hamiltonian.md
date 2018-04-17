---
title: Hamiltonian Moves
permalink: /docs/metropolis_hamiltonian/
---

<h2 class="bg-primary">MetropolisHamiltonian</h2>

NetKet implements sampling based on the off-diagonal elements of the [Hamiltonian](../hamiltonian/).
In this case, the transition matrix is taken to be:

$$
T( \mathbf{s} \rightarrow \mathbf{s}^\prime) = \frac{1}{\mathcal{N}(\mathbf{s})}\theta(|H_{\mathbf{s},\mathbf{s}^\prime}|),
$$   

where $$ \theta(x) $$ is the Heaviside step function, and $$ \mathcal{N}(\mathbf{s}) $$ is a state-dependent normalization. The effect of this transition probability is then to connect (with uniform probability) a given state $$ \mathbf{s} $$ to all those states $$ \mathbf{s}^\prime $$ for which the Hamiltonian has finite matrix elements.
Notice that this sampler preserves by construction all the symmetries of the Hamiltonian. This is in general not true for
the [local samplers](../metropolis_local/).

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| None | None |  None | None |
|===

### Example
```python
pars['Sampler']={
    'Name'           : 'MetropolisHamiltonian',
}
```

<h2 class="bg-primary">MetropolisHamiltonianPt</h2>

This sampler performs [parallel-tempering](https://en.wikipedia.org/wiki/Parallel_tempering) moves in addition to
the local moves implemented in `MetropolisHamiltonian`. The number of replicas can be $$ N_{\mathrm{rep}} $$ chosen by the user.

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `Nreplicas` | Integer |  The number of effective temperatures for parallel tempering, $$ N_{\mathrm{rep}} $$ | None |
|===

### Example
```python
pars['Sampler']={
    'Name'           : 'MetropolisHamiltonianPt',
    'Nreplicas'           : 64,
}
```
