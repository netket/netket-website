---
title: Restricted Boltzmann Machine
permalink: /docs/rbm/
---

Restricted Boltzmann machines are implemented in different flavors in NetKet.

<h2 class="bg-primary">RbmSpin</h2>
This type of RBM has spin $$ 1/2 $$ hidden units, and is defined by:

$$
\Psi(s_1,\dots s_N)  = e^{\sum_i^N a_i s_i} \times \Pi_{j=1}^M \cosh \left(\sum_i^N W_{i,j} s_i + b_j \right)
$$

for arbitrary local quantum numbers $$ s_i $$. All weights are taken complex-valued.
For more information see (1).


|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `Alpha` | Float |  Alternative to Nhidden, here $$ \alpha= M/N $$ | None |
| `Nhidden` | Integer |  The number of hidden units $$ M $$ | None |
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

<p class="bg-warning">Parameters initialization.</p>

## References
---------------
1. [Carleo, G., & Troyer, M. (2017). Solving the quantum many-body problem with artificial neural networks. Science, 355 602](http://science.sciencemag.org/content/355/6325/602)
