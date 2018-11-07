#!/bin/bash
. dev/bin/activate
python3 generator.py $1
python3 userSimulation.py $1
deactivate
