#!/bin/bash

killall python process_GateIO.py &
killall python process_Unisat.py &
killall python process_ArbOpp.py &

wait