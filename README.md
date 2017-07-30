# SmartGridGame

Game Theory solution for Energy Trading in a Nanogrid. My implementation is mostly based off this paper


```
Tushar, Wayes, et al. "Prioritizing consumers in smart grid: A game theoretic approach." IEEE Transactions on Smart Grid 5.3 (2014): 1429-1438.
```

## Framework

Using Twisted framework for my Client and Server situation

## Anaconda virual environment
To run the code, an [Anaconda virtual environment](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/) must be set up and the [CVXPY library](http://www.cvxpy.org/en/latest/install/index.html) must be installed.

## Running the system
Once the virtual environment has been set up, it must be activate using 
```
source activate name_of_env
```

Within the root folder run the command
```
chmod +x run.sh
```

The system can then be run using 
```
./run.sh
```

The system ends when all entities return to the Idle state. There are a number of breaks within the system to allow it to be read more clearly. Simply hit the return key in the terminal representing the CPS to allow the system to continue.

