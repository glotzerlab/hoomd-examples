# Contributing to hoomd-examples

## New tutorials

Contributions are welcomed via [pull requests on
GitHub](https://github.com/glotzerlab/hoomd-examples/pulls). Prior to writing a
new tutorial, please review the existing tutorials and the [software
carptentries methodologies](https://carpentries.github.io/instructor-training/)
plan the tutorial to reduce cognative load. Concept maps and outlines are
extremely effective tools for this planning, you can find the outlines for some
of the existing tutorials in the repository (TODO: link).

We encourage you to [propose your new example in an
issue](https://github.com/glotzerlab/hoomd-examples/issues/new?assignees=&labels=&template=new_example.md&title=)
and discuss your plans with the HOOMD developer community to ensure that the
proposed tutorial meshes well with the directions and standards of the project.
Follow the general guidelines outlined below when writing your example.

## Changes to an existing example

[File a GitHub
issue](https://github.com/glotzerlab/hoomd-examples/issues/new?assignees=&labels=&template=bug_report.md&title=)
to report problems with or suggest changes to an example. If you are able to
implement the fix yourself, **please do so** and submit a [pull request on
GitHub](https://github.com/glotzerlab/hoomd-examples/pulls). Follow the general
guidelines outlined below when modifying examples.

## General guidelines

### Methodology

Follow the the [software
carptentries methodologies](https://carpentries.github.io/instructor-training/).

Especially:

* Write tutorial content for novice users.
* Minimize cognative load.
* Provide motivation.
* Clearly outline the goals and prerequisites at the start of the tutorial and
  each section.

### Jupyter notebooks

Examples should be written as Jupyter notebooks with an appropriate mixture of
code and explanatory Markdown cells.

### Use a consistent style

All examples should follow a consistent style. See the existing notebooks which
demonstrate this style.

### Keep the repository size reasonable

Include notebook output in your commits, but keep the repository size
reasonable. HOOMD does not re-run notebooks when building documentation, so the
committed output is exactly what the user will see.

* Only commit changes for notebooks that you materially change.
* Captured output should be less than 2 MB per image.
* Feel free to make as many commits as needed during the review process, your
  pull request will be squash merged.
* Do not commit GSD files or other output files that the examples produce.

### Organize tutorials into sections

This repository is organized as a list of tutorials, each in its own directory.
Each tutorial consists of an ordered list of sections, each in its own notebook.
Each section should be concise and introduce only a few new concepts.
Consecutive sections should be ordered logically to teach all the concepts
necessary for the tutorial's subject.

Tutorials should list prequisite knowledge in the overview. A series of
*Introduction* tutorials explain the core concepts of HOOMD and later tutorials
should include one or more of these as a prerequisite.

### Name notebook files appropriately

The file naming scheme is `00-Tutorial-Title/00-Section-Title.ipynb` Use `-`
instead of spaces. The leading digits should be chosen so that tutorials and
sections are displayed in order by **ls**, **github**, and **jupyter**.

### List tutorials in the outline

Add new tutorials to the [outline](README.md).
