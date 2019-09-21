# -*- coding: utf-8 -*-
import sys
import json
import config
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
external_stylesheets = [dbc.themes.CERULEAN]
app = dash.Dash(
    __name__,
    server=http_server,
    routes_pathname_prefix='/dash/',
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True
)

app.head = [html.Link(rel="stylesheet", href='assets/styles.css')]
app.layout = dbc.Container(id="container-inputs", children=[dbc.Container([dcc.Input(
            id='size-input',
            placeholder='Insert grid size',
            type='number',
            value='2',
            min=2,
            step=1
        ), dcc.Input(
            id='grid-input',
            placeholder='Insert grid layout',
            type='text',
            value='[]')]),
    dbc.Container([GridGraphic(g).draw()], id='container-grid'),
    dbc.Container(id='container-solutions')])


def main():
    app.run_server(debug=True, threaded=True, host=config.HOST_IP_ADDRESS)

@app.callback(Output(component_id='grid-input', component_property='value'),
              [Input(component_id='size-input', component_property='value')])
def update_grid_input(size_input):
    if size_input:
        g.size = int(size_input)
        g.set_grid_blank()
    return g.map


@app.callback(Output(component_id='container-grid', component_property='children'),
              [Input(component_id='grid-input', component_property='value')])
def update_grid(grid_input):
    g.obstacles = []
    g.mario_loc = 0
    g.princess_loc = 0
    if len(grid_input) < 6:
        return
    grid_input = grid_input.replace("'", "").replace("'", "")
    g.solutions = []
    g.map = grid_input
    g.validate()
    if g.error:
        return html.Div(["Invalid grid"], id='error-div')
    return GridGraphic(g).draw()

@app.callback(Output(component_id='container-solutions', component_property='children'),
              [Input(component_id='container-grid', component_property='children')])
def calculate_paths(input):
    if not g.error:
        i = 0
        g.print()
        while g.solutions == []:
            g.next_move()
            # Stop it from hanging
            if i > 1000:
                g.paths = []
                return "unable to calculate"
            i += 1
        return str(g.solutions)
    else:
        return


@http_server.route('/input', methods=['POST'])
def check_input():
    grid_size = json.loads(request.form["size"].strip())

    input_grid = request.form["grid"].strip()
    if sys.getdefaultencoding() == "utf-8":
        input_grid = input_grid.replace("‘", "").replace("’", "")
    else:
        input_grid = input_grid.replace("\x91", "").replace("\x92", "")
    input_grid = "\"" + input_grid + "\""
    grid = json.loads(input_grid, encoding='utf-8')
    g.size = grid_size
    g.map = grid
    g.validate()
    if g.error:
        response = {
            "quickest_solutions": g.solutions,
            "error_flag": g.error
        }
    else:
        while g.solutions == []:
            g.next_move()
        response = {
            "quickest_solutions": g.solutions,
            "error_flag": g.error
        }
    return json.dumps(response)

@http_server.route('/log', methods=['GET'])
def get_logs():
    logs = lgr.read_all()
    return json.dumps(logs)


if __name__ == "__main__":
    main()
