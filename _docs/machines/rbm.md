---
title: Restricted Boltzmann Machine
permalink: /docs/rbm/
---

[Restricted Boltzmann machines](https://en.wikipedia.org/wiki/Restricted_Boltzmann_machine) are implemented in different flavors in NetKet.

<h2 class="bg-primary">RbmSpin</h2>
This type of RBM has spin $$ 1/2 $$ hidden units, and is defined by:

$$
\Psi(s_1,\dots s_N)  = e^{\sum_i^N a_i s_i} \times \Pi_{j=1}^M \cosh \left(\sum_i^N W_{ij} s_i + b_j \right)
$$

for arbitrary local quantum numbers $$ s_i $$. The total number of variational parameters is $$ \mathcal{O} (M \times N) $$, and all parameters are taken complex-valued.
For more information see (1).


|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `Alpha` | Float |  Alternative to Nhidden, here $$ \alpha= M/N $$ | None |
| `InitFile` | String |  If specified, network parameters are loaded from the given file | None |
| `InitRandom` | Boolean |  Whether to initialize the parameters with random gaussian-distributed values | True |
| `Nhidden` | Integer |  The number of hidden units $$ M $$ | None |
| `SigmaRand` | Float |  If InitRandom is chosen, this is the standard deviation of the gaussian  | 0.1 |
| `UseHiddenBias` | Boolean |  Whether to use the hidden bias $$ b_j $$ | True |
| `UseVisibleBias` | Boolean |  Whether to use the visible bias $$ a_i $$ | True |
|===

### Example
```python
pars['Machine']={
    'Name'           : 'RbmSpin',
    'Alpha'          : 1.0,
}
```

<h2 class="bg-primary">RbmSpinSymm</h2>
This type of RBM has spin $$ 1/2 $$ hidden units, and is constructed to be invariant under specific permutations of the
graph indices. In particular, $$ \Psi(s_1,\dots s_N) = \Psi(s_{P_k(1)} \dots s_{P_k(N)}) $$, where $$ P_k(i) $$ is the $$ k $$ -th permutation of the index $$ i $$,
and assuming a total of $$ N_p $$ distinct permutations.  

$$
\Psi(s_1,\dots s_N)  = e^{a \sum_i^N s_i} \times \Pi_{f=1}^{\alpha} \Pi_{k=1}^{N_p} \cosh \left(\sum_i^N W_{if} s_{P_k(i)} + b_f \right)
$$

for arbitrary local quantum numbers $$ s_i $$. The total number of variational parameters is $$ \mathcal{O} (\alpha \times N) $$, and all parameters are taken complex-valued.
For more information see the translation-invariant RBM used in (1).


|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `Alpha` | Float |  Hidden unit density $$ \alpha $$ | None |
| `InitFile` | String |  If specified, network parameters are loaded from the given file | None |
| `InitRandom` | Boolean |  Whether to initialize the parameters with random gaussian-distributed values | True |
| `SigmaRand` | Float |  If InitRandom is chosen, this is the standard deviation of the gaussian  | 0.1 |
| `UseHiddenBias` | Boolean |  Whether to use the hidden bias $$ b_j $$ | True |
| `UseVisibleBias` | Boolean |  Whether to use the visible bias $$ a $$ | True |
|===

### Example
```python
pars['Machine']={
    'Name'           : 'RbmSpinSymm',
    'Alpha'          : 1.0,
}
```


<h2 class="bg-primary">RbmMultival</h2>
This type of RBM has spin $$ 1/2 $$ hidden units, and couplings dependent on the quantum numbers.
It is defined by:

$$
\Psi(s_1,\dots s_N)  = e^{\sum_i^N a_i[s_i]} \times \Pi_{j=1}^M \cosh \left(\sum_i^N W_{ij}[s_i] + b_j \right)
$$

where $$ s_i $$ are local quantum numbers taking $$ m $$ possible values. The total number of variational parameters is $$ \mathcal{O} (m \times M \times N) $$, and all parameters are taken complex-valued.


|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `Alpha` | Float |  Alternative to Nhidden, here $$ \alpha= M/N $$ | None |
| `InitFile` | String |  If specified, network parameters are loaded from the given file | None |
| `InitRandom` | Boolean |  Whether to initialize the parameters with random gaussian-distributed values | True |
| `Nhidden` | Integer |  The number of hidden units $$ M $$ | None |
| `SigmaRand` | Float |  If InitRandom is chosen, this is the standard deviation of the gaussian  | 0.1 |
| `UseHiddenBias` | Boolean |  Whether to use the hidden bias $$ b_j $$ | True |
| `UseVisibleBias` | Boolean |  Whether to use the visible bias $$ a_i $$ | True |
|===

### Example
```python
pars['Machine']={
    'Name'           : 'RbmMultival',
    'Alpha'          : 1.0,
}
```


## References
---------------
1. [Hinton, G, & Salakhutdinov, R. (2006). Reducing the Dimensionality of Data with Neural Networks. Science, 313 504](http://science.sciencemag.org/content/313/5786/504)
2. [Carleo, G., & Troyer, M. (2017). Solving the quantum many-body problem with artificial neural networks. Science, 355 602](http://science.sciencemag.org/content/355/6325/602)
