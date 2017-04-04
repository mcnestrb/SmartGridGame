#!/bin/bash
source activate py35
xterm -e python CPS/CPS.py & sleep 2 &&
for run in {1..3}
do
    xterm -e python EC/EC.py &
done
