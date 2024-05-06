from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai
from openai import OpenAI
import polars as pl
import streamlit as st
import duckdb


def gemini_setup():
    api_key = os.getenv('API_KEY')
    genai.configure(api_key=api_key)

    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
    except Exception:
        raise Exception("Please check your API key")
    
def openai_setup():
    client = OpenAI(api_key=os.environ.get('Openai'))
    return client


def pl_loadLazy(data_path, response_message):
    NYCTLC = pl.read_parquet(data_path).lazy()
    with pl.SQLContext(register_globals=True) as NYCTLC:
        res = NYCTLC.execute(response_message+";").collect()

    return res


def execute_sql_query(data_path, query, df_name):

    # Load the dataset with Polars
    df = pl.read_parquet(data_path)
    # Initialize a DuckDB connection
    con = duckdb.connect()
    # # Register the Polars DataFrame as a view within DuckDB, using df_name as the alias in the SQL context
    con.register(df_name, df)
    # Convert Arrow Table to Polars DataFrame
    arrow_table = con.execute(query).fetch_arrow_table()
    # Convert Arrow Table to Polars DataFrame
    result = pl.from_arrow(arrow_table)
    # Close the connection
    con.close()

    return result

