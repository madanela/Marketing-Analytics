import base64
import os
from urllib.parse import quote as urlquote

from flask import Flask, send_from_directory
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from turtle import width
import dash_bootstrap_components as dbc
from dash import dcc, html

from dash import html, dcc, Dash, dash_table
from dash.dependencies import Input, Output, State

UPLOAD_DIRECTORY = "project/app_uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
class data_class:
    df = pd.DataFrame()
var = data_class

# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:

# @server.route("/download/<path:path>")
# def download(path):
#     """Serve a file from the upload directory."""
#     return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)
from app import app

def layout(params):
    return  dbc.Col(
    [
        dbc.Row([
            
            html.H1("File Browser"),
            html.H2("Upload"),
            dcc.Upload(
                id="upload-data",
                children=html.Div(
                    ["Drag and drop or click to select a file to upload."]
                ),
                style={
                    "width": "100%",
                    "height": "60px",
                    "lineHeight": "60px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "margin": "10px",
                },
                multiple=True,
            ),
            html.H2("File List"),
            html.Ul(id="file-list"),
        ]),
        
        dbc.Col( # Tabs  
            html.Div([
                dcc.Tabs(id = "tabs_inp_2",value = 'vis_2',
                    children = [
                        dcc.Tab(label="Visualisation", value="vis_2"),
                        dcc.Tab(label="Statistics", value="stat_2"),
                        dcc.Tab(label="Cross_Table", value="crosstable_2"),

                    ],
                ),
                html.Div(id='tabs-content-out-2')
            ]),
            class_name="pd-2",
        ),
    ],
)

def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""

    global var
    var.df = pd.read_csv(filename)

    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)


@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)

    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]


### tabs

from basic_page.tab1 import layout1
from basic_page.tab2 import layout2
from basic_page.tab3 import layout3
    

@app.callback(Output('tabs-content-out-2', 'children'),
              [Input('tabs_inp_2', 'value'),
             #  [Input(__package__ + "-button", "n_clicks")],
               ])
def render_content(tab):
    print(tab)
    if tab == 'vis_2':
        print("hllo")
        return  layout1(var.df)
    elif tab == 'stat_2':
       return layout2(var.df)
    elif tab == 'crosstable_2':
       return layout3(var.df)




