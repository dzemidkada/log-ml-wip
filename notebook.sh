#!/bin/bash

source activate logml
conda env list

export PROJECT_ROOT=`pwd`
export PYTHONPATH=$PYTHONPATH:`pwd`/src
jupyter notebook $@
