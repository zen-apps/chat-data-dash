"""
This file houses the main Dash application.
This is where the various CSS items are fetched, and the layout of the application is defined.
"""

import dash
import dash_bootstrap_components as dbc
from data_chat.layout import create_chat_layout
from data_chat.callbacks import chat_callbacks

# Constants
EXTERNAL_STYLESHEETS = [
    dbc.themes.SLATE,
    dbc.icons.FONT_AWESOME,
]
META_TAGS = [
    {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1",
    }
]

# Initialize Dash App
app = dash.Dash(
    __name__,
    external_stylesheets=EXTERNAL_STYLESHEETS,
    meta_tags=META_TAGS,
    suppress_callback_exceptions=True,
    title="Easy Data Chat",
)
server = app.server
app.scripts.config.serve_locally = True

# Adding additional CSS
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = create_chat_layout()
app = chat_callbacks(app)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=int(3457), debug=True)
