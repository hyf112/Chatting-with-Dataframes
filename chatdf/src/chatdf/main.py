from openai import OpenAI
import utils.utils as utils
import polars as pl
import json


def select_df():
    try:
        while True:
            dflist ={
                1: 'NYCTLC',
                2: 'Breast Cancer',
                3: 'Exit'
            }
            print("Select the dataset")
            print("================================")
            print (json.dumps(dflist, indent=2))
            usrInput = int(input("Select the dataset you want to load from:"))
            if usrInput > len(dflist):
                print("Input invalid!, Please try again.")
            if usrInput == len(dflist):
                raise ValueError("User exited the program without a valid option!")
            else:
                df = dflist[usrInput]
                break
    except Exception as e:
       print(f'{e}')
       exit(1)
    dfpath = {
        'NYCTLC' : '../../data/NYCTLC-2023-1.parquet'
    } 

    dfSchema = {
        'NYCTLC' :   """VendorID, int64
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
                        airport_fee, float64"""
    } 
    return dfpath[df], dfSchema

def load_gpt(dfSchema):
    print("Schema of Dataframe:")
    for i in dfSchema.values():
        print(i)
    prompt = input("Please input what you want to search for:")
    client = utils.openai_setup()
    messages=[
        {"role": "system", "content": "You are a sql assistant. Who is an expert in writing sql queries for polars dataframes.\
          The first Prompt, would be the schema and the datatypes. I want a result out in text format."},
        {"role": "user", "content": f'{dfSchema}'},
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
    response_message = response.choices[0].message
    print(response_message.content)
    return response_message.content

def load_polars(dfpath,response_message):
    df = utils.pl_loadLazy(dfpath, response_message)
    print(df)
    return df


if __name__ == "__main__":
        df_path, df_schema = select_df()
        gpt_res = load_gpt(dfSchema=df_schema)
        pl_res = load_polars(response_message=gpt_res, dfpath=df_path)
    