import os
from openai import OpenAI
import polars as pl
import streamlit as st
import duckdb


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

