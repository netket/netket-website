---
title: Built-in Hamiltonians
permalink: /docs/hardcoded_hamiltonians/
---

NetKet provides a library of built-in Hamiltonians, that can be accessed specifying the
`Name` tag in the `Hamiltonian` section of the input. Those Hamiltonians are typically defined
over a certain graph (say, particles on a square lattice), thus the user must also
specify either an [Built-in]({{ site.baseurl }}{% link _docs/graphs/hardcoded_graphs.md %}) or
a [Custom]({{ site.baseurl }}{% link _docs/graphs/custom_graphs.md %}) graph.

<h2 class="bg-primary">Ising</h2>
The transverse-field Ising model for spin $$ 1/2 $$ particles

$$
\mathcal{H}=-h\sum_{l}\sigma_{l}^{x} -J \sum_{\langle l,m \rangle}\sigma_{l}^{z}\sigma_{m}^{z},
$$

where the interaction terms runs over pairs of nearest-neighbors on a given graph.
To use this Hamiltonian, you must specify a valid Graph in the input.

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `h` | Float  |  The transverse field $$ h $$ | None |
| `J` | Float |  The coupling constant $$ J $$ | 1 |
|===

### Example
```python
pars['Hamiltonian']={
    'Name'           : 'Ising',
    'h'              : 1.0,
}
```

<h2 class="bg-primary">Heisenberg</h2>
The antiferromagnetic Heisenberg model for spin $$ 1/2 $$ particles

$$
\mathcal{H}=J\sum_{i,j} \left(\sigma_{i}^{x}\sigma_{j}^{x}+\sigma_{i}^{y}\sigma_{j}^{y}+\sigma_{i}^{z}\sigma_{j}^{z}\right),
$$

where the exchange terms runs over pairs of nearest-neighbors on a given graph.
To use this Hamiltonian, you must specify a valid Graph in the input.

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `TotalSz` | Float  |  If specified, the sampling is restricted to the given value of $$ \sum_i \sigma_{i}^{z} $$ | Unspecified |
|===

### Example
```python
pars['Hamiltonian']={
    'Name'           : 'Heisenberg',
    'TotalSz'        : 0,
}
```

<h2 class="bg-primary">BoseHubbard</h2>
The Bose-Hubbard model for soft-core bosons,

$$
\mathcal{H}= -J \sum_{i,j} b^{\dagger}_i b_j + \frac{U}{2} \sum_i n_i(n_i-1) -\mu \sum_i n_i,
$$

where the hopping term runs over pairs of nearest-neighbors on a given graph.
To use this Hamiltonian, you must specify a valid Graph in the input.

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `Nbosons` | Integer  |  If specified, the sampling is restricted to the given value of $$ \sum_i n_{i} $$ | Unspecified |
| `Nmax` | Integer  |  The maximum number of bosons per site | None |
| `Mu` | Float  |  The chemical potential $$ \mu $$ | 0 |
| `U` | Float  |  The Hubbard interaction strength $$ U $$ | None |
|===

### Example
```python
pars['Hamiltonian']={
    'Name'           : 'BoseHubbard',
    'U'              : 4.0,
    'Nmax'           : 3,
    'Nbosons'        : 12,
}
```
