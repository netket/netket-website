---
title: Introduction
permalink: /docs/learning_introduction/
---

A central task in machine learning applications for quantum many-body applications is certainly
the *learning* part. Loosely speaking, learning refers to a high-dimensional (and typically non-linear) optimization of
the parameters entering a machine, in order to solve a certain task.

NetKet implements learning algorithms to find the ground-state of a given many-body quantum Hamiltonian $$ \mathcal{H} $$, see references (1,2).
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
