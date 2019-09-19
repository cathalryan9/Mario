# -*- coding: utf-8 -*-
import sys
import json
import config
from logger import Logger
from grid import Grid
from flask import Flask, request, Response
from logger import Logger


http_server = Flask(__name__)
logger = Logger()

def main():
    http_server.run(debug=True, threaded=True, host=config.HOST_IP_ADDRESS)


@http_server.route('/input', methods=['POST'])
def check_input():
    gridSize = json.loads(request.form["size"].strip())

    inputGrid = request.form["grid"].strip()
    if sys.getdefaultencoding() == "utf-8":
        inputGrid = inputGrid.replace("‘", "").replace("’", "")
    else:
        inputGrid = inputGrid.replace("\x91", "")
        inputGrid = inputGrid.replace("\x92", "")
    inputGrid = "\"" + inputGrid + "\""
    print(inputGrid)

    grid = json.loads(inputGrid, encoding='utf-8')
    print(grid)
    g = Grid(gridSize, grid)
    if (g.error):
        print(g.error)
        response = {
            "quickestSolutions": g.solutions,
            "error": g.error
        }
    else:
        while g.solutions == []:
            g.nextMove()
        print(g.solutions)
        response = {
            "quickestSolutions": g.solutions,
            "error_flag": g.error
        }
    lgr = Logger()
    lgr.write(response, "/input")
    return json.dumps(response)


if __name__ == "__main__":
    main()
