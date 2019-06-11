---
title: Heisenberg model with different variational states 
permalink: /tutorials/heisenberg1d/
description: Learning the ground-state of a spin model with different Neural Networks available in NetKet
---

The goal of this tutorial is to review various neural network architectures available in NetKet, and this in order to learn the ground-state of a paradigmatic spin model, namely the spin $1/2$ Heisenberg antiferromagnetic spin chain.

The Hamiltonian we will consider for this tutorial is the following

$$ H = \sum_{i=1}^{L} \vec{\sigma}_{i} \cdot \vec{\sigma}_{i+1}.$$

$L$ is the length of the chain, and we will use both open and periodic boundary conditions. $\vec{\sigma}=(\sigma^x,\sigma^y,\sigma^z)$ denotes  the vector of Pauli matrices. Please note that there is a factor of $2$ between Pauli-matrices and spin-1/2 operators (thus a factor of $4$ in $H$).

We will consider in this tutorial 5 possible ways of determining the ground-state of this model.

    0. Defining the Hamiltonian
    1. Exact Diagonalization (as a testbed)
    2. Starting simple: the Jastrow ansatz
    3. Learning with a Restricted Boltzmann Machine (RBM)
    4. RBM again, this time with lattice symmetries
    5. Learning with Feed Forward Neural Networks

Estimated time for this tutorial: 20 minutes.

First things first, let's import the essentials


```python
# Import netket library
import netket as nk
# Import Json, this will be needed to examine log files
import json
# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import time
```

## 0) Defining the Hamiltonian

NetKet covers quite a few standard Hamiltonians and lattices, so let's use this to quickly define the antiferromagnetic Heisenberg chain. For the moment we assume $L=22$ and simply define a chain lattice in this way (using periodic boundary conditions for now).


```python
# Define a 1d chain
L = 22
g = nk.graph.Hypercube(length=L, n_dim=1, pbc=True)
```

Next, we need to define the Hilbert space on this graph. We have here spin-half degrees of freedom, and as we know that the ground-state sits in the zero magnetization sector, we can already impose this as a constraint in the Hilbert space. This is not mandatory, but will nicely speeds things up in the following.


```python
# Define the Hilbert space based on this graph
# We impose to have a fixed total magnetization of zero
hi = nk.hilbert.Spin(s=0.5, graph=g, total_sz=0)
```

The final element of the triptych is of course the Hamiltonian acting in this Hilbert space, which in our case in already defined in NetKet. Note that the NetKet Hamiltonian uses Pauli Matrices (if you prefer to work with spin-$1/2$ operators, it's pretty trivial to define your own custom Hamiltonian, as covered in another tutorial)


```python
# calling the Heisenberg Hamiltonian
ha = nk.operator.Heisenberg(hilbert=hi)
```

## 1. Exact Diagonalization (as a testbed)

Just as a matter of future comparison, let's compute the exact ground-state energy (since this is still possible for $L=22$ using brute-force exact diagonalization).
NetKet provides wrappers to the Lanczos algorithm which we now use:


```python
# compute the ground-state energy (here we only need the lowest energy, and do not need the eigenstate)
exact_result = nk.exact.lanczos_ed(ha, first_n=1, compute_eigenvectors=False)
exact_gs_energy = exact_result.eigenvalues[0]
print('The exact ground-state energy is E0=',exact_gs_energy)

# Just in case you can't do this calculation, here is the result
# exact_gs_energy = -39.14752260706246
```

    The exact ground-state energy is E0= -39.14752260706246


## 2. Starting simple: the Jastrow ansatz

Let's start with a simple ansatz for the ground-state.


```python
ma = nk.machine.Jastrow(hilbert=hi)
ma.init_random_parameters(seed=1, sigma=0.01)
```


```python
# Optimizer
op = nk.optimizer.Sgd(learning_rate=0.1)

# Sampler
sa = nk.sampler.MetropolisExchange(machine=ma,graph=g)
ma.init_random_parameters(seed=12, sigma=0.01)

# Stochastic reconfiguration
gs = nk.variational.Vmc(
    hamiltonian=ha,
    sampler=sa,
    optimizer=op,
    n_samples=1000,
    diag_shift=0.1,
    method='Sr')

start = time.time()
gs.run(output_prefix='Jastrow', n_iter=300)
end = time.time()

print('### Jastrow calculation')
print('Has',ma.n_par,'parameters')
print('The Jastrow calculation took',end-start,'seconds')
```

    ### Jastrow calculation
    Has 231 parameters
    The Jastrow calculation took 15.655055046081543 seconds



```python
# import the data from log file
data=json.load(open("Jastrow.log"))

# Extract the relevant information
iters_Jastrow=[]
energy_Jastrow=[]

for iteration in data["Output"]:
    iters_Jastrow.append(iteration["Iteration"])
    energy_Jastrow.append(iteration["Energy"]["Mean"])

fig, ax1 = plt.subplots()
ax1.plot(iters_Jastrow, energy_Jastrow, color='C8', label='Energy (Jastrow)')
ax1.set_ylabel('Energy')
ax1.set_xlabel('Iteration')
plt.axis([0,iters_Jastrow[-1],exact_gs_energy-0.1,exact_gs_energy+0.4])
plt.axhline(y=exact_gs_energy, xmin=0,
                xmax=iters_Jastrow[-1], linewidth=2, color='k', label='Exact')
ax1.legend()
plt.show()
```


![png](/tutorials/img/heisenberg1d_output_13_0.png)


Well that's not too bad for a simple ansatz. But we can do better, can't we?

## 3. Learning with a Restricted Boltzmann Machine (RBM)

We will now consider another celebrated ansatz, the Restricted Boltzmann Machine (RBM). It simply consists of two layers: a visible one representing the $L$ spin 1/2 degrees of freedom, and an hidden one which contains a different number $M$ of hidden units. There are connections between all visible and hidden nodes. The ansatz is the [following](https://www.netket.org/docs/machine_RbmSpin/)

$\Psi_{\rm RBM} (\sigma_1^z,\sigma_2^z, ..., \sigma_L^z)  = \exp ( \sum_{i=1}^L a_i \sigma_i^z ) \prod_{i=1}^M \cosh (b_i + \sum_j W_{ij} \sigma^z_j)$

$a_i$ (resp. $b_i$) are the visible (resp. hidden) bias. Together with the weights $W_{ij}$, they are variational parameters that we (or rather NetKet) will optimize to minimize the energy. Netket gives you the control on the important parameters in this ansatz, such as $M$ and the fact that you want to use or not the biases. The full explanation is [here](https://www.netket.org/docs/machine_RbmSpin/).

More conveniently (especially if you want to try another $L$ in this tutorial), let's define the hidden unit density $\alpha = M / L$, and invoke the RBM ansatz in NetKet with as many hidden as visible units.


```python
# RBM ansatz with alpha=1
ma = nk.machine.RbmSpin(alpha=1, hilbert=hi)
```

And let us use the same sampler (Metropolis exchange) with some different random initial parameters, optimizer (stochastic gradient), and variational method (stochastic reconfiguration) as for the Jastrow ansatz, and let's run things!


```python
# Sampler
sa = nk.sampler.MetropolisExchange(machine=ma,graph=g)
ma.init_random_parameters(seed=123, sigma=0.01)

# Optimizer
op = nk.optimizer.Sgd(learning_rate=0.05)
# Stochastic reconfiguration
gs = nk.variational.Vmc(
    hamiltonian=ha,
    sampler=sa,
    optimizer=op,
    n_samples=1000,
    diag_shift=0.1,
    use_iterative=True,
    method='Sr')

start = time.time()
gs.run(output_prefix='RBM', n_iter=600)
end = time.time()

print('### RBM calculation')
print('Has',ma.n_par,'parameters')
print('The RBM calculation took',end-start,'seconds')
```

    ### RBM calculation
    Has 528 parameters
    The RBM calculation took 79.31553912162781 seconds



```python
# import the data from log file
data=json.load(open("RBM.log"))

# Extract the relevant information
iters=[]
energy_RBM=[]

for iteration in data["Output"]:
    iters.append(iteration["Iteration"])
    energy_RBM.append(iteration["Energy"]["Mean"])

fig, ax1 = plt.subplots()
ax1.plot(iters_Jastrow, energy_Jastrow, color='C8', label='Energy (Jastrow)')
ax1.plot(iters, energy_RBM, color='red', label='Energy (RBM)')
ax1.set_ylabel('Energy')
ax1.set_xlabel('Iteration')
plt.axis([0,iters[-1],exact_gs_energy-0.03,exact_gs_energy+0.2])
plt.axhline(y=exact_gs_energy, xmin=0,
                xmax=iters[-1], linewidth=2, color='k', label='Exact')
ax1.legend()
plt.show()
```


![png](/tutorials/img/heisenberg1d_output_19_0.png)


Note that this plot zooms closer to the exact ground-state energy. With 600 iterations, we start to see convergence and reach the ground-state energy within about one per thousand, this is already nice! But we are not totally there yet, and in particular the simpler (less parameters) Jastrow wave-function seems to perform better for this example. How can we improve things? As an exercice, try to increase the number of hidden units and/or the number of iterations. What is happening? You can also check out the influence of the learning rate.

By playing with these parameters, you have hopefully arrived at an improved result, but likely at an increased CPU time cost. Let's do things differently, and take to our advantage the symmetries of the Hamiltonian in the neural network construction.


## 4. RBM again, this time with lattice symmetries

Let's define a similar RBM machine, which takes into account that the model has translational symmetries. All sites are equivalent and thus many of the wave-functions coefficients are related by symmetry. We use the same exact hyperparameters as in the previous RBM calculation ($\alpha=1$, same learning rate, and number of samples and iterations in the Variational Monte Carlo) and run now a symmetric RBM.


```python
# Symmetric RBM Spin Machine
ma = nk.machine.RbmSpinSymm(alpha=1, hilbert=hi)
ma.init_random_parameters(seed=1234, sigma=0.01)

# Metropolis Exchange Sampling
# Notice that this sampler exchanges two neighboring sites
# thus preservers the total magnetization
sa = nk.sampler.MetropolisExchange(machine=ma, graph=g)

# Optimizer
op = nk.optimizer.Sgd(learning_rate=0.05)

# Stochastic reconfiguration
gs = nk.variational.Vmc(
    hamiltonian=ha,
    sampler=sa,
    optimizer=op,
    n_samples=1000,
    diag_shift=0.1,
    use_iterative=True,
    method='Sr')

start = time.time()
gs.run(output_prefix='RBMSymmetric', n_iter=300)
end = time.time()

print('### Symmetric RBM calculation')
print('Has',ma.n_par,'parameters')
print('The Symmetric RBM calculation took',end-start,'seconds')
```

    ### Symmetric RBM calculation
    Has 24 parameters
    The Symmetric RBM calculation took 33.651692152023315 seconds


The simulation was much faster, wasn't it? There were of course much less parameters to optimize. Now let's extract the results and plot them using a zoomed scale, and together with the previous results with the RBM.


```python
# import the data from log file
data=json.load(open("RBMSymmetric.log"))

# Extract the relevant information
energy_symRBM=[]
iters_symRBM=[]
for iteration in data["Output"]:
    energy_symRBM.append(iteration["Energy"]["Mean"])
    iters_symRBM.append(iteration["Iteration"])

fig, ax1 = plt.subplots()
ax1.plot(iters_Jastrow, energy_Jastrow, color='C8', label='Energy (Jastrow)')
ax1.plot(iters, energy_RBM, color='red', label='Energy (RBM)')
ax1.plot(iters_symRBM, energy_symRBM, color='blue', label='Energy (Symmetric RBM)')

ax1.set_ylabel('Energy')
ax1.set_xlabel('Iteration')
plt.axis([0,iters_symRBM[-1],exact_gs_energy-0.06,exact_gs_energy+0.12])
plt.axhline(y=exact_gs_energy, xmin=0,
                xmax=iters[-1], linewidth=2, color='k', label='Exact')
ax1.legend()
plt.show()
```


![png](/tutorials/img/heisenberg1d_output_24_0.png)


Not only the simulation was faster in terms of CPU time, but we are now reaching the ground-state in a much lower number of iterations! Imposing symmetries greatly helps, and NetKet allows to do this. Note that there is also a symmetric version of the Jastrow ansatz that we tested [earlier](#2.-Starting-simple:-the-Jastrow-ansatz) in NetKet, which is called `JastrowSymm`. As an exercice, check it out. What you will find is that while it converges slightly faster in terms of iterations with respect to the non-symmetric Jastrow, it does not improve the estimate of the ground-state energy. We actually see that the symmetric RBM sets the standard very high.

## 5. Learning with Feed Forward Neural Networks

Now let's try a more complex network, namely a Feed Forward Neural Network (FFNN). There you will have more freedom to construct your own specific architecture. We'll try two different FFNN in this tutorial.

The first one is a simple structure: the first layer takes as input L-dimensional input, applies a bias and outputs two times more data, just followed by a `Lncosh` activation layer. The final layer `SumOuput` is needed to obtain a single number for the wave-function coefficient associated to the input basis state.



```python
layers = (nk.layer.FullyConnected(input_size=L,output_size=int(2*L),use_bias=True),
          nk.layer.Lncosh(input_size=int(2*L)),
          nk.layer.SumOutput(input_size=int(2*L))
         )
for layer in layers:
    layer.init_random_parameters(seed=12345, sigma=0.01)

ffnn = nk.machine.FFNN(hi, layers)

sa = nk.sampler.MetropolisExchange(graph=g, machine=ffnn)

opt = nk.optimizer.Sgd(learning_rate=0.05)

gs = nk.variational.Vmc(hamiltonian=ha,
                        sampler=sa,
                        optimizer=opt,
                        n_samples=1000,
                        use_iterative=True,
                        method='Sr')

start = time.time()
gs.run(output_prefix='FF', n_iter=300)
end = time.time()

print('### Feed Forward calculation')
print('Has',ffnn.n_par,'parameters')
print('The Feed Forward calculation took',end-start,'seconds')
```

    ### Feed Forward calculation
    Has 1012 parameters
    The Feed Forward calculation took 100.12213611602783 seconds



```python
# import the data from log file
data=json.load(open("FF.log"))

# Extract the relevant information
energy_FF=[]
for iteration in data["Output"]:
    energy_FF.append(iteration["Energy"]["Mean"])

fig, ax1 = plt.subplots()
ax1.plot(iters_Jastrow, energy_Jastrow, color='C8',linestyle="None", marker='d',label='Energy (Jastrow)')
ax1.plot(iters, energy_RBM, color='red', marker='o',linestyle="None",label='Energy (RBM)')
ax1.plot(iters_symRBM, energy_symRBM, color='blue',linestyle="None",marker='o',label='Energy (Symmetric RBM)')
ax1.plot(iters_symRBM, energy_FF, color='orange', marker='s',linestyle="None",label='Energy (Feed Forward, take 1)')
ax1.legend(bbox_to_anchor=(1.05, 0.3))
ax1.set_ylabel('Energy')
ax1.set_xlabel('Iteration')
plt.axis([0,iters_symRBM[-1],exact_gs_energy-0.02,exact_gs_energy+0.1])
plt.axhline(y=exact_gs_energy, xmin=0,
                xmax=iters[-1], linewidth=2, color='k', label='Exact')
plt.show()
```


![png](/tutorials/img/heisenberg1d_output_28_0.png)


The results are clearly better than a simple (non-symmetrized RBB), and perform slightly better than the Jastrow ansatz. Let us increase the number of layers by adding a fully-connected layer with bias and  `Lncosh` activation (with $2L$ inputs and ouputs) before the final `SumOuput` layer.


```python
layers = (nk.layer.FullyConnected(input_size=L,output_size=int(2*L),use_bias=True),
          nk.layer.Lncosh(input_size=int(2*L)),
          nk.layer.FullyConnected(input_size=int(2*L),output_size=int(2*L),use_bias=True),
          nk.layer.Lncosh(input_size=int(2*L)),
          nk.layer.SumOutput(input_size=int(2*L)),
         )
for layer in layers:
    layer.init_random_parameters(seed=123456, sigma=0.01)

ffnn = nk.machine.FFNN(hi, layers)

sa = nk.sampler.MetropolisExchange(graph=g, machine=ffnn)

opt = nk.optimizer.Sgd(learning_rate=0.05)

gs = nk.variational.Vmc(hamiltonian=ha,
                        sampler=sa,
                        optimizer=opt,
                        n_samples=1000,
                        use_iterative=True,
                        method='Sr')

start = time.time()
gs.run(output_prefix='FF2', n_iter=300)
end = time.time()


print('### Feed Forward (more layers) calculation')
print('Has',ffnn.n_par,'parameters')
print('The Feed Forward (more layers) calculation took',end-start,'seconds')
```

    ### Feed Forward (more layers) calculation
    Has 2992 parameters
    The Feed Forward (more layers) calculation took 285.4591450691223 seconds



```python
# import the data from log file
data=json.load(open("FF2.log"))

# Extract the relevant information
energy_FF_morelayers=[]
for iteration in data["Output"]:
    energy_FF_morelayers.append(iteration["Energy"]["Mean"])

fig, ax1 = plt.subplots()
#ax1.plot(iters_Jastrow, energy_Jastrow, color='C8',linestyle="None", marker='d',label='Energy (Jastrow)')
#ax1.plot(iters, energy_RBM, color='red', label='Energy (RBM)')
ax1.plot(iters_symRBM, energy_symRBM, color='blue',linestyle="None",marker='o',label='Energy (Symmetric RBM)')
ax1.plot(iters_symRBM, energy_FF, color='orange', marker='s',alpha=0.5,linestyle="None",label='Energy (Feed Forward, take 1)')
ax1.plot(iters_symRBM, energy_FF_morelayers, color='green',marker='s',linestyle="None", alpha=1,label='Energy (Feed Forward, more layers)')
ax1.legend(bbox_to_anchor=(1.05, 0.5))
ax1.set_ylabel('Energy')
ax1.set_xlabel('Iteration')
plt.axis([0,iters_symRBM[-1],exact_gs_energy-0.02,exact_gs_energy+0.06])
plt.axhline(y=exact_gs_energy, xmin=0,
                xmax=iters[-1], linewidth=2, color='k', label='Exact')
plt.show()
```


![png](/tutorials/img/heisenberg1d_output_31_0.png)


The results are even better, but at the price of an increase in computational time....

Note that more complex structures, such as Convolutional Neural Networks (CNN), can also be used within Netket. However, for such 1d systems, they do not bring too much compared to the symmetric RBM (as a matter of fact, the symmetric RBM is a special type of a simple CNN. CNNs show their full strength for more complex systems, such as 2d quantum systems. Convolutional Neural Networks will be the topic of another tutorial in NetKet (and we'll make there the connection with the special case of the symmetric RBM).

Finally let us conclude that another type of machine, Matrix Product States (MPS), is also available in NetKet. They do perform extremely well for 1d quantum systems. Since however they are a bit different, they will be presented in another tutorial.


```python

```
