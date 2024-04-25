from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai
from openai import OpenAI
import polars as pl



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

