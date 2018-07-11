---
title: Custom Samplers
permalink: /docs/custom_sampling/
---
NetKet provides the freedom to define user’s own samplers, by specifying the relevant move operators in the `Sampler` section of the input. For the moment, this functionality is limited to move operators which are sums of $$k$$-local move operators:

$$
\mathcal{M}= \sum_i M_i
$$

where the move operators $$ M_i $$ act on an (arbitrary) subset of sites.

<h2 class="bg-primary">Move Operators</h2>
The operators $$ M_i $$ are specified giving their matrix elements, and a list of sites on which they act. Each operator $$ M_i $$ must be real, symmetric, positive definite and stochastic (i.e. sum of each column and line is 1).

The transition probability associated to a custom sampler can be decomposed into two steps:

1. One of the move operators $$ M_i $$ is chosen with a weight given by the user (or uniform probability by default). If the weights are provided, they do not need to sum to unity.
2. Starting from state $$ |n\rangle $$, the probability to transition to state $$ |m\rangle $$ is given by $$ \langle n | M_i | m \rangle $$.

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `ActingOn` | List of list of integers  |  The sites on which each $$ M_i $$ acts on | None |
| `MoveOperators` | List of stochastic matrices |  For each $$ i $$, the matrix elements of $$ M_i $$ in the $$ k $$-local Hilbert space | None |
| `MoveWeights` | List of reals |  For each $$ i $$, the probability to pick one of the move operators (must sum to one) | uniform probability |
|===


### Example

(extracted from `Tutorials/CustomSampler/customsampler_heisenberg1d.py`)
```python
# defining the custom sampler
# for a spin 1/2 chain of size L
# here we use two types of moves : local spin flip (0 <--> 1), and exchange flip between two sites (10 <--> 01, 11 and 00 are unchanged)
# note that each line and column has to add up to 1.0 (stochastic matrices)
# we also choose a relative frequency of 2 for local-spin flips with respect to exchange flips
spin_flip = [[0, 1], [1, 0]]
exchange_flip = [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
weight_spin_flip = 2.0
weight_exchange_flip = 1.0

# adding both types of flip for all sites in the chain
operators = []
sites = []
weights = []
for i in range(L):
        operators.append(exchange_flip)
        sites.append([i, (i + 1) % L])
        weights.append(weight_exchange_flip)
        operators.append(spin_flip)
        sites.append([i])
        weights.append(weight_spin_flip)

# now we define the custom sampler accordingly
pars['Sampler'] = {
'MoveOperators' : operators,
'ActingOn' : sites,
'MoveWeights' : weights,
# parallel tempering is also possible with custom sampler (uncomment the following line)
#'Nreplicas' : 12,
}
```


<h2 class="bg-primary">CustomSamplerPt</h2>
The custom sampler can perform [parallel-tempering](https://en.wikipedia.org/wiki/Parallel_tempering) moves in addition to the custom moves implemented in `CustomSampler`. The number of replicas $$ N_{\mathrm{rep}} $$ can be chosen by the user (see commented line in the example above).

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `Nreplicas` | Integer |  The number of effective temperatures for parallel tempering, $$ N_{\mathrm{rep}} $$ | None |
|===
