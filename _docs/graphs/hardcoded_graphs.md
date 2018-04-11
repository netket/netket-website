---
title: Built-in Graphs
permalink: /docs/hardcoded_graphs/
---

NetKet provides a library of built-in graphs, that can be accessed specifying the
`Name` tag in the `Graph` section of the input. A graph specifies the geometrical arrangement
of the local degrees of freedom defining the quantum system, and is needed when
using [built-in Hamiltonians]({{ site.baseurl }}{% link _docs/hamiltonians/hardcoded_hamiltonians.md %}).
In other cases, it is not necessary to specify a graph explicitly.   

<h2 class="bg-primary">Hypercube</h2>
A hypercube lattice of side $$ L $$ in $$ d $$ dimensions. Periodic boundary
conditions can also be imposed.

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `Dimension` | Integer  |  The dimensionality of the Hypercube $$ d $$ | None |
| `L` | Integer |  The side of the Hypercube $$ L $$ | None |
| `Pbc` | Boolean |  Whether to use periodic boundary conditions | True |
|===

### Example
```python
pars['Graph']={
    'Name'           : 'Hypercube',
    'L'              : 20,
    'Dimension'      : 1 ,
    'Pbc'            : True,
}
```
