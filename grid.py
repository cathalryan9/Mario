import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


class Grid:
    size = 0
    map = 0
    mario_loc = 0
    princess_loc = 0
    error = False
    paths = []
    obstacles = []
    solutions = []

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
                if not(-1 < new_coordinates[0] < self.size) or not(-1 < new_coordinates[1] < self.size) or \
                        (new_coordinates in self.obstacles):
                    continue
                new_path[1] = new_coordinates
                new_path[0].append(direction[0])
                self.paths.append(new_path)
            self.paths.pop(0)

        # Check if the paths have reached the Princess
        for path in self.paths:
            if path[1] == self.princess_loc:
                self.solutions.append(path[0])

    def validate(self, grid):
        map = grid[1:-1]
        map = map.split(",")
        self.map = list(map)

        mario_counter = 0
        princess_counter = 0
        for row_index, row in enumerate(self.map):
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
                self.princess_loc = (rowIndex, row.find("p"))
                princess_counter += 1
            if "x" in row:

                for charIndex, char in enumerate(row):
                    if char == "x":
                        self.obstacles.append((rowIndex, charIndex))

        if self.princess_loc == 0 or self.mario_loc == 0:
            # Not a valid grid
            return False

        if mario_counter > 1 or princess_counter > 1:
            return False
        self.paths = [[[], self.mario_loc]]
        return True

    def update_grid(self, row, col, char):
        # Placeholder
        a = 0

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
            print(map)
        # Convert to str
        st = "["
        for row in map:
            st += str(row) + ","
        st = st[:-1]
        st += "]"
        self.map = st


    #def __init__(self):
        #self.size = int(size)
        # Remove unneeded chars and convert to list
        #map = map[1:-1]
        #map = map.split(",")

        #self.map = list(map)

        # Grid is validated here
        #if not self.validate():
            #self.error = True


# This class is used to draw the square grid graphically
class GridGraphic:
    grid = 0

    def __init__(self, grid):
        self.grid = grid

    def draw(self):
        container_contents = []

        for row in self.grid.map[1:-1].split(','):
            row_contents = []
            for col in row[1:-1]:
                row_contents.append(dbc.Col([html.Div(col, className="grid-col")]))
            container_contents.append(dbc.Row(row_contents))

        return dbc.Container(container_contents, id='grid-container-inner')
