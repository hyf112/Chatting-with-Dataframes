import streamlit as st
from openai import OpenAI
import polars as pl
import json
import sys
import os

# Get the absolute directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Calculate 'src' directory path correctly (one level up from current_dir)
src_dir = os.path.dirname(current_dir)

# Add 'src' to the system path if it's not already included
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

import utils.utils as utils


# Function to generate SQL queries using the GPT model
def load_gpt(df_name, df_schema):
    response_message = ""
    prompt = st.text_input("Please input what you want to search for:", key='prompt')

    if st.button("Generate SQL Query"):
        client = OpenAI(api_key=st.session_state["OPENAI_API_KEY"])
        schema_info = df_schema

        messages = [
            {"role": "system", "content": "You are a SQL assistant expert in writing SQL queries for Polars dataframes."},
            {"role": "user", "content": f'Table schema for "{df_name}": {schema_info}'},
            {"role": "user", "content": f"{prompt}. Only give me the SQL query in plaintext in a single line without any markdown or extra tokens"}
        ]

        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=messages,
            temperature=0,
            max_tokens=4096,
            top_p=1,
        )
        
        response_message = response.choices[0].message.content

        # Display the generated SQL query in the Streamlit UI
        #st.text_area("Generated SQL Query:", response_message, height=100)

    return response_message


def main():
    st.set_page_config(page_title="Chat With Your Dataframe", layout="wide")

    st.title("SQL Query Chatbot")

    # Set up default values if keys do not exist
    if "OPENAI_API_KEY" not in st.session_state:
        st.session_state["OPENAI_API_KEY"] = ""
    if "DF_PATH" not in st.session_state:
        st.session_state["DF_PATH"] = ""
    if "DF_SCHEMA" not in st.session_state:
        st.session_state["DF_SCHEMA"] = ""
    if "DATASET_NAME" not in st.session_state:
        st.session_state["DATASET_NAME"] = ""

    # Check for API key, data path, schema, and dataset name
    missing_config = False
    if not st.session_state["OPENAI_API_KEY"]:
        st.warning("Please set up your OpenAI API Key on the settings page.")
        missing_config = True
    if not st.session_state["DF_PATH"]:
        st.warning("Dataset path is not specified. Please configure it on the selecting page.")
        missing_config = True
    if not st.session_state["DF_SCHEMA"]:
        st.warning("Dataset schema is not specified. Please configure it on the selecting page.")
        missing_config = True
    if not st.session_state["DATASET_NAME"]:
        st.warning("Dataset name is not specified. Please configure it on the selecting page.")
        missing_config = True

    if missing_config:
        return  # Stop execution if configuration is missing


    df_path = st.session_state["DF_PATH"]
    df_schema = st.session_state["DF_SCHEMA"]
    df_name = st.session_state["DATASET_NAME"]

    #st.write("Data Path:", df_path)
    #st.write("Data Schema:", df_schema)
    #st.write("Dataset Name:", df_name)

    # Generate SQL query using GPT model
    query = load_gpt(df_name, df_schema)

    # If a query was generated and a data path is available, execute the SQL query
    if query and df_path:
        result_df = utils.execute_sql_query(df_path, query, df_name)
        st.write("Query Results:")
        st.write(result_df)

if __name__ == "__main__":
    main()
