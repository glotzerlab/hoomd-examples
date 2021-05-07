# HOOMD-blue tutorials

These [jupyter] notebooks provide a tutorial for the [HOOMD-blue] simulation software and are
included in HOOMD-blue's [documentation].

[jupyter]: https://jupyter.org
[HOOMD-blue]: https://glotzerlab.engin.umich.edu/hoomd-blue
[documentation]: http://hoomd-blue.readthedocs.io

## Outline

* [Introducing HOOMD-blue](00-Introducing-HOOMD-blue/index.ipynb)
* [Introducing Molecular Dynamics](01-Introducing-Molecular-Dynamics/index.ipynb)
* [Logging](02-Logging/index.ipynb)

## Executing the tutorials

You can [install HOOMD-blue] and run these examples interactively.

[install HOOMD-blue]: http://hoomd-blue.readthedocs.io

Clone the **hoomd-examples** repository and start **jupyter notebook**

```bash
$ git clone https://github.com/glotzerlab/hoomd-examples
$ cd hoomd-examples
$ jupyter lab
```

## Prerequisites

These examples use the following python packages:

* [fresnel](https://github.com/glotzerlab/fresnel)
* [freud](http://glotzerlab.engin.umich.edu/freud/)
* [GSD](https://github.com/glotzerlab/gsd)
* [HOOMD-blue](http://glotzerlab.engin.umich.edu/hoomd-blue/)
* [jupyterlab](http://jupyterlab.io/)
* [matplotlib](http://matplotlib.org/)
* [pillow](https://python-pillow.org/)

Anaconda users can install these from [conda-forge](https://conda-forge.org/):

```bash
conda install -c conda-forge fresnel freud  gsd hoomd jupyterlab matplotlib
```
