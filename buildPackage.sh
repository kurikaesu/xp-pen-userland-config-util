#!/bin/bash

rm -rf deb_dist
python3 setup.py --command-packages=stdeb.command bdist_deb
