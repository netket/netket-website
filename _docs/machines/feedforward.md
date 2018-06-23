---
title: Feedforward Neural Networks
permalink: /docs/feedforward/
---

[Feedforward Neural Networks](https://en.wikipedia.org/wiki/Feedforward_neural_network) are implemented in NetKet. In this network, the information moves forward, from the input nodes, through the hidden layers and to the output nodes.

Let $$ \boldsymbol{v}_n $$ be the output vector of layer $$ n $$ and define the input into the network as $$ \boldsymbol{v}_0 $$. The output of layer $$ n $$ is then the input for layer $$ n + 1 $$. At each layer, we apply an affine map followed by a element wise non-linear function $$ g_{n} $$ (the so-called activation function), i.e.

$$
\boldsymbol{v}_n \rightarrow \boldsymbol{v}_{n+1} = g_{n}(\boldsymbol{W}_{n}\boldsymbol{v}_{n} + \boldsymbol{b}_{n}  )
$$

where $$ \boldsymbol{W}_{n} $$ are called the weights and $$ \boldsymbol{b}_{n} $$ are the biases.

We would like this network to represent a scalar wavefunction $$ \Psi(\boldsymbol{\sigma}) $$, where $$ \boldsymbol{\sigma} $$ represents a system configuration, e.g. $$ \uparrow\downarrow\downarrow \dots $$ for a spin-half system. Therefore, the output layer should have only 1 output node. such that for a network consisting of $$ n $$ layers, we have

$$
\boldsymbol{\sigma} = \boldsymbol{v}_{0} \rightarrow \boldsymbol{v}_{1} \rightarrow \dots \rightarrow v_{n} = \Psi(\boldsymbol{\sigma})
$$

There are other variations regarding the transformation applied at each layer but the basic idea remains the same, for instance convolutional layers where there is some element of parameter sharing among the elements of the weight matrix $$ \boldsymbol{W}_{n}. However, at the moment the only available layer is the fully connected one.

<h2 class="bg-primary">FFNN</h2>
To use the feedforward neural network (FFNN) one must specify a list of layers one wants to use.

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `Layers` | List | Contains list of descriptions for the the layers you intend to use (in order) | None |
| `InitFile` | String |  If specified, network parameters are loaded from the given file | None |
| `InitRandom` | Boolean |  Whether to initialize the parameters with random gaussian-distributed values | True |
| `SigmaRand` | Float |  If InitRandom is chosen, this is the standard deviation of the gaussian  | 0.1 |
|===

### Example
```python
pars['Machine']={
    'Name'      : 'FFNN',
    'Layers'    : [{'Name':'FullyConnected','Inputs': 20,'Outputs':20,'Activation':'Lncosh'},
                   {'Name':'FullyConnected','Inputs': 20,'Outputs':10,'Activation':'Lncosh'}],
}
```

The above example constructs a feedforward neural network comprising of three fully connected layers, with the following node structure: $$ 20 \rightarrow 20 \rightarrow 10 \rightarrow 1 $$. The third layer is a fully connected layer with identity activation function. This layer is added automatically so that the number of output nodes is one.

<h2 class="bg-primary">FullyConnected</h2>

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `Inputs` | Integer | Number of inputs to the layer | None |
| `Outputs` | Integer | Number of outputs to the layer| None |
| `Activation` | String |  Choice of Activation function | None |
| `UseBias` | Boolean |  Whether to use the bias $$ \boldsymbol{b}_n $$ | True |
|===

## References
---------------
1. [Hinton, G, & Salakhutdinov, R. (2006). Reducing the Dimensionality of Data with Neural Networks. Science, 313 504](http://science.sciencemag.org/content/313/5786/504)
2. [Carleo, G., & Troyer, M. (2017). Solving the quantum many-body problem with artificial neural networks. Science, 355 602](http://science.sciencemag.org/content/355/6325/602)
