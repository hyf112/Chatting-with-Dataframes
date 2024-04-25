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


# Default set
if "OPENAI_API_KEY" not in st.session_state:
    st.session_state["OPENAI_API_KEY"] = ""

st.set_page_config(page_title="Chat With Your Dataframe", layout="wide")

st.title("SQL Query Chatbot")

# Check if user enters api key
if st.session_state["OPENAI_API_KEY"] == "":
    st.warning("Please set up your OpenAI API Key in the setting page.")

df_path, df_schema = st.session_state["DF_PATH", "DF_SCHEMA"]

if df_path:  # Check if a dataset path was returned
        # Load dataset using Polars
        try:
            df = pl.read_parquet(df_path)
            
            # Display the first few rows of the dataset
            st.write("Preview of the Dataset:", df.head())

            # Display basic statistics
            st.write("Basic Statistics:")
            st.write(df.describe())

        except Exception as e:
            st.write("Current working directory:", os.getcwd())
            st.error(f"Failed to load the dataset: {e}")

# Function to load GPT with a schema and query generation
def load_gpt(dfSchema):
    client = OpenAI(api_key=st.session_state["OPENAI_API_KEY"])
    messages = [
        {"role": "system", "content": "You are a sql assistant. Who is an expert in writing sql queries.\
          The first Prompt, would be the schema and the datatypes. I want a result out in text format."},
        {"role": "user", "content": f'{dfSchema}'},
        {"role": "user", "content": "Give me the average fare amount when passenger count is greater than 2. \
                                    Only give me the query in plaintext without any markdown or extra tokens"}
    ]

    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=messages,
        temperature=0,
        max_tokens=4096,
        top_p=1,
    )
    return response.choices[0].message


if __name__ == "__main__":
    main()
