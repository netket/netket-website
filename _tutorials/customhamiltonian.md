---
title: Defining Custom Hamiltonians
permalink: /tutorials/customhamiltonian/
description: Learn how to define a custom Hamiltonian in NetKet.
---

In this tutorial, we will see how to define custom Hamiltonians in NetKet.

NetKet provides two ```operator``` classes for defining custom Hamiltonians.

1. ```netket.operator.GraphOperator```
2. ```netket.operator.LocalOperator```

We will explore both of these methods in this tutorial.

Let's start.


```python
# Import netket library
import netket as nk
from mpi4py import MPI

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
```

## 1) GraphOperator

We shall use the ```GraphOperator``` to define the spin half J1-J2 model in one-dimension. The Hamiltonian

$$ \hat{H} = \sum_{i=1}^{L} J_{1}\hat{S}_{i} \cdot \hat{S}_{i+1} + J_{2} \hat{S}_{i} \cdot \hat{S}_{i+2} $$

This is an operator defined on the bonds of a graph. For example, we can define a graph with two types of edges: nearest-neighbour and next-nearest-neighbour. We can then specify a bond operator for each type of edge. This is exactly what we need to define the J1-J2 model above.

First, we need a custom graph ``nk.graph.CustomGraph``. To initialise the class we simply provide a list of edges in the ``[[site_i, site_j, edge_color], ...]``. In our example, we give the ```edge_color``` ```1``` for nearest-neighbour edges and the ```2``` for next-nearest-neighbour edges.


```python
# J1-J2 Model Parameters
J = [1, 0.2]
L = 16

# Define custom graph
edge_colors = []
for i in range(L):
    edge_colors.append([i, (i+1)%L, 1])
    edge_colors.append([i, (i+2)%L, 2])

# Define the netket graph object
g = nk.graph.CustomGraph(edge_colors)

print('This graph has', g.n_sites, 'sites')
print('with the following set of edges:', g.edges)
```

    This graph has 16 sites
    with the following set of edges: [[1, 15], [0, 14], [12, 13], [13, 15], [11, 12], [12, 14], [10, 11], [11, 13], [9, 10], [10, 12], [8, 9], [9, 11], [7, 8], [8, 10], [14, 15], [6, 7], [7, 9], [13, 14], [5, 6], [6, 8], [4, 5], [5, 7], [0, 15], [3, 4], [4, 6], [2, 3], [3, 5], [1, 2], [2, 4], [0, 1], [1, 3], [0, 2]]


Next, lets define the Hilbert space of our model.


```python
# Spin based Hilbert Space
hi = nk.hilbert.Spin(s=0.5, total_sz=0.0, graph=g)
```

Now, we need to create the relevant bond operators. Since we have two type of terms in our Hamiltonian, we need two different bond operators. To do we simply express the iteraction term as a matrix in the computational basis of the relevant local Hilbert space. In our case, since we are dealing with spin-half degrees of freedom, the local basis of bond is simply $$ \lvert \uparrow \uparrow \rangle $$, $$ \lvert \uparrow \downarrow \rangle $$, $$ \lvert \downarrow \uparrow \rangle $$, $$ \lvert \downarrow \downarrow \rangle $$. Since

$$
\begin{equation}
\hat{S}_{i} \cdot \hat{S}_{i+1} = \hat{S}_{i}^{z}\hat{S}_{i+1}^{z} + \hat{S}_{i}^{x}\hat{S}_{i+1}^{x} + \hat{S}_{i}^{y}\hat{S}_{i+1}^{y}
\end{equation}
$$

we just need to represent each term as kronecker product of the standard Pauli matrix.



```python
# Pauli Matrices
sigmaz = [[1, 0], [0, -1]]
sigmax = [[0, 1], [1, 0]]
sigmay = [[0, -1j], [1j, 0]]

# Bond Operator
interaction = np.kron(sigmaz, sigmaz) + np.kron(sigmax, sigmax) + np.kron(sigmay, sigmay)  

bond_operator = [
    (J[0] * interaction).tolist(),
    (J[1] * interaction).tolist(),
]
bond_color = [1, 2]
```

The ```GraphOperator``` can now be defined simply by doing providing the list of bond operators and the corresponding list of bond colors.


```python
# Custom Graph Hamiltonian operator
op = nk.operator.GraphOperator(hi, bondops=bond_operator, bondops_colors=bond_color)
```

The Hamiltonian is now defined and one can proceed to perform variational Monte Carlo or supervised learning or exact diagonalisation. The code snippet below gives us the exact diagonalisation result for the ground state energy of our Hamiltonian.


```python
res = nk.exact.lanczos_ed(op, first_n=1, compute_eigenvectors=True)
print("Exact J1J2 ground state energy = {0:.3f}".format(res.eigenvalues[0]))
```

    Exact J1J2 ground state energy = -26.308


## 2) LocalOperator

The next method we would use is the ```LocalOperator``` class. Let's use this method to define a one-dimensional spin half transverse field Ising model given by the Hamiltonian:

$$ \hat{H} = -\sum_{i=1}^{L} \hat{S}_{i}^{z} \hat{S}_{i+1}^{z} + h \sum_{i=1}^{L} \hat{S}_{i}^{x}  $$.

As before, we start by defining the graph on which our degree of freedom sits.

Once again, we use the ```CustomGraph```, but this time we do not need to provide our edges with colors. We simply provide it with the list of edges.


```python
h = 0.5
L = 16

edges = []
for i in range(L):
    edges.append([i, (i+1)%L])

g = nk.graph.CustomGraph(edges)
```

Next, we define the Hilbert space but without the constraint of on total magnetization ```total_sz```.


```python
# Spin based Hilbert Space
hi = nk.hilbert.Spin(s=0.5, graph=g)
```

Now, we simply define a list of local operators corresponding to the different terms in the Hamiltonian and also  a list containing the sites on which the respective local operators acts on.


```python
# Pauli Matrices
sigmaz = np.array([[1, 0], [0, -1]])
sigmax = np.array([[0, 1], [1, 0]])

operators = []
sites = []

# Local Field term
for i in range(L):
    operators.append((h*sigmax).tolist())
    sites.append([i])

# Ising iteraction
for i in range(L):
    operators.append((-np.kron(sigmaz,sigmaz)).tolist())
    sites.append([i, (i+1)%L])
```

Then, we create the ```LocalOperator``` by proving the list of operators and the list of sites.


```python
op = nk.operator.LocalOperator(hi, operators=operators, acting_on=sites)
```


```python
res = nk.exact.lanczos_ed(op, first_n=1, compute_eigenvectors=True)
print("Exact transverse Ising ground state energy = {0:.3f}".format(res.eigenvalues[0]))
```

    Exact transverse Ising ground state energy = -17.017
