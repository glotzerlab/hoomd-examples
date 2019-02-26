# HOOMD-blue example notebooks

These [jupyter](https://jupyter.org) notebooks provide a tutorial for the
[HOOMD-blue](https://glotzerlab.engin.umich.edu/hoomd-blue) simulations software. Static versions will be included in
a future version of [HOOMD-blue's documentation](http://hoomd-blue.readthedocs.io).

## Index

### Basic tutorials

Basic tutorials introduce the user to the essential elements of a HOOMD simulation via short examples with extended descriptions. Later example scripts may assume that the user is familiar with these concepts and do not to re-introduce
them.

* [Introduction](00-Basic-tutorials/00-Introduction.ipynb)
* [Executing scripts](00-Basic-tutorials/01-Executing-scripts.ipynb)
* [Introducing contexts](00-Basic-tutorials/02-Introducing-contexts.ipynb)
* [Specifying the initial condition](03-Basic-tutorials/02-Specifying-the-initial-condition.ipynb)
* [MD simulations](00-Basic-tutorials/04-MD-simulations.ipynb)
* [HPMC simulations](00-Basic-tutorials/05-HPMC-simulations.ipynb)
* [Log file output](00-Basic-tutorials/06-Log-file-output.ipynb)
* [Trajectory output](00-Basic-tutorials/07-Trajectory-output.ipynb)
* [Saving trajectory metadata](00-Basic-tutorials/08-Saving-trajectory-metadata.ipynb)
* [Visualizing trajectories](00-Basic-tutorials/09-Visualizing-trajectories.ipynb)

### Research examples

Examples demonstrate research-relevant use cases of HOOMD with simple, easy-to-understand code, along with extensive
descriptions and a link to the research paper.

* [Active rotation](01-Research-examples/00-Active-rotation.ipynb)

### Guides

A how-to guide demonstrates a specific HOOMD feature as succinctly as possible with brief explanations.

* TODO: Populate

### External tools

Guides that demonstrate how to use HOOMD-blue in conjunction with other tools.

* TODO: Populate

## Executing the examples
You can [install HOOMD-blue](https://hoomd-blue.readthedocs.io) and run these examples
interactively. Different installation methods require different steps to launch.

These examples use the following python packages. If you do not have the packages installed, some or all of the examples
will fail to execute:

* [HOOMD-blue](http://glotzerlab.engin.umich.edu/hoomd-blue/)
* [Jupyter](http://jupyter.org/)
* [GSD](https://github.com/glotzerlab/gsd)
* [matplotlib](http://matplotlib.org/)
* [freud](http://glotzerlab.engin.umich.edu/freud/)
* [fresnel](https://github.com/glotzerlab/fresnel)
* [pillow](https://python-pillow.org/)

Anaconda users can install all of these from [conda-forge](https://conda-forge.org/):

```bash
conda install -c conda-forge hoomd jupyter gsd matplotlib freud fresnel
```

### Host installation (from source or anaconda package)

Clone the **hoomd-examples** repository and start **jupyter notebook**

```bash
▶ git clone https://github.com/glotzerlab/hoomd-examples
▶ cd hoomd-examples
▶ jupyter notebook
```

### Singularity container

Clone the **hoomd-examples** repository.

```bash
▶ git clone https://github.com/glotzerlab/hoomd-examples
▶ cd hoomd-examples
```

The image contains all software needed to execute these notebooks. Use singularity to launch the container:

```bash
▶ singularity exec -B $XDG_RUNTIME_DIR software.simg jupyter notebook
```

Add ``--nv`` after exec to utilize GPUs.

Explanation:

* ``singularity exec`` - Ask singularity to execute a command in a container.
* ``-B $XDG_RUNTIME_DIR`` - Bind mount your user specific temporary director. Jupyter uses this directory and
  singularity does not mount it by default.
* ``software.simg`` - The image to launch.
* ``jupyter notebook`` Execute ``jupyter notebook`` inside the image

Once **jupyter** starts, point your browser to the URL **jupyter** prints on the terminal. **jupyter** inside the
container accesses the configuration in your home directory on the host system. If you have a password configured for
**jupyter** on your host system, use that to login. Otherwise, the URL should include a token that will log you in.

### Docker container

The **glotzerlab/software** image contains all software needed to execute these notebooks and a copy of the notebooks
themselves in ``/hoomd-examples``. Run this command to start **jupyter**:

```bash
▶ docker run --rm -p 127.0.0.1:9999:9999 glotzerlab/software jupyter notebook --port 9999 --ip 0.0.0.0 --no-browser /hoomd-examples
```

If you have installed the docker NVIDIA runtime, add ``--runtime=nvidia`` after ``run`` to utilize your GPUs.

Explanation:

* ``docker run`` - Ask docker to run a command in a container.
* ``--runtime=nvidia`` - (if applicable) use the NVIDIA runtime to make host GPUS accessible in the container.
* ``--rm`` - Delete the container after exiting.
* ``-p 127.0.0.1:9999:9999`` - Make port 9999 in the container available at ``localhost:9999``.
* ``glotzerlab/software`` - name of the image to execute.
* ``jupyter notebook`` - execute the **jupyter** notebook.
* ``--port 9999 --ip 0.0.0.0`` - **jupyter** should listen on port 9999 for connections from outside the container.
* ``--no-browser`` - Tell Jupyter not to attempt to launch a browser.
* ``/hoomd-examples`` - Location of the example notebooks in the image.

Once **jupyter** starts, point your browser to ``localhost:9999``. Copy the token from the **jupyter** terminal output
and paste it into the password box to access the notebook.
