---
title: Optimizers
permalink: /docs/optimizers/
---

The vast majority of learning applications solves the associated high-dimensional optimization problem in an iterative way.

More formally, given a cost function $$ F(\mathbf{p}) $$ to be minimized, depending on a set of $$ \mathbf{p} = p_1 \dots p_M $$,
then at each step of the optimization, we perform a change in the parameters:

$$
p^\prime_k = p_k + \mathcal{S}_k,
$$

i.e. each component is updated with a variation $$ \mathcal{S}_k $$ depending on the current/past set of parameters, and on the cost function $$ F $$.
Typically, but not exclusively, $$ \mathcal{S} $$ contains information directly related to the gradient of $$ F $$.

NetKet implements a series of *optimizers*, suitable for situations where the gradient of $$ F $$ (and $$ F $$ itself) is known only stochastically.
Optimizers must be used in conjunction with one of the available learning Methods, specifying the field `Name` in the `Optimizer` section of the input (see for example [here](../stochastic_reconfiguration/)).


<h2 class="bg-primary">Stochastic Gradient Descent</h2>

[Stochastic Gradient Descent](https://en.wikipedia.org/wiki/Stochastic_gradient_descent) is one of the most popular *optimizers* in machine learning applications.
Given a stochastic estimate of the gradient of the cost function ($$ G(\mathbf{p}) $$), it performs the update:

$$
p^\prime_k = p_k -\eta G_k(\mathbf{p}),
$$

where $$ \eta $$ is the so-called learning rate. NetKet also implements two extensions to the simple SGD, the first one is $$ L_2 $$ regularization,
and the second one is the possibility to set a decay factor $$ \gamma \leq 1 $$ for the learning rate, such that at iteration $$ n $$ the learning rate is $$ \eta \gamma^n $$.  

The Stochastic Gradient Descent optimizer can be chosen specifying `Name`:`Sgd` in pars[`Optimizer`].

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `DecayFactor` | Float |  The decay factor $$ \gamma $$  | 1 |
| `LearningRate` | Float $$ \leq 1 $$ |  The learning rate $$ \eta $$  | None |
| `L2Reg` | Float $$ \geq 0 $$ |  The amount of $$ L_2 $$ regularization  | 0 |
|===


### Example
```python
pars['Optimizer']={
    ...
    'Name'    : 'Sgd',
    'LearningRate'   : 0.01,
    ...
}
```

<h2 class="bg-primary">AdaMax</h2>

NetKet implements AdaMax, an adaptive stochastic gradient descent method, and a variant of [Adam](https://arxiv.org/pdf/1412.6980.pdf) based on the infinity norm.
In contrast to the SGD, AdaMax offers the important advantage of being much less sensitive to the choice of the hyper-parameters (for example, the learning rate).

Given a stochastic estimate of the gradient of the cost function ($$ G(\mathbf{p}) $$), AdaMax performs an update:

$$
p^\prime_k = p_k + \mathcal{S}_k,
$$

where $$ \mathcal{S}_k $$ implicitly depends on all the history of the optimization up to the current point.
The NetKet naming convention of the parameters strictly follows the one introduced by the authors of AdaMax.
For an in-depth description of this method, please refer to Reference 1 (Algorithm 2 therein).

The AdaMax optimizer can be chosen by specifying `Name`:`AdaMax` in pars[`Optimizer`].

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `Alpha` | Float |  The step size  | 0.001 |
| `Beta1` | Float $$ \in [0,1] $$ | First exponential decay rate | 0.9 |
| `Beta2` | Float $$ \in [0,1] $$ |  Second exponential decay rate | 0.999 |
|===

### Example
```python
pars['Optimizer']={
    ...
    'Name'    : 'AdaMax',
    'Alpha'   : 0.01,
    ...
}
```
<h2 class="bg-primary">Momentum</h2>
The momentum update incorporates an exponentially weighted moving average over previous gradients to speed up descent [2]. The momentum vector $$\mathbf{m}$$ is initialized to zero. Given a stochastic estimate of the gradient of the cost function $$G(\mathbf{p})$$, the updates for the parameter $$p_k$$ and corresponding component of the momentum $$m_k$$ are

$$
\begin{aligned}
m^\prime_k &= \beta m_k + (1-\beta)G_k(\mathbf{p})\\
p^\prime_k &= \eta m^\prime_k
\end{aligned}
$$

The Momentum optimizer can be chosen by specifying `Name`:`Momentum` in pars[`Optimizer`].

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `LearningRate` | Float $$ \leq 1 $$ |  The learning rate $$ \eta $$  | 0.001 |
| `Beta` | Float $$ \in [0,1] $$ | Momentum exponential decay rate | 0.9 |
|===

### Example
```python
pars['Optimizer']={
    ...
    'Name'    : 'Momentum',
    'LearningRate'   : 0.01,
    ...
}
```

<h2 class="bg-primary">AdaGrad</h2>
In many cases, the learning rate $$\eta$$ should decay as a function of training iteration to prevent overshooting as the optimum is approached. AdaGrad [3] is an adaptive learning rate algorithm that automatically scales the learning rate with a sum over past gradients. The vector $$\mathbf{g}$$ is initialized to zero. Given a stochastic estimate of the gradient of the cost function $$G(\mathbf{p})$$, the updates for $$g_k$$ and the parameter $$p_k$$ are

$$
\begin{aligned}
g^\prime_k &= g_k + G_k(\mathbf{p})^2\\
p^\prime_k &= p_k - \frac{\eta}{\sqrt{g_k + \epsilon}}G_k(\mathbf{p})
\end{aligned}
$$

AdaGrad has been shown to perform particularly well when the gradients are sparse, but the learning rate may become too small after many updates because the sum over the squares of past gradients is cumulative.

The AdaGrad optimizer can be chosen by specifying `Name`:`AdaGrad` in pars[`Optimizer`].

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `LearningRate` | Float $$ \leq 1 $$ |  The learning rate $$ \eta $$  | 0.001 |
|===

### Example
```python
pars['Optimizer']={
    ...
    'Name'    : 'AdaGrad',
    'LearningRate'   : 0.01,
    ...
}
```

<h2 class="bg-primary">RMSProp</h2>
RMSProp is a well-known update algorithm proposed by Geoff Hinton in his Neural Networks course notes [4]. It corrects the problem with AdaGrad by using an exponentially weighted moving average over past squared gradients instead of a cumulative sum. After initializing the vector $$\mathbf{s}$$ to zero, $$s_k$$ and the parameters $$p_k$$ are updated as

$$
\begin{align}
s^\prime_k = \beta s_k + (1-\beta) G_k(\mathbf{p})^2 \\
p^\prime_k = p_k - \frac{\eta}{\sqrt{s_k}+\epsilon} G_k(\mathbf{p})
\end{align}
$$

The RMSProp optimizer can be chosen by specifying `Name`:`RMSProp` in pars[`Optimizer`].

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `LearningRate` | Float $$ \leq 1 $$ |  The learning rate $$ \eta $$  | 0.001 |
| `Beta` | Float $$ \in [0,1] $$ | Exponential decay rate | 0.9 |
|===

### Example
```python
pars['Optimizer']={
    ...
    'Name'    : 'RMSProp',
    'LearningRate'   : 0.01,
    ...
}
```


<h2 class="bg-primary">AdaDelta</h2>
Like RMSProp, AdaDelta [5] corrects the monotonic decay of learning rates associated with AdaGrad, while additionally eliminating the need to choose a global learning rate $$ \eta $$. The NetKet naming convention of the parameters strictly follows the one introduced in Ref. 5; here $$E[g^2]$$ is equivalent to the vector $$\mathbf{s}$$ from RMSProp. $$E[g^2]$$ and $$E[\Delta x^2]$$ are initialized as zero vectors.

$$
\begin{align}
E[g^2]^\prime_k &= \rho E[g^2] + (1-\rho)G_k(\mathbf{p})^2\\
\Delta p_k &= - \frac{\sqrt{E[\Delta x^2]+\epsilon}}{\sqrt{E[g^2]+ \epsilon}}G_k(\mathbf{p})\\
E[\Delta x^2]^\prime_k &= \rho E[\Delta x^2] + (1-\rho)\Delta p_k^2\\
p^\prime_k &= p_k + \Delta p_k\\
\end{align}
$$

The AdaDelta optimizer can be chosen by specifying `Name`:`AdaDelta` in pars[`Optimizer`].

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `Rho` | Float $$ \in [0,1] $$ | Exponential decay rate | 0.95 |
|===

### Example
```python
pars['Optimizer']={
    ...
    'Name'    : 'AdaDelta',
    'Rho'   : 0.9,
    ...
}
```


<h2 class="bg-primary">AMSGrad</h2>
In some cases, adaptive learning rate methods such as AdaMax fail to converge to the optimal solution because of the exponential moving average over past gradients. To address this problem, Sashank J. Reddi, Satyen Kale and Sanjiv Kumar proposed the AMSGrad update algorithm [6]. The update rule for $$\mathbf{v}$$ (equivalent to $$E[g^2]$$ in AdaDelta and $$\mathbf{s}$$ in RMSProp) is modified such that $$v^\prime_k \geq v_k$$ is guaranteed, giving the algorithm a "long-term memory" of past gradients. The vectors $$\mathbf{m}$$ and $$\mathbf{v}$$ are initialized to zero, and are updated with the parameters $$\mathbf{p}$$:

$$
\begin{aligned}
m^\prime_k &= \beta_1 m_k + (1-\beta_1)G_k(\mathbf{p})\\
v^\prime_k &= \beta_2 v_k + (1-\beta_2)G_k(\mathbf{p})^2\\
v^\prime_k &= \mathrm{Max}(v^\prime_k, v_k)\\
p^\prime_k &= p_k - \frac{\eta}{\sqrt{v^\prime_k}+\epsilon}m^\prime_k
\end{aligned}
$$

The AMSGrad optimizer can be chosen by specifying `Name`:`AMSGrad` in pars[`Optimizer`].

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `LearningRate` | Float $$ \leq 1 $$ |  The learning rate  | 0.001 |
| `Beta1` | Float $$ \in [0,1] $$ | First exponential decay rate | 0.9 |
| `Beta2` | Float $$ \in [0,1] $$ |  Second exponential decay rate | 0.999 |
|===

### Example
```python
pars['Optimizer']={
    ...
    'Name'    : 'AMSGrad',
    'LearningRate'   : 0.01,
    ...
}
```

## References
---------------
[1] [Kingma, D., & Ba, J. (2015). Adam: a method for stochastic optimization](https://arxiv.org/pdf/1412.6980.pdf)

[2] [Qian, N. (1999) On the momentum term in gradient descent learning algorithms](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.57.5612&rep=rep1&type=pdf)

[3] [Hinton, G. Lecture 6a Overview of mini-batch gradient descent](http://www.cs.toronto.edu/~tijmen/csc321/slides/lecture_slides_lec6.pdf)

[4] [Duchi, J., Hazan, E., & Singer, Y. (2011). Adaptive subgradient methods for online learning and stochastic optimization](www.jmlr.org/papers/volume12/duchi11a/duchi11a.pdf)

[5] [Zeiler, M. D. (2012). ADADELTA: an adaptive learning rate method](http://arxiv.org/abs/1212.5701)

[6] [Reddi, S., Kale, S., & Kumar, S. (2018) On the convergence of Adam and beyond](https://openreview.net/forum?id=ryQu7f-RZ)
