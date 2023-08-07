"""
Functions to setup Prompts and Chat with OpenAI
"""
import os
import re
import sqlite3
import pandas as pd
import json
import openai
from langchain.schema import ChatMessage
from langchain.chat_models import ChatOpenAI
from utils.data_helpers import (
    sample_dataframe,
)

conn = sqlite3.connect("test_db", check_same_thread=False)


def generate_defintion(df, table_name):
    csv_data = df.to_csv(index=False)
    csv_dtypes = df.dtypes
    instructions_prompt = f"""You are a data analyst.
        Your job is to create a DESCRIPTION for each FIELD_NAME from data sample below provide the response in the OUTPUT_FORMAT provided.
        
        Here is the data to create each FIELD_NAME DESCRIPTION {csv_data}.
        
        The TABLE_NAME is {table_name}.
        
        The DATA_TYPE are in {csv_dtypes}.  These DATA_TYPES will need to be converted to sqlite datatypes.
        
        Include the Headers on top the response.
        
        OUTPUT_FORMAT
        TABLE_NAME\tFIELD_NAME\tDESCRIPTION\tDATA_TYPE
        """
    chat_history = []
    chat_history.append(ChatMessage(role="assistant", content=instructions_prompt))
    openai.api_key = os.getenv("OPENAI_API_KEY")
    chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    response = chat(chat_history)
    return response.content


def setup_data_chat(filename, table_name, common_dataset=True, upload_df=None):
    input_df = upload_df.copy()
    input_df.columns = input_df.columns.str.lower()
    sampled_df = sample_dataframe(input_df)
    table_rsp = generate_defintion(sampled_df, table_name)
    data_list = [line.split("\t", 3) for line in table_rsp.strip().split("\n")]
    df = pd.DataFrame(data_list[1:], columns=data_list[0])
    csv_data = df.to_csv(index=False)

    input_df.to_sql(table_name, conn, if_exists="replace", index=False)

    instructions_prompt = f"""You are a sqlite3 SQL analyst.  
        Your job is to write very good SQL queries.

        Use the previous SQL queries as a guide as memory when you write your next SQL query.

        Only use the TABLE_NAME for SQL query table name that is provided in the table definition.  DO NOT MAKE UP table names. 

        Only use the FIELD_NAME for SQL query field names that is provided in the table definition. DO NOT MAKE UP field names.

        You MUST provide the SQL code in a code block.

        You MUST provide SQL code in an answer.  If you cannot create a valid SQL query, then let the user know that you cannot create a valid SQL query.
        
        Here are the table names, fields, descriptions, and data types:"""
    combined_prompt = instructions_prompt + csv_data

    return combined_prompt, df.to_dict("records")


def extract_sql_info(payload):
    pattern = re.compile(r"(.*?)```sql\n(.*?)\n```(.*)", re.DOTALL)
    match = pattern.match(payload)
    if match:
        return {
            "pre": match.group(1).strip(),
            "sql": match.group(2).strip(),
            "post": match.group(3).strip(),
        }
    else:
        return {"pre": None, "sql": None, "post": None}


UNABLE_TO_CREATE_SQL_MESSAGE = "Unable to create SQL query for that question.  Please try again by re-wording your question, or refresh page to start over."


def sql_chat(prompt: str, chat_history: list, instructions_prompt: str):
    if len(instructions_prompt) == 0:
        return {}, "Please first Upload a dataset."
    if len(chat_history) == 0:
        chat_history.append(ChatMessage(role="assistant", content=instructions_prompt))
    chat_history.append(ChatMessage(role="user", content=prompt))

    openai.api_key = os.getenv("OPENAI_API_KEY")
    chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    response = chat(chat_history)
    chat_history.append(ChatMessage(role="assistant", content=response.content))

    try:
        parsed_hist_dict = extract_sql_info(response.content)
        try:
            sql_formatted = parsed_hist_dict["sql"].replace("\n", " ")
        except:
            return (
                response,
                UNABLE_TO_CREATE_SQL_MESSAGE,
            )
        if sql_formatted is not None:
            df = pd.read_sql(sql_formatted, conn)
            output_rsp_dict = parsed_hist_dict.copy()
            output_rsp_dict["result"] = df.to_json(orient="split", index=False)
            return response, json.dumps(output_rsp_dict)
        else:
            return (
                response,
                UNABLE_TO_CREATE_SQL_MESSAGE,
            )

    except Exception as e:
        print("chat 216 exception", e)
        if sql_formatted is not None:
            output = (
                f"""The {sql_formatted} is not valid.  {UNABLE_TO_CREATE_SQL_MESSAGE}"""
            )
        elif "table" in response.content:
            output = UNABLE_TO_CREATE_SQL_MESSAGE
        else:
            if len(sql_formatted) > 0:
                output = f"""The {sql_formatted} is not valid.  {UNABLE_TO_CREATE_SQL_MESSAGE}"""
            else:
                output = UNABLE_TO_CREATE_SQL_MESSAGE
        return response, output
