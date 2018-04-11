---
title: Writing New Code
permalink: /docs/write_new/
---


This library is meant to provide a basic infrastructure on which to develop and use new Machines/Hamiltonians/Learning methods etc.

### Defining a new Machine
Machines are prototyped as an abstract class in `Machines/abstract_machines.hh` where the virtual methods that a generic machine should implement are declared. To write a new machine, you should inherit from this class. To use the newly defined machine, you should then
1. Include its declaration in `Machines/machines.hh`
2. Add it to `Machines/machines.cc` to make use of the Json input infrastructure
