---
title: Compiling
permalink: /getstarted/compiling/
---

Once you have fulfilled the necessary steps to get the [required libraries](../requirements/), you are just one step away from fully enjoying NetKet.

Download the latest stable version (<a href="{{site.latest_release.zip}}" download>zip</a> or <a href="{{site.latest_release.gz}}" download>tar.gz </a>), and unzip the content in a folder of your choice.

At this point, move to the NetKet folder and trigger the build using `CMake`

```shell
mkdir build && cd build && cmake .. && make -j
```

which will generate the executable file `netket` in the `/build` directory.

Optionally, you can also permanently install the `netket` executable doing

```shell
make install
```

Congratulations now, you have installed NetKet!
