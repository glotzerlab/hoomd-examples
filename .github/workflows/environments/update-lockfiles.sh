#!/bin/bash

# Execute this script to update all lock files to the latest versions of dependencies.

rm *-conda-lock.yml

for python_version in 3.12
do
  sed "s/python==.*/python=$python_version/g" environment.yaml > tmp.yaml || exit 2
  conda lock -f tmp.yaml -p linux-64 --lockfile py${python_version//.}-conda-lock.yml || exit 2
done
rm tmp.yaml
