---
title: Introduction
permalink: /docs/machines_introduction/
---

One of the key components of machine-learning simulations for quantum many-body systems are certainly the *machines*.
In NetKet, artificial neural networks are used to parametrize the many-body wave-function, as introduced in Reference (1).

Generally speaking, a machine is a high-dimensional (typically non-linear) function

$$
\Psi(s_1 \dots s_N; \mathbf{p})
$$

of the quantum numbers $$ s_1 \dots s_N $$ that define the many-body
quantum system, and depending on a set of parameters $$ \mathbf{p} \equiv p_1 \dots p_M $$.

NetKet ships with several state-of-the-art implementations of [Restricted Boltzmann Machines]({{ site.baseurl }}{% link _docs/machines/rbm.md %}).
Custom machines can be also provided by the user, following the steps described [here]({{ site.baseurl }}{% link _docs/machines/custom_machines.md %}).
Future versions of NetKet will provide users with a larger choice of built-in machines.
See also our [Challenges]({{ "/challenges/home/" | prepend: site.baseurl }}), if you would like to contribute to the developments in these directions.


Compact parametrizations of the wave-function in terms of artificial neural networks can be used to find the ground-state of a many-body Hamiltonian (see also Ref. (2) for additional details).
The algorithms to perform this learning task, as implemented in NetKet, are described in the [Learning the Ground State](../stochastic_reconfiguration/) section.

In addition to finding the ground-state of a given Hamiltonian, there are other learning tasks that can be performed using the machines implemented in NetKet.
For example, supervised learning with *Born machines* (3,4), or unsupervised learning to perform state-reconstruction (5).

The corresponding learning algorithms will be implemented in future versions of NetKet. See also our [Challenges]({{ "/challenges/home/" | prepend: site.baseurl }}), if you would like to contribute to the developments in these directions.

## References
---------------

1. [Carleo, G., & Troyer, M. (2017). Solving the quantum many-body problem with artificial neural networks. Science, 355 602](http://science.sciencemag.org/content/355/6325/602)
2. [Carleo, G. (2017). Lecture notes for the Advanced School on Quantum Science and Quantum technology.](https://gitlab.com/nqs/ictp_school/blob/7ff4fcc22a1685fec0972f291919090c79586012/notes.pdf)
3. [Stoudenmire, M., & Schwab, D. (2016). Supervised Learning with Quantum-Inspired Tensor Networks. Advances in Neural Information Processing Systems 29, 4799](https://arxiv.org/abs/1605.05775)
4. [Cheng, S., Chen J., & Wang L. (2017). Information Perspective to Probabilistic Modeling: Boltzmann Machines versus Born Machines.](https://arxiv.org/abs/1712.04144)
5. [Torlai, G. et al. (2018). Neural-network quantum state tomography. Nature Physics doi:10.1038/s41567-018-0048-5](https://www.nature.com/articles/s41567-018-0048-5)
