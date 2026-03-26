#!/bin/bash

for run in {4865..4890}; do
    ./run_KaonLT.py --run-number $run --run-type Prod --target LH2
done
