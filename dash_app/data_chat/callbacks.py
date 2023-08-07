"""
Callback functions for the Data Chat Page
"""

import json
import pandas as pd
from dash import html, dash_table, Output, Input, State
from data_chat.chat import sql_chat, setup_data_chat
from utils.data_helpers import upload_file_processing, dict_to_chat_obj
from utils.layout_helpers import display_data_table


def chat_callbacks(app):
    @app.callback(
        Output(component_id="dd-output-container", component_property="children"),
        Output(component_id="file-selector-store", component_property="data"),
        Output(component_id="data-table-schema-store", component_property="data"),
        Output("output-data-upload", "children"),
        Input("upload-data", "contents"),
        State("upload-data", "filename"),
    )
    def update_output(contents, filename):
        if contents is not None:
            df, table_name, sampled_df = upload_file_processing(contents, filename)
            table_name = filename.split(".")[0]
            basic_prompt, table_schema = setup_data_chat(None, table_name, False, df)
            return (
                "you have uploaded the data: {}".format(table_name),
                basic_prompt,
                table_schema,
                display_data_table(df.head()),
            )
        else:
            return "", "", [], []

    @app.callback(
        Output("data-table-schema", "data"),
        Output("data-table-schema", "columns"),
        Input(component_id="checklist", component_property="value"),
        [Input("data-table-schema-store", "data")],
    )
    def update_table(checklist_value, data_from_store):
        if "checkbox_val" in checklist_value and data_from_store:
            df = pd.DataFrame(data_from_store)
            columns = [{"name": col, "id": col} for col in df.columns]
            return df.to_dict("records"), columns
        else:
            return [], []

    @app.callback(
        Output("hidden-div-chat-history", "data"),
        Output("hidden-div-chat-output-parsed", "data"),
        Input("send-button", "n_clicks"),
        State("user-input", "value"),
        State("hidden-div-chat-history", "data"),
        Input("file-selector-store", "data"),  # This is the data from the file selector
    )
    def update_conversation(
        n_clicks, input_value, chat_history_dict, instructions_prompt
    ):
        if n_clicks is None:
            return chat_history_dict
        if not chat_history_dict:
            chat_history_dict = []
        try:
            chat_history_obj = [
                dict_to_chat_obj(chat) for chat in chat_history_dict
            ]  # Convert chat history to chat objects
        except:
            chat_history_obj = []
        if input_value:
            chat_history_dict.append({"user": True, "message": input_value})
            response, parsed_rsp_dict = sql_chat(
                input_value, chat_history_obj, instructions_prompt
            )
            chat_history_display = chat_history_dict.copy()
            try:
                chat_history_dict.append({"user": False, "message": response.content})
            except:
                chat_history_dict.append({"user": False, "message": None})
            chat_history_display.append({"user": False, "message": parsed_rsp_dict})
            return chat_history_dict, chat_history_display
        else:
            return chat_history_dict, {}

    @app.callback(
        Output("chat-output", "children"),
        Input("hidden-div-chat-output-parsed", "data"),
    )
    def update_chat_output(chat_history_dict):
        if not chat_history_dict:
            return ""
        chat_content = []
        # print("app: 148", chat_history_dict, "\n")
        for chat in chat_history_dict:
            # print("apps: 149", chat, "\n")
            message = chat["message"]
            user_or_bot = "You" if chat["user"] else "Bot"
            if user_or_bot == "Bot":
                try:
                    if type(json.loads(message)) == dict:
                        message_dict = json.loads(message)
                        chat_content.append(
                            html.P(
                                [
                                    f"{user_or_bot}: {message_dict['pre']}",
                                    html.Br(),
                                    html.Code(f"{message_dict['sql']}"),
                                    html.Br(),
                                    message_dict["post"],
                                    html.Br(),
                                    html.Br(),
                                    html.Code(
                                        style={"color": "green"},
                                    ),
                                ]
                            )
                        )
                        df = pd.read_json(message_dict["result"], orient="split")
                        table = dash_table.DataTable(
                            data=df.to_dict("records"),
                            columns=[{"name": i, "id": i} for i in df.columns],
                            sort_action="native",  # Enable sorting
                            style_table={"overflowX": "auto"},
                            style_cell={
                                "whiteSpace": "normal",
                                "height": "auto",
                                "textAlign": "left",
                                "color": "white",
                                "backgroundColor": "#313131",
                            },
                            style_data={"whiteSpace": "normal", "height": "auto"},
                            style_header={
                                "backgroundColor": "#515151",
                                "fontWeight": "bold",
                            },
                            page_size=10,
                        )
                        chat_content.append(table)
                    else:
                        chat_content.append(html.P(f"{user_or_bot}: {message}"))
                except:
                    chat_content.append(html.P(f"{user_or_bot}: {message}"))
            else:
                chat_content.append(
                    html.P([f"{user_or_bot}: {message}"], style={"color": "green"})
                )

        return chat_content

    # Send Chat button
    @app.callback(
        Output("user-input", "value"),
        Input("send-button", "n_clicks"),
    )
    def reset_button(n_clicks):
        return ""

    return app
