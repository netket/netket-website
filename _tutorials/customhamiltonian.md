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

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
```

## 1) GraphOperator

We shall use the ```GraphOperator``` to define the spin half $J_1$-$J_2$ model in one dimension. The Hamiltonian

$$ H = \sum_{i=1}^{L} J_{1}\vec{\sigma}_{i} \cdot \vec{\sigma}_{i+1} + J_{2} \vec{\sigma}_{i} \cdot \vec{\sigma}_{i+2} $$

Here $\vec{\sigma}=(\sigma^x,\sigma^y,\sigma^z)$ stand for the vector of Pauli matrices. Each term is the sum is an operator defined on the bonds of a graph. For example, we can define a graph with two types of edges: nearest-neighbour and next-nearest-neighbour. We can then specify a bond operator for each type of edge. This is exactly what we need to define the model above.

First, we need a custom graph ``nk.graph.CustomGraph``. To initialise the class we simply provide a list of edges in the ``[[site_i, site_j, edge_color], ...]``. In our example, we give the ```edge_color``` ```1``` for nearest-neighbour edges and the ```2``` for next-nearest-neighbour edges.


```python
# J1-J2 Model Parameters
J = [1, 0.2]
L = 20

# Define custom graph
edge_colors = []
for i in range(L):
    edge_colors.append([i, (i+1)%L, 1])
    edge_colors.append([i, (i+2)%L, 2])

# Define the netket graph object
g = nk.graph.CustomGraph(edge_colors)

# Printing out the graph information
print('This graph has', g.n_sites, 'sites')
print('with the following set of edges:', g.edges)
```

    This graph has 20 sites
    with the following set of edges: [[17, 19], [16, 18], [15, 17], [14, 16], [14, 15], [13, 15], [13, 14], [12, 14], [12, 13], [11, 13], [11, 12], [10, 12], [1, 19], [10, 11], [0, 19], [9, 11], [0, 18], [9, 10], [8, 10], [8, 9], [7, 9], [7, 8], [6, 8], [6, 7], [5, 7], [5, 6], [4, 6], [4, 5], [18, 19], [3, 5], [3, 4], [17, 18], [2, 4], [2, 3], [16, 17], [1, 3], [1, 2], [15, 16], [0, 2], [0, 1]]


Next, let's define the Hilbert space of our model. Note that we impose here to select only configurations with zero total magnetization:


```python
# Spin 1/2 based Hilbert Space
hi = nk.hilbert.Spin(s=0.5, total_sz=0.0, graph=g)
```

Now, we need to create the relevant bond operators. Since we have two type of terms in our Hamiltonian, we need two different bond operators. To do this, we simply express the interaction term as a matrix in the computational basis of the relevant local Hilbert space. In our case, since we are dealing with spin-half degrees of freedom, the local basis of bond is simply $\lvert \uparrow \uparrow \rangle$, $\lvert \uparrow \downarrow \rangle$, $\lvert \downarrow \uparrow \rangle$, $\lvert \downarrow \downarrow \rangle$. Since

\begin{equation} 
\vec{\sigma}_{i} \cdot \vec{\sigma}_{i+1} = {\sigma}_{i}^{z}{\sigma}_{i+1}^{z} + {\sigma}_{i}^{x}{\sigma}_{i+1}^{x} + {\sigma}_{i}^{y}{\sigma}_{i+1}^{y} 
\end{equation}

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
res = nk.exact.lanczos_ed(op, first_n=1, compute_eigenvectors=False)
print("Exact J1J2 ground state energy = {0:.3f}".format(res.eigenvalues[0]))
```

    Exact J1J2 ground state energy = -32.812


## 2) LocalOperator

The second method we can use is through the ```LocalOperator``` class. Let's use this method to define a one-dimensional spin half transverse field Ising model given by the Hamiltonian:

$$ {H} = -\sum_{i=1}^{L} {\sigma}_{i}^{z} {\sigma}_{i+1}^{z} + h \sum_{i=1}^{L} {\sigma}_{i}^{x}  $$.

As before, we start by defining the graph on which our degrees of freedom sit. 

Once again, we use the ```CustomGraph```, but this time we do not need to provide our edges with colors. We simply provide it with the list of edges.


```python
h = 0.5
L = 16

edges = []
for i in range(L):
    edges.append([i, (i+1)%L])

g = nk.graph.CustomGraph(edges)
```

Next, we define the Hilbert space as earlier, except that this time we do not impose the constraint on total magnetization ```total_sz``` (as it is not a quantity conserved by this Hamiltonian this time)


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

And finally we again compute the ground-state energy


```python
res = nk.exact.lanczos_ed(op, first_n=1, compute_eigenvectors=False)
print("Exact transverse Ising ground state energy = {0:.3f}".format(res.eigenvalues[0]))
```

    Exact transverse Ising ground state energy = -17.017

