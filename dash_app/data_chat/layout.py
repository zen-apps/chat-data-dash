"""
Layout for the Data Chat Page
"""
from dash import dcc, html, dash_table
from utils.layout_helpers import (
    box_style,
    chat_output_style,
    style_table,
    style_cell,
    style_header,
)


def create_chat_layout():
    return html.Div(
        [
            html.Div(
                [
                    html.H3(
                        "Step 1: Select Data",
                        style={"marginBotton": "10px", "color": "SeaGreen"},
                    ),
                    dcc.Upload(
                        id="upload-data",
                        children=html.Button("Upload Your Own Spreadsheet"),
                        multiple=False,
                    ),
                    html.Div(
                        id="output-data-upload",
                        style={"width": "90%", "margin": "0 auto"},
                    ),
                    html.Div(id="dd-output-container"),
                    dcc.Store(id="file-selector-store", storage_type="memory", data=[]),
                    dcc.Checklist(
                        id="checklist",
                        options=[
                            {
                                "label": "Display LLM Generated Table Definitions",
                                "value": "checkbox_val",
                            }
                        ],
                        value=[],
                    ),
                    dash_table.DataTable(
                        id="data-table-schema",
                        columns=[],
                        data=[],
                        editable=True,
                        style_table=style_table,
                        style_cell=style_cell,
                        style_header=style_header,
                    ),
                    dcc.Store(
                        id="data-table-schema-store", storage_type="memory", data=[]
                    ),
                ],
                style=box_style,
            ),
            html.Div(
                [
                    html.H3(
                        "Step 2: Ask a question about the data",
                        style={"color": "SeaGreen"},
                    ),
                    html.Div(id="chat-output", style=chat_output_style),
                    dcc.Input(
                        id="user-input",
                        type="text",
                        placeholder="Type your message...",
                        style={"width": "90%", "textAlign": "center"},
                    ),
                    html.Button("Send", id="send-button", n_clicks=0),
                    dcc.Store(
                        id="hidden-div-chat-history", storage_type="memory", data=[]
                    ),
                    dcc.Store(
                        id="hidden-div-chat-output-parsed",
                        storage_type="memory",
                        data=[],
                    ),
                ],
                style=box_style,
            ),
        ]
    )
