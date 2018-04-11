---
title: Custom Hamiltonians
permalink: /docs/custom_hamiltonians/
---

NetKet provides the freedom to define user's defined Hamiltonians, just specifying the relevant operators
in the `Hamiltonian` section of the input. For the moment, this functionality is limited to
lattice Hamiltonians which are sums of $$ k $$ -local operators:

$$
\mathcal{H}= \sum_i h_i,
$$

where the operators $$ h_i $$ act on an (arbitrary) subset of sites. In order to define your custom
Hamiltonian, you need to specify both the local Hilbert space and the operators $$ h_i $$.

<h2 class="bg-primary">Specifying the local Hilbert space</h2>
The Hilbert space here is constructed as the tensor product of $$ L $$ local Hilbert spaces
in such a way that the many-body quantum numbers are

$$
\left | s_1 s_2 \dots s_L \right \rangle,
$$

where each $$ s_i $$ can take values in the set $$ n_1 n_2 \dots $$.


|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `QuantumNumbers` | List of floats  |  A set of local quantum numbers $$ n_1 n_2 \dots $$. They do not need to be ordered or be consecutive. | None |
| `Size` | Integer |  The total number of lattice sites $$ L $$ | None |
|===

### Example
```python
pars['Hilbert']={
    'QuantumNumbers' : [1,-1],
    'Size'           : L,
}
```

<h2 class="bg-primary">Local Operators</h2>
The local operators $$ h_i $$ are specified giving their matrix elements, and a list of sites on which they act.
For example, to specify a single-site operator acting on site $$ l$$, and with a local Hilbert space of two elements $$ n_1, n_2 $$,
you must provide a $$ 2 \times 2 $$ matrix

$$
\left(\begin{array}{cc}
\langle n_{1}|h|n_{1}\rangle & \langle n_{2}|h|n_{1}\rangle\\
\langle n_{1}|h|n_{2}\rangle & \langle n_{2}|h|n_{2}\rangle
\end{array}\right)
$$

In general, for a $$ k $$-local operator acting on local Hilbert spaces with $$ b $$ quantum numbers,
you must provide a $$ b^k \times b^k $$ matrix

$$
\left(\begin{array}{cccc}
\langle n_{1}n_{1}\dots n_{1}|h|n_{1}n_{1}\dots n_{1}\rangle & \langle n_{1}n_{1}\dots n_{1}|h|n_{1}n_{1}\dots n_{2}\rangle & \cdots & \langle n_{1}n_{1}\dots n_{1}|h|n_{b}n_{b}\dots n_{b}\rangle\\
\langle n_{1}n_{1}\dots n_{2}|h|n_{1}n_{1}\dots n_{1}\rangle & \langle n_{1}n_{1}\dots n_{2}|h|n_{1}n_{1}\dots n_{2}\rangle & \cdots & \langle n_{1}n_{1}\dots n_{2}|h|n_{b}n_{b}\dots n_{b}\rangle\\
\vdots & \vdots & \ddots & \vdots\\
\langle n_{b}n_{b}\dots n_{b}|h|n_{1}n_{1}\dots n_{1}\rangle & \langle n_{b}n_{b}\dots n_{b}|h|n_{1}n_{1}\dots n_{2}\rangle & \cdots & \langle n_{b}n_{b}\dots n_{b}|h|n_{b}n_{b}\dots n_{b}\rangle
\end{array}\right)
$$


|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `ActingOn` | List of list of integers  |  The sites on which each $$ h_i $$ acts on | None |
| `Operators` | List of floating/complex matrices |  For each $$ i $$, the matrix elements of $$ h_i $$ in the $$ k $$-local Hilbert space | None |
|===

### Example
```python
#Transverse-Field Ising model on L site
pars['Hamiltonian']={
    'ActingOn'       : sites,
    'Operators'      : operators,
}
```


## References
---------------
1. [Carleo, G., & Troyer, M. (2017). Solving the quantum many-body problem with artificial neural networks. Science, 355 602](http://science.sciencemag.org/content/355/6325/602)
