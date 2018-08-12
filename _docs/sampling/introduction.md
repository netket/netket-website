---
title: Introduction
permalink: /docs/sampling_introduction/
---

A central task in several learning applications is the ability to sample from a given machine.
For example, in the variational learning one samples quantum numbers $$ s_1\dots s_N $$
from the probability distribution given by the square modulus of the wave-function:

$$
P(s_1\dots s_N) = |\Psi(s_1\dots s_N) | ^2.
$$


NetKet implements several local [Metropolis-Hastings](https://en.wikipedia.org/wiki/Metropolis–Hastings_algorithm) moves.
In this case, the sampler transits from the current set of quantum numbers $$ \mathbf{s} = s_1 \dots s_N $$ to another set $$ \mathbf{s^\prime} = s^\prime_1 \dots s^\prime_N $$. Samplers are then fully specified by the transition probability:

$$
T( \mathbf{s} \rightarrow \mathbf{s}^\prime) .
$$

The [local samplers](../metropolis_local/) implemented in NetKet propose to modify only a limited set of quantum numbers at the time. [Hamiltonian sampler](../metropolis_hamiltonian/) instead use the off-diagonal elements of the Hamiltonian to construct the transition matrix. For more customized applications, arbitrary sampling strategies based on set of local operators can also be defined in NetKet. This is achieved specifying a set of local stochastic transition operators, as explained in [Custom samplers](../custom_sampling/). 

Most samplers can also be used with [parallel-tempering](https://en.wikipedia.org/wiki/Parallel_tempering) moves. In this case, one effectively samples from the a set of probability distributions

$$
P_\beta(s_1\dots s_N) \equiv P^\beta(s_1\dots s_N),
$$

each associated to an inverse *temperature* $$ 1 \leq \beta_k \leq 0 $$. During the sampling, configurations at different
*temperatures* are exchanged, to increase ergodicity. Only quantum numbers sampled from $$ \beta =1 $$ (corresponding to the original probability distribution) are retained
to compute the required expectation values.

Inverse temperatures are chosen according to the simple form $$ \beta_k = 1 - k/N_{\mathrm{rep}} $$,
where $$ N_{\mathrm{rep}} $$ is a user-supplied number specifying how many temperatures are to be taken.
Upon increasing the number of temperatures (or replicas, in the jargon) one can improve the sampling efficiency.

The samplers described below can be used for any quantum system with a local (and finite) discrete Hilbert space.
