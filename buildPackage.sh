#!/bin/bash

rm -rf deb_dist
rm -f *.tar.gz
python3 setup.py --command-packages=stdeb.command bdist_deb
