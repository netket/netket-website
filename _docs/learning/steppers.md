---
title: Steppers
permalink: /docs/steppers/
---

The vast majority of learning applications solves the associated high-dimensional optimization problem in an iterative way.

More formally, given a cost function $$ F(\mathbf{p}) $$ to be minimized, depending on a set of $$ \mathbf{p} = p_1 \dots p_M $$,
then at each step of the optimization, we perform a change in the parameters:

$$
p^\prime_k = p_k + \mathcal{S}_k,
$$

i.e. each component is updated with a variation $$ \mathcal{S}_k $$ depending on the current/past set of parameters, and on the cost function $$ F $$.
Typically, but not exclusively, $$ \mathcal{S} $$ contains information directly related to the gradient of $$ F $$.

NetKet implements a series of *steppers*, suitable for situations where the gradient of $$ F $$ (and $$ F $$ itself) is known only stochastically.
Steppers must be used in conjunction with one of the available learning Methods, specifying the field `StepperType` in the `Learning` section of the input (see for example [here](../stochastic_reconfiguration/)).


<h2 class="bg-primary">Stochastic Gradient Descent</h2>

The [Stochastic Gradient Descent](https://en.wikipedia.org/wiki/Stochastic_gradient_descent) is one of the most popular *steppers* in machine learning applications.
Given a stochastic estimate of the gradient of the cost function ($$ G(\mathbf{p}) $$), it performs the update:

$$
p^\prime_k = p_k -\eta G_k(\mathbf{p}),
$$

where $$ \eta $$ is the so-called learning rate. NetKet also implements two extensions to the simple SGD, the first one is $$ L_2 $$ regularization,
and the second one is the possibility to set a decay factor $$ \gamma \leq 1 $$ for the learning rate, such that at iteration $$ n $$ the learning rate is $$ \eta \gamma^n $$.  

The Stochastic Gradient Descent can be chosen specifying `Sgd` as a `StepperType`.

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `DecayFactor` | Float |  The decay factor $$ \gamma $$  | 1 |
| `LearningRate` | Float $$ \leq 1 $$ |  The learning rate $$ \eta $$  | None |
| `L2Reg` | Float $$ \geq 0 $$ |  The amount of $$ L_2 $$ regularization  | 0 |
|===


### Example
```python
pars['Learning']={
    ...
    'StepperType'    : 'Sgd',
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

The Stochastic Gradient Descent can be chosen specifying `AdaMax` as a `StepperType`.

|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `Alpha` | Float |  The step size  | 0.001 |
| `Beta1` | Float $$ \in [0,1] $$ | First exponential decay rate | 0.9 |
| `Beta2` | Float $$ \in [0,1] $$ |  Second exponential decay rate | 0.999 |
|===

### Example
```python
pars['Learning']={
    ...
    'StepperType'    : 'AdaMax',
    'Alpha'   : 0.01,
    ...
}
```

## References
---------------
1. [Kingma, D., & Ba, J. (2015). Adam: a method for stochastic optimization](https://arxiv.org/pdf/1412.6980.pdf)
