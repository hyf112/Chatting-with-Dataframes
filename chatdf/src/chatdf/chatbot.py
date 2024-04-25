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
def load_gpt(df_schema): 
    
    prompt = st.text_input("Please input what you want to search for:", key='prompt')

    if st.button("Generate SQL Query"):
        client = OpenAI(api_key=st.session_state["OPENAI_API_KEY"])
        messages=[
        {"role": "system", "content": "You are a sql assistant. Who is an expert in writing sql queries for polars dataframes.\
          The first Prompt, would be the schema and the datatypes. I want a result out in text format."},
        {"role": "user", "content": f'{df_schema}'},
        {"role": "user", "content": f"{prompt}. \
                                    Only give me the SQL query in plaintext in a single line without any markdown or extra tokens"}
      ]

        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=messages,
            temperature=0,
            max_tokens=4096,
            top_p=1,
            )
        
        response_message = response.choices[0].message.content

        #res = utils.pl_loadLazy(data='/Users/ivan/Georgetown/5400/Chatting-with-Dataframes/chatdf/data/NYCTLC-2023-1.parquet', response_message=response_message)

        st.text_area("Generated SQL Query:", response_message, height=100)
    return response_message
    #return res

def main():
    # Default set
    if "OPENAI_API_KEY" not in st.session_state:
        st.session_state["OPENAI_API_KEY"] = ""
    
    if "DF_PATH" not in st.session_state:
        st.session_state["DF_PATH"] = '../data/NYCTLC-2023-1.parquet'
    
    if "DF_SCHEMA" not in st.session_state:
        st.session_state["DF_SCHEMA"] = {
        'NYCTLC': """VendorID, int64
                    tpep_pickup_datetime, datetime64[us]
                    tpep_dropoff_datetime, datetime64[us]
                    passenger_count, float64
                    trip_distance, float64
                    RatecodeID, float64
                    store_and_fwd_flag, object
                    PULocationID, int64
                    DOLocationID, int64
                    payment_type, int64
                    fare_amount, float64
                    extra, float64
                    mta_tax, float64
                    tip_amount, float64
                    tolls_amount, float64
                    improvement_surcharge, float64
                    total_amount, float64
                    congestion_surcharge, float64
                    airport_fee, float64"""}

    st.set_page_config(page_title="Chat With Your Dataframe", layout="wide")

    st.title("SQL Query Chatbot")

    # Check if user enters api key
    if st.session_state["OPENAI_API_KEY"] == "":
        st.warning("Please set up your OpenAI API Key in the setting page.")

    df_path, df_schema = st.session_state["DF_PATH", "DF_SCHEMA"]

    # Generate SQL query using GPT model
    query = load_gpt(df_schema)

    
if __name__ == "__main__":
    main()
