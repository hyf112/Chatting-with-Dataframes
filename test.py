from openai import OpenAI
from utils import openai_setup

client = openai_setup()

messages=[
    {"role": "system", "content": "You are a sql assistant. Who is an expert in writing sql queries.\
      The first Prompt, would be the schema and the datatypes. I want a result out in text format."},
    {"role": "user", "content": """VendorID, int64
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
                                    airport_fee, float64"""},
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
response_message = response.choices[0].message
print(response_message)
