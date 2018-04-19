---
title: Custom Machines
permalink: /docs/custom_machines/
---

In addition to [Built-in machines]({{ site.baseurl }}{% link _docs/machines/rbm.md %})  NetKet
can be extended with user-defined custom machines.

At variance with custom [Graphs]({{ site.baseurl }}{% link _docs/graphs/custom_graphs.md %})
and custom [Hamiltonians]({{ site.baseurl }}{% link _docs/hamiltonians/custom_hamiltonians.md %}),
providing a new machine requires some coding in C++.

Specifically, your machine must be derived from the base abstract class in `Machines/abstract_machine.hh`,
which provides prototypes for the pure virtual methods to be implemented. All the key methods in there are commented
with the requirements each method should fulfill.

### Example
For example, if you wanted to use a fully-visible Boltzmann machine (a.k.a. Jastrow wave-function) in NetKet, one of the
key methods that you would need to implement is the one computing the logarithm of the wave-function
for a given visible vector. Assuming that the wave-function takes the form:

$$
\Psi(s_1 \dots s_N) = \exp \left( \sum_{i<j} W_{ij} s_i s_j \right),
$$

then you would have to implement the method:

```c++
T LogVal(const VectorXd & v){
   T logpsi=0;

   for(int i=0;i<v.size();i++){
     for(int j=i+1;j<v.size();j++){
       logpsi+=W(i,j)*v(i)*v(j);
     }
   }
   return logpsi;
}
```

### Summing up
The steps to be followed are then:

1. Write your own machine, say `Machines/new_machine.hh` taking care of implementing all the methods prototyped in `Machines/abstract_machine.hh`
2. Include its declaration in `Machines/machines.hh`
3. Add it to `Machines/machines.cc` to make use of the JSON input infrastructure

In future releases of NetKet, we plan to provide more automatic ways of defining custom machines.
Any suggestion on how to implement this (or, better, motivated people to implement this functionality) are more than welcome!
