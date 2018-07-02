---
title: Graph Hamiltonians
permalink: /docs/graph_hamiltonians/
---

Netket provides users with the ability to specify Hamiltonians based on properties of a custom graph. Users can specify whether operators act on sites or edges with a particular color. For examples about how to specify the edges colors see the [custom graphs documentation]({{ site.baseurl }}{% link _docs/graphs/custom_graphs.md %}).

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

<h2 class="bg-primary">Specifying the Site and Bond Operators</h2>
Users must specify all three parameters below. If necessary, they may be set to an empty list.

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `SiteOps` | List of floating/complex matrices | The unique operators that act on each site | None |
| `BondOps` | List of floating/complex matrices | The unique operators acting on bonds | None |
| `BondOpColors` | List of integers | Each color corresponds to an operator in BondOps | None |
|===

### Example
```python

from __future__ import print_function
import json
import numpy as np
import networkx as nx

#Sigma^z*Sigma^z interactions
sigmaz = [[1, 0], [0, -1]]
mszsz = (np.kron(sigmaz, sigmaz))

#Exchange interactions
exchange = np.asarray([[0, 0, 0, 0], [0, 0, 2, 0], [0, 2, 0, 0], [0, 0, 0, 0]])

#Couplings J1 and J2
J = [1, 0.4]
L = 20

pars = {}

# Define bond operators and associated colors
bond_operator = [
    (J[0] * mszsz).tolist(),
    (J[1] * mszsz).tolist(),
    (-J[0] * exchange).tolist(),
    (J[1] * exchange).tolist(),
]

bond_color = [1, 2, 1, 2]

# Define custom graph
G = nx.DiGraph()
for i in range(L):
    G.add_edge(i, (i + 1) % L, color=1)
    G.add_edge(i, (i + 2) % L, color=2)

edge_colors = [G[u][v]['color'] for u, v in G.edges]

# Specify custom graph
pars['Graph'] = {
    'Edges': list(G.edges),
    'EdgeColors': edge_colors,
}

#We chose a spin 1/2 hilbert space with total Sigmaz=0
pars['Hilbert'] = {
    'Name': 'Spin',
    'S': 0.5,
    'TotalSz': 0,
    'Nspins': L,
}

#defining our graph hamiltonian
pars['Hamiltonian'] = {
    'Name': 'Graph',
    'SiteOps': [],
    'BondOps': bond_operator,
    'BondOpColors': bond_color,
}
```
