# HOOMD-blue example notebooks

These [jupyter](https://jupyter.org) notebooks provide a tutorial for the
[HOOMD-blue](https://glotzerlab.engin.umich.edu/hoomd-blue) simulation software
and are included in [HOOMD-blue's
documentation](http://hoomd-blue.readthedocs.io).

## Tutorials

* [Introducing HOOMD-blue](00-Introducing-HOOMD-blue/index.ipynb)
* [Introducing Molecular Dynamics](01-Introducing-Molecular-Dynamics/index.ipynb)

## Executing the examples

You can [install HOOMD-blue](https://hoomd-blue.readthedocs.io) and run these
examples interactively.

Clone the **hoomd-examples** repository and start **jupyter notebook**

```bash
$ git clone https://github.com/glotzerlab/hoomd-examples
$ cd hoomd-examples
$ jupyter notebook
```

## Prerequisites

These examples use the following python packages:

* [fresnel](https://github.com/glotzerlab/fresnel)
* [freud](http://glotzerlab.engin.umich.edu/freud/)
* [GSD](https://github.com/glotzerlab/gsd)
* [HOOMD-blue](http://glotzerlab.engin.umich.edu/hoomd-blue/)
* [jupyter](http://jupyter.org/)
* [matplotlib](http://matplotlib.org/)
* [pillow](https://python-pillow.org/)

Anaconda users can install these from [conda-forge](https://conda-forge.org/):

```bash
conda install -c conda-forge fresnel freud  gsd hoomd jupyter matplotlib
```
