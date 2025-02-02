# household heating

## About
This projects consists of two python classes used to describe model households and solve heat equation on them.
It can be used to model temperature over time allowing for analysis of energy consumption or heat distribution in different scenarions.

##
house.py contains class used to define houses. They are defined through rooms, doors, windows and heaters, each of which plays different role in heat distribution.

solver.py contains class used to solve a differential equation on a house and show results.

run_experiment.py is an example file used to run two simple simulations. First one checks if its better to place heaters next to windows or not.
                  The second one checks if its better energy-wise to turn of heating when you leave house of leave it on.
