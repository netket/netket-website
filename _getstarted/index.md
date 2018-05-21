---
title: Get Started
permalink: /getstarted/home/
redirect_from: /getstarted/index.html
layout: default
---
<br>
<div class="container">
  <div id="markdown-content-container">

<div class="row" >
  <div class="col-sm-5">
    <div class="jumbotron">
    <h2 class="text-center">Quick Start</h2>
    <div class="text-center">
    <p class="text-muted"> for the impatient</p>
    </div>
    </div>
  </div>
  <div class="col-sm-7">
    <ol class="list-group">
       <libullet class="list-group-item" markdown="span">Make sure you have [CMake](https://cmake.org), a working [MPI](https://www.open-mpi.org) compiler and a [Python](https://www.python.org) interpreter. </libullet>
       <libullet class="list-group-item">Download NetKet (<a href="{{site.latest_release.zip}}" download>zip</a> or <a href="{{site.latest_release.gz}}" download>tar.gz </a>).</libullet>
       <libullet class="list-group-item">Go to the unzipped NetKet folder.</libullet>
       <libullet class="list-group-item" markdown="span">`mkdir build && cd build && cmake .. && make -j && make install`</libullet>
       <libullet class="list-group-item" markdown="span">Explore our [Tutorials]({{ "/tutorials/home/" | prepend: site.baseurl }}).</libullet>
    </ol>
  </div>
</div>
<br>
<div class="row" >
  <div class="col-sm-5">
    <div class="jumbotron">
    <h2 class="text-center">More Details</h2>
    <div class="text-center">
    <p class="text-muted"> for everybody</p>
    </div>
    </div>
  </div>
  <div class="col-sm-7">
    <ol class="list-group">
       <libullet class="list-group-item" markdown="span">Find out the [requirements](../requirements/).</libullet>
       <libullet class="list-group-item" markdown="span">Find out how to [compile](../compiling/) NetKet.</libullet>
       <libullet class="list-group-item" markdown="span">Explore our [Tutorials]({{ "/tutorials/home/" | prepend: site.baseurl }}).</libullet>
       <libullet class="list-group-item" markdown="span">Set up your custom [Graph]({{ site.baseurl }}{% link _docs/graphs/custom_graphs.md %}),[Hamiltonian]({{ site.baseurl }}{% link _docs/hamiltonians/custom_hamiltonians.md %}),
       [Machine]({{ site.baseurl }}{% link _docs/machines/custom_machines.md %}), [Observable]({{ site.baseurl }}{% link _docs/observables/custom_observables.md %}), and more.</libullet>
       <libullet class="list-group-item" markdown="span">Get involved, pick your own [Challenge]({{ site.baseurl }}{% link _challenges/index.md %}).</libullet>
    </ol>
  </div>
</div>

</div>
</div>
