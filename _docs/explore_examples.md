---
title: Explore the Examples
permalink: /docs/explore_examples/
---

Once you successfully compile the main executable, you can start using the code, and explore the available examples. Move to the folder `Examples/` where you will find a few physical systems on which you can test the power of neural-network quantum states.

### Running an example
In `chosen_example.py` (say `heisenberg1d.py` in `Examples/Heisenberg1d/`)  you will find a series of parameters you can set to run NetKet. Once you have tuned at will those parameters, you should just invoke `python chosen_example.py` and follow the instructions printed there. Basically, this will generate a `.json` input file that you can feed to the `netket.o` executable we have generated during compilation. Most of the examples come with visualization aids, and while the code is running you can have a live plot the energy during the learning procedure just calling the corresponding script (say `python plot_heis.py`, for the Heisenberg model in 1D). Those scripts are also meant to familiarize you with the output system (in `Json`) of NetKet.
