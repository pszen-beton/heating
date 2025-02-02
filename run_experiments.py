from house import *
from solver import *

# EXPERIMENT 1
    # WINDOW HEATING

test_house1 = House(0.1, 500)
test_house1.set_heating(294)
test_house1.add_room([0,0],[3,2])
test_house1.add_room([0,2.1],[2,3.5])
test_house1.add_room([3.1,0],[4,1.25])
test_house1.add_room([3.1,1.35],[4,2])

test_house1.add_outside([2.1,2.1],[4,4.5])

test_house1.add_window([0,0.3],[0,1.7],'v')
test_house1.add_window([0,2.15],[0,3.3],'v')
test_house1.add_window([2,2.15],[2,3.3],'v')
test_house1.add_window([2.15,2],[2.7,2],'h')
test_house1.add_window([4,1.5],[4,1.8],'v')

test_house1.add_heater([0.1,0.3],[0.1,1.7],'v',[0.1,0.1],[1.9,1.9])
test_house1.add_heater([0.1,2.15],[0.1,3.3],'v',[0.1,2.2],[0.9,2.4])
test_house1.add_heater([1.9,2.15],[1.9,3.3],'v',[1.2,2.2],[1.9,3.4])
test_house1.add_heater([2.15,1.9],[2.7,1.9],'h',[2.2,0.1],[2.9,1.9])

test_house1.add_door([0.5,2],[1.2,2],'h')
test_house1.add_door([0.5,2.1],[1.2,2.1],'h')

test_house1.add_door([3,1.4],[3,1.9],'v')
test_house1.add_door([3.1,1.4],[3.1,1.9],'v')

test_house1.add_door([3,0.7],[3,1.1],'v')
test_house1.add_door([3.1,0.7],[3.1,1.1],'v')
test_house1.layout(True)

test_solver = Solver(19, 1.3, 1005, pd.read_csv("wroclaw_temperature.csv"))
sol, xs, ys, n_xs, n_ys, add = test_solver.solve(test_house1,9,1,0.0001)
test_solver.show_solution_snapshots(points=5)
test_solver.show_solution_animation(1)
print(sum(add))

    #NON-WINDOW HEATING

test_house2 = House(0.1, 500)
test_house2.set_heating(294)
test_house2.add_room([0,0],[3,2])
test_house2.add_room([0,2.1],[2,3.5])
test_house2.add_room([3.1,0],[4,1.25])
test_house2.add_room([3.1,1.35],[4,2])

test_house2.add_outside([2.1,2.1],[4,4.5])

test_house2.add_window([0,0.3],[0,1.7],'v')
test_house2.add_window([0,2.15],[0,3.3],'v')
test_house2.add_window([2,2.15],[2,3.3],'v')
test_house2.add_window([2.15,2],[2.7,2],'h')
test_house2.add_window([4,1.5],[4,1.8],'v')

test_house2.add_heater([0.3,0.1],[2.3,0.1],'h',[0.1,0.1],[2.9,1.9])
test_house2.add_heater([1.05,2.15],[1.05,3.3],'v',[0.1,2.2],[1.9,3.4])
test_house2.add_heater([1,2.15],[1,3.3],'v',[0.1,2.2],[1.9,3.4])


test_house2.add_door([0.5,2],[1.2,2],'h')
test_house2.add_door([0.5,2.1],[1.2,2.1],'h')

test_house2.add_door([3,1.4],[3,1.9],'v')
test_house2.add_door([3.1,1.4],[3.1,1.9],'v')

test_house2.add_door([3,0.7],[3,1.1],'v')
test_house2.add_door([3.1,0.7],[3.1,1.1],'v')
test_house2.layout(True)

test_solver = Solver(19, 1.3, 1005, pd.read_csv("wroclaw_temperature.csv"))
sol, xs, ys, n_xs, n_ys, add = test_solver.solve(test_house2,9,1,0.0001)
test_solver.show_solution_snapshots(points=5)
test_solver.show_solution_animation(1)
print(sum(add))

### EXPERIMENT 2
    #heaters constanlty on
test_solver = Solver(19, 1.3, 1005, pd.read_csv("wroclaw_temperature.csv"))
sol, xs, ys, n_xs, n_ys, add = test_solver.solve(test_house1,6,11,0.0001)
test_solver.show_solution_snapshots(points=5)
test_solver.show_solution_animation(1)

    #heaters completely off
test_house1.set_heating(279)
sol1, xs, ys, n_xs, n_ys, add1 = test_solver.solve(test_house1,6,9,0.0001)
test_solver.show_solution_snapshots(points=5)
test_solver.show_solution_animation(1)
ad1 = sum(add1)
    #heaters back on
test_house1.set_heating(294)
sol2, xs, ys, n_xs, n_ys, add2 = test_solver.solve(test_house1,15,2,0.0001,sol1[-1,:])
test_solver.show_solution_snapshots(points=5)
test_solver.show_solution_animation(1)
ad2 = sum(add2)
sum(add)
print(ad1+ad2)