import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

class Grid:
    size = 0
    map = 0
    marioLoc = 0
    princessLoc = 0
    error = False
    paths = []
    obstacles = []
    solutions = []


    def nextMove(self):
        directions = [("UP", (-1, 0)), ("RIGHT", (0, 1)), ("DOWN", (1, 0)), ("LEFT", (0, -1))]

        pathsCopy = list(self.paths)
        for path in pathsCopy:
            lastMove = 0
            if len(path[0]) > 0:
                lastMove = path[0][-1]

            for direction in directions:
                # Don't go backwards
                if lastMove != 0:
                    if (direction[0] == "UP" and lastMove == "DOWN") or (direction[0] == "RIGHT" and lastMove == "LEFT") \
                            or (direction[0] == "DOWN" and lastMove == "UP") or (
                            direction[0] == "LEFT" and lastMove == "RIGHT"):
                        continue
                newPath = list(path)
                newPath[0] = list(path[0])

                # Calculate new co-ordinates
                newCoordinates = (path[1][0] + direction[1][0], path[1][1] + direction[1][1])
                # Validate move is in grid
                # Don't add path if not in grid or is an obstacle
                if not(-1 < newCoordinates[0] < self.size) or not(-1 < newCoordinates[1] < self.size) or \
                        (newCoordinates in self.obstacles):
                    continue
                newPath[1] = newCoordinates
                newPath[0].append(direction[0])
                self.paths.append(newPath)
            self.paths.pop(0)

        # Check if the paths have reached the Princess
        for path in self.paths:
            if path[1] == self.princessLoc:
                self.solutions.append(path[0])

    def validate(self, grid):
        map = grid[1:-1]
        map = map.split(",")
        self.map = list(map)

        marioCounter = 0
        princessCounter = 0
        for rowIndex, row in enumerate(self.map):
            if len(row) != self.size:
                return False
            elif rowIndex >= self.size:
                return False
            # Check chars are valid
            validChars = ['m', 'p', '-', 'x']
            for char in row:
                if char not in validChars:
                    return False
            if "m" in row:
                if row.count("m") > 1:
                    return False
                self.marioLoc = (rowIndex, row.find("m"))
                marioCounter += 1
            if "p" in row:
                if row.count("p") > 1:
                    return False
                self.princessLoc = (rowIndex, row.find("p"))
                princessCounter += 1
            if "x" in row:

                for charIndex, char in enumerate(row):
                    if char == "x":
                        self.obstacles.append((rowIndex, charIndex))

        if self.princessLoc == 0 or self.marioLoc == 0:
            # Not a valid grid
            return False

        if marioCounter > 1 or princessCounter > 1:
            return False
        self.paths = [[[], self.marioLoc]]
        return True
    def update_grid(self, row, col, char):
        a =0
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
    size = 0
    #map = ""
    grid = 0
    #def __init__(self):
        #print(grid.map)
        #self.size = grid.size
        #self.grid = grid

    def draw(self):
        container = []
        x = 0
        while x < self.size:
            row = []
            y = 0
            while y < self.size:
                row.append(dbc.Col([html.Div("0", className="grid-col")]))
                y += 1
            container.append(dbc.Row(row))
            x += 1
        dbc.Container(container)
        return dbc.Container(container, id='grid-container-inner')
