# -*- coding: utf-8 -*-
import sys
import json
import config
from logger import Logger
from grid import Grid, GridGraphic
from flask import Flask, request, Response
from logger import Logger
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

http_server = Flask(__name__)
lgr = Logger()
g = Grid()
externalStylesheets = [dbc.themes.CERULEAN]
app = dash.Dash(
    __name__,
    server=http_server,
    routes_pathname_prefix='/dash/',
    external_stylesheets=externalStylesheets
)
app.head = [html.Link(rel="stylesheet", href='assets/styles.css')]
app.layout = html.Div([dcc.Input(
            id='size-input',
            placeholder='Insert grid size',
            type='number',
            value='',
            min=2,
            step=1
        ), dbc.Container(id='grid-container-outer')])

def main():
    app.run_server(debug=True, threaded=True, host=config.HOST_IP_ADDRESS)

@app.callback(Output(component_id='grid-container-outer', component_property='children'),
              [Input(component_id='size-input', component_property='value')])
def update_grid(input_value):
    if input_value:
        g.size = int(input_value)
        # read from the frontend
        g.set_grid_blank()
        return GridGraphic().draw()


@http_server.route('/input', methods=['POST'])
def check_input():
    gridSize = json.loads(request.form["size"].strip())

    inputGrid = request.form["grid"].strip()
    if sys.getdefaultencoding() == "utf-8":
        inputGrid = inputGrid.replace("‘", "").replace("’", "")
    else:
        inputGrid = inputGrid.replace("\x91", "").replace("\x92", "")
    inputGrid = "\"" + inputGrid + "\""
    grid = json.loads(inputGrid, encoding='utf-8')
    g.size = gridSize
    g.validate(grid)
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

    print(g.map)
    lgr.write(response, "/input")

    return json.dumps(response)

@http_server.route('/log', methods=['GET'])
def get_logs():
    logs = lgr.read_all()
    return json.dumps(logs)


if __name__ == "__main__":
    main()
