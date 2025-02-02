import matplotlib.pyplot as plt
import numpy as np
from house import House
from matplotlib.animation import FuncAnimation
import pandas as pd

def round_down_to_nearest_quarter_hour(time):
    # Get the hours and minutes
    hours = int(time)
    minutes = (time - hours) * 60

    # Round the minutes down to the nearest 15-minute interval
    rounded_minutes = (minutes // 15) * 15

    # If rounded minutes reach 60, adjust the hour and reset minutes
    if rounded_minutes == 60:
        rounded_minutes = 0
        hours += 1

    # Return the time as a float in hours with rounded minutes
    return hours + rounded_minutes / 60

def get_temperature_at_time(df, time):
    rounded_time = round_down_to_nearest_quarter_hour(time)
    temperature = df[df["Time"] == rounded_time]["Temperature"].values

    return temperature[0]


def decimal_to_time(decimal_hours):
    hours = int(decimal_hours)
    minutes = round((decimal_hours - hours) * 60)

    time_string = f"{hours}:{minutes:02d}"

    return time_string


class Solver:

    """
    A class for solving the heat equation for a given house layout.
    """

    def __init__(self, alpha, rho, c, temperatures):
        """
        Initializes the solver with material properties and temperature data.

        Parameters:
        alpha (float): Thermal diffusivity.
        rho (float): Density of the material.
        c (float): Specific heat capacity.
        temperatures (pd.DataFrame): Temperature data.
        """
        self.alpha = alpha
        self.rho = rho
        self.c = c
        self.temperatures = temperatures
        self.solution = None
        self.xs = None
        self.ys = None
        self.n_xs = None
        self.n_ys = None
        self.start_time = None
        self.end_time = None
        self.times = None

    def solve(self, house, start_time, end_time, time_step, start=None):

        """
        Solves the heat equation over a given time range for a house layout.

        Parameters:
        house (House): The house object representing the layout.
        start_time (float): Simulation start time.
        end_time (float): Simulation end time.
        time_step (float): Time step for the simulation.
        start (numpy array, optional): Initial temperature distribution.

        Returns:
        tuple: Solution array, grid coordinates, number of points, and heat added.
        """

        time_vector = np.arange(0, end_time, time_step)

        ys, xs = house.main_frame()[1:3]

        layout = house.layout(False)
        layout = layout.flatten()

        step = house.step

        n_xs = len(xs)
        n_ys = len(ys)

        ###WALLS
        bottom_walls = list(np.where(layout == 1)[0])
        top_walls = list(np.where(layout == 2)[0])
        left_walls = list(np.where(layout == 3)[0])
        right_walls = list(np.where(layout == 4)[0])

        bottom_neighboors = [i + n_xs for i in bottom_walls]
        top_neighboors = [i - n_xs for i in top_walls]
        left_neighboors = [i + 1 for i in left_walls]
        right_neighboors = [i - 1 for i in right_walls]

        outside = list(np.where(layout == -1)[0])

        inside = list(np.where(layout == 0)[0])

        heaters = []
        n_heaters = (np.max(layout)) - 4
        for i in range(5, (int(np.max(layout))+1)):
            heaters.append(list(np.where(layout == i)[0]))


        xs, ys = np.meshgrid(xs, ys)

        solution = np.zeros([len(time_vector),n_xs*n_ys])

        d2_x = np.zeros([n_xs, n_xs])
        d2_y = np.zeros([n_ys, n_ys])

        for i in range(n_xs):
            d2_x[i, i] = -2
            if i > 0:
                d2_x[i, i - 1] = 1
            if i < n_xs-1:
                d2_x[i, i + 1] = 1
        d2_x = (1 / step ** 2) * d2_x * self.alpha

        for i in range(n_ys):
            d2_y[i, i] = -2
            if i > 0:
                d2_y[i, i - 1] = 1
            if i < n_ys-1:
                d2_y[i, i + 1] = 1
        d2_y = (1 / step ** 2) * d2_y * self.alpha

        L = np.kron(np.identity(n_ys), d2_x) + np.kron(d2_y, np.identity(n_xs))

        if start is None:
            for point in inside:
                solution[0, point] = 294

            for heater in heaters:
                for point in heater:
                    solution[0, point] = 294

            for i in bottom_walls + top_walls + left_walls + right_walls:
                solution[0,i] = 294

            for i in outside:
                temp = get_temperature_at_time(self.temperatures, start_time)
                solution[0, i] = temp
        else:
            solution[0,:] = start

        heat_added = []

        for t in range(len(time_vector) - 1):
            solution[t + 1, :] = (solution[t, :] + time_step * np.matmul(L, solution[t, :]))



            for i, j in enumerate(left_walls):
                solution[t+1, j] = solution[t+1, left_neighboors[i]]

            for i, j in enumerate(right_walls):
                solution[t+1, j] = solution[t+1, right_neighboors[i]]

            for i, j in enumerate(top_walls):
                solution[t+1, j] = solution[t+1, top_neighboors[i]]

            for i, j in enumerate(bottom_walls):
                solution[t+1, j] = solution[t+1, bottom_neighboors[i]]



            for i, heater in enumerate(heaters):
                heated_room = house.get_area(house.heaters[i][3], house.heaters[i][4])
                heated_room = heated_room.flatten()
                heated_room = (np.where(heated_room == 1)[0])
                temperatures_in_spots = [solution[t+1, spot] for spot in heated_room]
                average_temp = np.mean(temperatures_in_spots)
                if average_temp < house.heater_setting:
                    for j in heater:
                        solution[t + 1, j] = solution[t+1, j] + (house.heater_power / (0.01 * self.rho * self.c))
                        heat_added.append((house.heater_power / (0.01 * self.rho * self.c)))

            current_time = start_time + time_vector[t+1]
            #print(current_time)
            current_temp = get_temperature_at_time(self.temperatures, current_time)
            for i in outside:
                solution[t+1, i] = current_temp

        heater_lens = [len(heater) for heater in heaters]

        self.solution, self.xs, self.ys, self.n_xs, self.n_ys = solution, xs, ys, n_xs, n_ys
        self.start_time, self.end_time, self.times = start_time, (start_time + end_time), time_vector



        return solution , xs, ys, n_xs, n_ys, heat_added

    def show_solution_snapshots(self, points=2, cmap='inferno'):
        """
        Displays snapshots of the heat distribution at different time points.

       Parameters:
       points (int): Number of snapshots to display.
       cmap (str): Colormap to use.
       """
        if self.solution is None:
            raise Exception("Solve a problem first :)")

        n_ts = len(self.solution[:,0])
        indexes = [i for i in range(n_ts)]

        if points == 1:
            indexes = [0]

        if points == 2:
            indexes = [indexes[0], indexes[-1]]

        else:
            step = (n_ts // (points-1))
            indexes = [0] + ([indexes[(i * step)] for i in range(1, (points-1))]) + [n_ts - 1]



        for i in indexes:
            time = round(self.times[i] + self.start_time,2)
            time = decimal_to_time(time)
            fig, ax = plt.subplots()
            heatmap = ax.pcolormesh(self.xs, self.ys, self.solution[i, :].reshape(self.n_ys,self.n_xs), cmap=cmap, vmin=270, vmax=320)
            ax.set_aspect('equal')
            fig.suptitle(f"Heat distribution for t={time}")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            fig.colorbar(heatmap, ax=ax)
            plt.show()

    def show_solution_animation(self, each=1, cmap='inferno'):
        """
        Animates the heat distribution over time.

        Parameters:
        each (int): Interval at which frames are displayed.
        cmap (str): Colormap to use.
        """
        solution_frames = self.solution[::each, :]

        fig, ax = plt.subplots()
        heatmap = ax.pcolormesh(self.xs, self.ys, solution_frames[0, :].reshape(self.n_ys,self.n_xs), cmap=cmap, vmin=270, vmax=320)
        ax.set_aspect('equal')
        fig.colorbar(heatmap, ax=ax)


        def update(frame):
            heatmap.set_array(solution_frames[frame, :].reshape(self.n_ys,self.n_xs).flatten())
            return frame

        anim = FuncAnimation(fig, update, frames=len(solution_frames), interval=100)
        plt.show()






