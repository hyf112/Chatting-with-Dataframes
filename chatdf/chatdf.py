import pathlib
import textwrap
import timeit
from dotenv import load_dotenv
import os

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

load_dotenv()


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))



def gemini_model():
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("""I want to generate queries for a duckdb dataframe.\
                                         Please write a SQL query to Find out all combinations \
                                         of PULocationID and DOLocationID which constitute more than \
                                         0.1 percent of the total trips based on the dataframe structure below. 
                                         I want the output in text block.
                                         VendorID   int64
                                         tpep_pickup_datetime     datetime64[us]
                                         tpep_dropoff_datetime    datetime64[us]
                                         passenger_count                 float64
                                         trip_distance                   float64
                                         RatecodeID                      float64
                                         store_and_fwd_flag               object
                                         PULocationID                      int64
                                         DOLocationID                      int64
                                         payment_type                      int64
                                         fare_amount                     float64
                                         extra                           float64
                                         mta_tax                         float64
                                         tip_amount                      float64
                                         tolls_amount                    float64
                                         improvement_surcharge           float64
                                         total_amount                    float64
                                         congestion_surcharge            float64
                                         airport_fee                     float64""")
    print(response.text)


if __name__ == '__main__':
    gemini_setup()
    gemini_model()
    