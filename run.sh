#!/bin/bash

xterm -maximized -hold -e python CPS/CPS.py 3 & sleep 2 &&
for run in {1..3}
do
    xterm -maximized -hold -e python EC/EC.py test1.txt $run &
done
