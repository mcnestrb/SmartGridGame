#!/bin/bash

source activate py35
xterm -hold -e python CPS/CPS.py 3 & sleep 3 &&
for run in {1..3}
do
    xterm -hold -e python EC/EC.py test1.txt $run &
done
