import dash_bootstrap_components as dbc


class Grid:
    size = 2
    map = ""
    mario_loc = None
    princess_loc = None
    error = False
    paths = []
    visited_coordinates = []
    obstacles = []
    solutions = []

    # For debugging purposes
    def print(self):
        print("size:" + str(self.size) + " map:" + self.map + " mario_loc:" + str(self.mario_loc) + " princess_loc:" +
              str(self.princess_loc) + " error:" + str(self.error) + " paths:" + str(self.paths) +
              " obstacles:" + str(self.obstacles) + " visited_coordinates:" + str(self.visited_coordinates) +
              " solutions" + str(self.solutions))

    # Grid has array of possible paths. This goes through the array
    # and adds additional paths until at princess coordinates.
    def next_move(self):
        directions = [("UP", (-1, 0)), ("RIGHT", (0, 1)), ("DOWN", (1, 0)), ("LEFT", (0, -1))]

        paths_copy = list(self.paths)
        for path in paths_copy:
            last_move = 0
            if len(path[0]) > 0:
                last_move = path[0][-1]

            for direction in directions:
                # Don't go backwards
                if last_move != 0:
                    if (direction[0] == "UP" and last_move == "DOWN") or (direction[0] == "RIGHT" and last_move == "LEFT") \
                            or (direction[0] == "DOWN" and last_move == "UP") or (
                            direction[0] == "LEFT" and last_move == "RIGHT"):
                        continue
                new_path = list(path)
                new_path[0] = list(path[0])

                # Calculate new co-ordinates
                new_coordinates = (path[1][0] + direction[1][0], path[1][1] + direction[1][1])
                # Validate move is in grid
                # Don't add path if not in grid or is an obstacle
                # Or already visited by other path in previous attempts
                if not(-1 < new_coordinates[0] < self.size) or not(-1 < new_coordinates[1] < self.size) or \
                        (new_coordinates in self.obstacles) or (new_coordinates in self.visited_coordinates):
                    continue
                new_path[1] = new_coordinates
                new_path[0].append(direction[0])
                self.paths.append(new_path)
            # Remove the path just checked. New paths are this path plus one direction
            self.paths.pop(0)

        # Check if the paths have reached the Princess

        for path in self.paths:
            if path[1] not in self.visited_coordinates:
                self.visited_coordinates.append(path[1])
            if path[1] == self.princess_loc:
                self.solutions.append(path[0])

    # returns True if grid is valid
    def validate(self):
        # Make sure properties are reset
        self.visited_coordinates = []
        self.obstacles = []
        self.solutions = []
        # convert map to list for iteration
        map = self.map[1:-1]
        map = map.split(",")
        map = list(map)
        # self.error will change to False if method does not return due to error
        self.error = True
        mario_counter = 0
        princess_counter = 0
        for row_index, row in enumerate(map):
            # Check row lengths
            if len(row) != self.size:
                return False
            elif row_index >= self.size:
                return False
            # Check chars are valid
            valid_chars = ['m', 'p', '-', 'x']
            for char in row:
                if char not in valid_chars:
                    return False
            if "m" in row:
                if row.count("m") > 1:
                    return False
                self.mario_loc = (row_index, row.find("m"))
                mario_counter += 1
            if "p" in row:
                if row.count("p") > 1:
                    return False
                self.princess_loc = (row_index, row.find("p"))
                princess_counter += 1
            if "x" in row:
                for char_index, char in enumerate(row):
                    if char == "x":
                        if (row_index, char_index) not in self.obstacles:
                            self.obstacles.append((row_index, char_index))

        if not bool(self.princess_loc) or not bool(self.mario_loc):
            return False
        if mario_counter != 1 or princess_counter != 1:
            return False
        self.paths = [[[], self.mario_loc]]
        self.error = False
        self.print()
        return True

    # Sets the map to a blank grid. The size is determined by size property
    # Used by app when size input is changed
    def set_grid_blank(self):
        i = 0
        map = []
        # construct blank grid
        while i < self.size:
            dash = "'-'"
            j = 0
            for row in map:
                dash = dash[:-1] + '-' + dash[-1:]
                map[j] = row[:-1] + '-' + row[-1:]
                j += 1
            i += 1

            map.append(dash)
        # Convert to str
        st = "["
        for row in map:
            st += str(row) + ","
        st = st[:-1]
        st += "]"
        self.map = st


# This class is used to draw the square grid graphically
class GridGraphic:
    grid = None

    def __init__(self, grid_obj):
        self.grid = grid_obj

    # returns the grid inside container
    def draw(self):
        container_contents = []
        x_val = 0
        for row in self.grid.map[1:-1].split(','):
            row_contents = []
            y_val = 0
            for col in row:
                coordinates = (x_val, y_val)
                class_names = {'x': 'grid-col-x', '-': 'grid-col-blank', 'm': 'grid-col-mario', 'p': 'grid-col-princess'}
                row_contents.append(dbc.Col([dbc.Col([col], className='grid-col ' + class_names[col], id="col-"+str(coordinates))]))
                y_val += 1
            container_contents.append(dbc.Row(row_contents, className='grid-row'))
            x_val += 1
        return dbc.Container(container_contents, id='grid-container-inner')
