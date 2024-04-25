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

response_message = "SELECT * FROM df LIMIT 10"  # Ensure 'df' matches the registered name
data_path = '/Users/ivan/Georgetown/5400/Chatting-with-Dataframes/chatdf/data/NYCTLC-2023-1.parquet'
res = utils.pl_loadLazy(data=data_path, response_message=response_message)
print(res)