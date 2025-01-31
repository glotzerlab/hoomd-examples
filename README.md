# HOOMD-blue tutorials

These [jupyter] notebooks provide a tutorial for the [HOOMD-blue] simulation software and are
included in HOOMD-blue's [documentation].

[jupyter]: https://jupyter.org
[HOOMD-blue]: https://glotzerlab.engin.umich.edu/hoomd-blue
[documentation]: http://hoomd-blue.readthedocs.io

## Outline

* [Introducing HOOMD-blue](00-Introducing-HOOMD-blue/00-index.ipynb)
* [Introducing Molecular Dynamics](01-Introducing-Molecular-Dynamics/00-index.ipynb)
* [Logging](02-Logging/00-index.ipynb)
* [Parallel Simulations With MPI](03-Parallel-Simulations-With-MPI/00-index.ipynb)
* [Custom Actions In Python](04-Custom-Actions-In-Python/00-index.ipynb)
* [Organizing and Executing Simulations](05-Organizing-and-Executing-Simulations/00-index.ipynb)
* [Modelling Rigid Bodies](06-Modelling-Rigid-Bodies/00-index.ipynb)
* [Modelling Patchy Particles](07-Modelling-Patchy-Particles/00-index.ipynb)
* [Multiparticle Collision Dynamics](09-Multiparticle-Collision-Dynamics/00-index.ipynb)

## Executing the tutorials

You can [install HOOMD-blue] and run these examples interactively.

[install HOOMD-blue]: http://hoomd-blue.readthedocs.io

Clone the **hoomd-examples** repository and open the notebooks with the tool you
prefer.

## Prerequisites

These examples use the following python packages:

* [fresnel](https://github.com/glotzerlab/fresnel)
* [freud](http://glotzerlab.engin.umich.edu/freud/)
* [GSD](https://github.com/glotzerlab/gsd)
* [HOOMD-blue](http://glotzerlab.engin.umich.edu/hoomd-blue/)
* [matplotlib](http://matplotlib.org/)
* [pillow](https://python-pillow.org/)
* [signac](https://signac.readthedocs.io/)
* [signac-flow](https://signac.readthedocs.io/)

You can install these from [conda-forge](https://conda-forge.org/):

```bash
micromamba install fresnel freud gsd hoomd matplotlib pillow signac signac-flow
```
