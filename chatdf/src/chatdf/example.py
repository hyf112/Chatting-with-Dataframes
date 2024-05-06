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

#response_message = "SELECT * FROM df LIMIT 10"
#data_path = '/Users/ivan/Georgetown/5400/Chatting-with-Dataframes/chatdf/data/NYCTLC-2023-1.parquet'
#res = utils.pl_loadLazy(data=data_path, response_message=response_message)
#print(res)

import polars as pl
import duckdb

def execute_sql_query(data_path, query):
    # Load the dataset with Polars
    df = pl.read_parquet(data_path)
    
    # Initialize a DuckDB connection
    con = duckdb.connect()

    # Register the Polars DataFrame as a view within DuckDB
    con.register("df", df)

    # Execute SQL query and fetch the result as an Arrow Table
    arrow_table = con.execute(query).fetch_arrow_table()
    
    # Convert Arrow Table to Polars DataFrame
    result = pl.from_arrow(arrow_table)
    
    # Close the connection
    con.close()

    return result

# Example usage
data_path = '/Users/ivan/Georgetown/5400/Chatting-with-Dataframes/chatdf/data/NYCTLC-2023-1.parquet'
#query = "SELECT * FROM df LIMIT 10"
#query = "SELECT COUNT(*) FROM table_name"
query = "SELECT COUNT(*) FROM NYCTLC"

result = execute_sql_query(data_path, query)
print(result)

#res = utils.pl_loadLazy(data_path, query)
#print(res)

