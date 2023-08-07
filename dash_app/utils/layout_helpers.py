"""
Style helpers for the Dash app
"""
from dash import html, dash_table


box_style = {
    "maxWidth": "1000px",
    "width": "90%",
    "margin": "0 auto",
    "padding": "20px",
    "border": "1px solid #ccc",
    "borderRadius": "5px",
    "textAlign": "center",
}

chat_output_style = {
    "maxWidth": "1000px",
    "width": "90%",
    "margin": "0 auto",
    "padding": "20px",
    "marginBotton": "10px",
    "maxHeight": "300px",
    "overflowY": "auto",
}

dark_mode_style = {
    "background-color": "#343a40",
    "color": "white",
}

style_table = {
    "overflowX": "auto",
    "border": "1px solid #343a40",
    "backgroundColor": "#343a40",
}

style_cell = {
    "backgroundColor": "#343a40",
    "color": "white",
    "border": "1px solid white",
}

style_header = {
    "backgroundColor": "#20232a",
    "fontWeight": "bold",
    "color": "white",
}


def display_data_table(df):
    return html.Div(
        [
            dash_table.DataTable(
                data=df.to_dict("records"),
                columns=[{"name": i, "id": i} for i in df.columns],
                style_table=style_table,
                style_cell=style_cell,
                style_header=style_header,
            )
        ]
    )
