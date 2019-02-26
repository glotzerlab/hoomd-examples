# Contributing to hoomd-examples

## New examples

Contributions are welcomed via [pull requests on GitHub](https://github.com/glotzerlab/hoomd-examples/pulls).
Prior to writing a new example, please review the [examples outline](README.md) and determine where your example best fits.
We encourage you to [propose your new example in an issue](https://github.com/glotzerlab/hoomd-examples/issues/new?assignees=&labels=&template=new_example.md&title=)
and discuss your plans with the HOOMD developer community to ensure that the planned development meshes well with the directions and standards of the project.
Follow the general guidelines outlined below when writing your example.

## Changes to an existing example

[File a GitHub issue](https://github.com/glotzerlab/hoomd-examples/issues/new?assignees=&labels=&template=bug_report.md&title=)
to report problems with or suggest changes to an example. If you are able to implement the fix yourself, **please do so**
and submit a [pull request on GitHub](https://github.com/glotzerlab/hoomd-examples/pulls). Follow the general guidelines
outlined below when modifying examples.

## General guidelines

### Jupyter notebooks

Examples should be written as Jupyter notebooks with an appropriate mixture of code and explanatory Markdown cells.

### Use a consistent style

All examples should follow a consistent style. See the existing notebooks which demonstrate this style.

### Keep the repository size reasonable

Include notebook output in your commits, but keep the repository size reasonable. HOOMD does not re-run notebooks when
building documentation, so the committed output is exactly what the user will see.

* Only commit changes for notebooks that you materially change
* Animated GIF output should be less than 2 MB per image (the visualization helper script will warn for larger movies)
* Feel free to make as many commits as needed during the review process, your pull request will be squash merged
* Do not commit GSD files or other output files that the examples produce

### Name notebook files appropriately

Notebook files should be named like `00-Example-Title.ipynb` and placed in the appropriate (sub-)section directory.
Use `-` instead of spaces. The leading digits should be chosen so that the example appears in the correct place in
the order displayed by ls, github, and jupyter. See the [examples outline](README.md) for the outline of current examples.

### List examples in the outline

Add new examples to the [examples outline](README.md).
