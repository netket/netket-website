---
title: Custom Observables
permalink: /docs/custom_observables/
---

NetKet provides the freedom to define user's defined Observables, which are measured during the learning procedure.
Custom Observables follow the same concepts discussed for
[custom Hamiltonians]({{ site.baseurl }}{% link _docs/hamiltonians/custom_hamiltonians.md %}).
It is possible to add an observable specifying the relevant operators
in the `Observables` section of the input.
For the moment, this functionality is limited to
lattice observables which are sums of $$ k $$ -local operators:

$$
\mathcal{O}= \sum_i o_i,
$$

where the operators $$ o_i $$ act on an (arbitrary) subset of sites. In order to define your custom
Observable, you need to specify the operators $$ o_i $$. Notice here the Hilbert space is derived from the definition of
the Hamiltonian, and Observables compatible with the Hamiltonian Hilbert space must be declared by the user.


<h2 class="bg-primary">Local Operators</h2>
The local operators $$ o_i $$ are specified giving their matrix elements, and a list of sites on which they act.
For example, to specify a single-site operator acting on site $$ l$$, and with a local Hilbert space of two elements $$ n_1, n_2 $$,
you must provide a $$ 2 \times 2 $$ matrix

$$
\left(\begin{array}{cc}
\langle n_{1}|o|n_{1}\rangle & \langle n_{2}|o|n_{1}\rangle\\
\langle n_{1}|o|n_{2}\rangle & \langle n_{2}|o|n_{2}\rangle
\end{array}\right)
$$

In general, for a $$ k $$-local operator acting on local Hilbert spaces with $$ b $$ quantum numbers,
you must provide a $$ b^k \times b^k $$ matrix

$$
\left(\begin{array}{cccc}
\langle n_{1}n_{1}\dots n_{1}|o|n_{1}n_{1}\dots n_{1}\rangle & \langle n_{1}n_{1}\dots n_{1}|o|n_{1}n_{1}\dots n_{2}\rangle & \cdots & \langle n_{1}n_{1}\dots n_{1}|o|n_{b}n_{b}\dots n_{b}\rangle\\
\langle n_{1}n_{1}\dots n_{2}|o|n_{1}n_{1}\dots n_{1}\rangle & \langle n_{1}n_{1}\dots n_{2}|o|n_{1}n_{1}\dots n_{2}\rangle & \cdots & \langle n_{1}n_{1}\dots n_{2}|o|n_{b}n_{b}\dots n_{b}\rangle\\
\vdots & \vdots & \ddots & \vdots\\
\langle n_{b}n_{b}\dots n_{b}|o|n_{1}n_{1}\dots n_{1}\rangle & \langle n_{b}n_{b}\dots n_{b}|o|n_{1}n_{1}\dots n_{2}\rangle & \cdots & \langle n_{b}n_{b}\dots n_{b}|o|n_{b}n_{b}\dots n_{b}\rangle
\end{array}\right)
$$


|---
| Parameter | Possible values | Description | Default value |
|-|-|-|-
| `ActingOn` | List of list of integers  |  The sites on which each $$ o_i $$ acts on | None |
| `Name` | String |  Chosen name of the observable | None |
| `Operators` | List of floating/complex matrices |  For each $$ i $$, the matrix elements of $$ o_i $$ in the $$ k $$-local Hilbert space | None |
|===

### Example
```python

sigmaxop=[]
sites=[]
for i in range(L):
    #\sum_i sigma^x(i)
    sigmaxop.append([[0,1],[1,0]])
    sites.append([i])

pars['Observables']={
    'Operators'      : sigmaxop,
    'ActingOn'       : sites,
    'Name'           : 'SigmaX',
}

```


## References
---------------
1. [Carleo, G., & Troyer, M. (2017). Solving the quantum many-body problem with artificial neural networks. Science, 355 602](http://science.sciencemag.org/content/355/6325/602)
