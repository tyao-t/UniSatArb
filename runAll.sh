#!/bin/bash

python process_GateIO.py &
python process_Unisat.py &
python process_ArbOpp.py &
# Add more scripts as needed

wait