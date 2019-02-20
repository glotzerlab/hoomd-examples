# Contributing to hoomd-examples

## New examples

Contributions are welcomed via [pull requests on GitHub](https://github.com/glotzerlab/hoomd-examples/pulls).
Prior to writing a new example, please review the [examples outline](OUTLINE.md) and determine where your example
best fits. We encourage you to [propose your new example in an issue](https://github.com/glotzerlab/hoomd-examples/issues/new?assignees=&labels=&template=new_example.md&title=)
and discuss your plans with the HOOMD developer community
to ensure that the planned development meshes well with the directions and standards of the project. Follow the general
guidelines outlined below when writing your example.

## Changes to an existing example

[File a github issue](https://github.com/glotzerlab/hoomd-examples/issues/new?assignees=&labels=&template=bug_report.md&title=)
to report problems with or suggest changes to an example. If you are able to implement the fix yourself, **please do so**
and submit a [pull request on GitHub](https://github.com/glotzerlab/hoomd-examples/pulls). Follow the general guidelines
outlined below when modifying examples.

## General guidelines

### Jupyter notebooks

Examples should be written as Jupyter notebooks with an appropriate mixture of code and explanatory markdown cells.

### Use a consistent style

All examples should follow a consistent style. See the existing notebooks which demonstrate this style.

### Keep the repository size reasonable

Include notebook output in your commits, but keep the repository size reasonable. HOOMD does not re-run notebooks when
building documentation, so the committed output is exactly what the user will see.

* Only commit changes for notebooks that you materially change
* Animated GIF output should be less than 2 MB per image (the visualization helper script will warn for larger movies)
* Feel free to make as many commits as needed during the review process, your pull request will be squash merged
* Do not commit GSD or other files that the examples produce

### Name notebook files appropriately

Notebook files should be named 0000-Example-Title.ipynb. Use `-` instead of space. The four digit code should be
unique and chosen so that the example appears in the correct place in Lexicographical order. Specifically, the first
digit is the section number, the second digit is the subsection, and the last two are the example number within the
subsection. See the [examples outline](OUTLINE.md) for context.

### List examples in the outline

Add new examples to the [examples outline](OUTLINE.md).
