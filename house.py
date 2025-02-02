import numpy as np
import matplotlib.pyplot as plt


class House:
    """
    A class representing a house layout with rooms, windows, doors, heaters, and outside areas.
    """

    def __init__(self, step, heater_power):
        """
        Initializes the House object.

        Parameters:
        step (float): The grid step size.
        heater_power (float): The power of the heater.
        """
        self.rooms = []
        self.outside = []
        self.windows = []
        self.doors = []
        self.heaters = []
        self.heater_power = heater_power
        self.heater_setting = 0
        self.step = step

    def main_frame(self):
        """
        Creates the main frame of the house based on room layout.

        Returns:
        tuple: A tuple containing a 2D numpy array representing the house layout,
               and numpy arrays representing x and y coordinates.
        """
        room_x_indexes = [room[1][1] for room in self.rooms] + [room[0][1] for room in self.rooms]
        room_y_indexes = [room[1][0] for room in self.rooms] + [room[0][0] for room in self.rooms]

        sorted_x = sorted(room_x_indexes)
        sorted_y = sorted(room_y_indexes)

        min_x = sorted_x[0]
        max_x = sorted_x[-1]
        min_y = sorted_y[0]
        max_y = sorted_y[-1]

        shift = self.step / 2
        xs = np.arange(start=0 + shift, stop=max_x, step=self.step)
        ys = np.arange(start=0 + shift, stop=max_y, step=self.step)

        return np.zeros((len(xs), len(ys))), xs, ys

    def layout(self, draw=False, door_gen=False):
        """
        Generates the layout of the house and optionally draws it.

        Parameters:
        draw (bool): If True, draws the house layout.
        door_gen (bool): Unused parameter, included for future extensions.

        Returns:
        numpy.ndarray: 2D array representing the house layout.
        """
        frame, xs, ys = self.main_frame()
        shift = self.step / 2

        for room in self.rooms:
            # Define room boundaries
            frame[int(room[0][1] // self.step),
            int(room[0][0] // self.step):(int(room[1][0] // self.step) + 1)] = 1  # Bottom
            frame[int(room[1][1] // self.step),
            int(room[0][0] // self.step):(int(room[1][0] // self.step) + 1)] = 2  # Top
            frame[(int(room[0][1] // self.step) + 1):int(room[1][1] // self.step),
            int(room[0][0] // self.step)] = 3  # Left
            frame[(int(room[0][1] // self.step) + 1):int(room[1][1] // self.step),
            int(room[1][0] // self.step)] = 4  # Right

        # Mark outside areas
        for area in self.outside:
            frame[int(area[0][1] // self.step):int(area[1][1] // self.step),
            int(area[0][0] // self.step):(int(area[1][0] // self.step) + 1)] = -1

        # Mark windows
        for window in self.windows:
            if window[2] == 'h':
                frame[int(window[0][1] // self.step),
                (int(window[0][0] // self.step)):(int(window[1][0] // self.step) + 1)] = -1
            elif window[2] == 'v':
                frame[(int(window[0][1] // self.step) + 1):(int(window[1][1] // self.step) + 1),
                int(window[0][0] // self.step)] = -1

        # Mark doors
        for door in self.doors:
            if door[2] == 'h':
                frame[int(door[0][1] // self.step),
                (int(door[0][0] // self.step)):(int(door[1][0] // self.step) + 1)] = 0
            elif door[2] == 'v':
                frame[(int(door[0][1] // self.step) + 1):(int(door[1][1] // self.step) + 1),
                int(door[0][0] // self.step)] = 0

        # Mark heaters
        n = 5
        for heater in self.heaters:
            if heater[2] == 'h':
                frame[int(heater[0][1] // self.step),
                (int(heater[0][0] // self.step)):(int(heater[1][0] // self.step) + 1)] = n
            elif heater[2] == 'v':
                frame[(int(heater[0][1] // self.step) + 1):(int(heater[1][1] // self.step) + 1),
                int(heater[0][0] // self.step)] = n
            n += 1

        if draw:
            plt.pcolormesh(ys, xs, frame, cmap='Greys')
            plt.gca().set_aspect('equal')
            plt.xlabel("$x$")
            plt.ylabel("$y$")
            plt.suptitle("House Layout")
            plt.colorbar()
            plt.show()

        return frame

    def add_room(self, index1, index2):
        """Adds a room to the house."""
        self.rooms.append([index1, index2])

    def add_outside(self, point1, point2):
        """Adds an outside area."""
        self.outside.append([point1, point2])

    def add_window(self, point1, point2, orientation):
        """Adds a window."""
        self.windows.append([point1, point2, orientation])

    def add_door(self, point1, point2, orientation):
        """Adds a door."""
        self.doors.append([point1, point2, orientation])

    def add_heater(self, point1, point2, orientation, room1, room2):
        """Adds a heater."""
        self.heaters.append([point1, point2, orientation, room1, room2])

    def set_heater_power(self, value):
        """Sets the heater power."""
        self.heater_power = value

    def set_heating(self, value):
        """Sets the heating level."""
        self.heater_setting = value

    def get_area(self, p1, p2):
        """
        Returns a 2D array representation of a specific area in the house.

        Parameters:
        p1 (tuple): Bottom-left coordinate of the area.
        p2 (tuple): Top-right coordinate of the area.

        Returns:
        numpy.ndarray: 2D array representing the selected area.
        """
        frame = self.main_frame()[0]
        frame[int(p1[1] // self.step):(int(p2[1] // self.step) + 1),
        int(p1[0] // self.step):(int(p2[0] // self.step) + 1)] = 1
        return frame
