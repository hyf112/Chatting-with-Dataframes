import streamlit as st

# Default set
if "DF_PATH" not in st.session_state:
    st.session_state["DF_PATH"] = ""
if "DF_SCHEMA" not in st.session_state:
    st.session_state["DF_SCHEMA"] = ""
if "DATASET_NAME" not in st.session_state:
    st.session_state["DATASET_NAME"] = ""

def select_dataset(dataset_choice):
    # Define paths and schemas for each dataset
    dfpath = {
        'NYCTLC': 'https://github.com/hyf112/Chatting-with-Dataframes/raw/main/chatdf/data/NYCTLC-2023-1.parquet',
        'Breast Cancer': '../data/BreastCancer-2023-1.parquet'  # Placeholder path
    }

    dfSchema = {
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
                    airport_fee, float64""",
        'Breast Cancer': """Feature1, float64
                            Feature2, float64
                            Feature3, float64
                            Outcome, int64"""  # Placeholder schema
    }

    return dataset_choice, dfpath[dataset_choice], dfSchema[dataset_choice]

# Dataset dictionary
dflist = {
    1: 'NYCTLC',
    2: 'Breast Cancer'
}

# Convert the dataset dictionary to a list for the dropdown
dataset_names = [name for _, name in sorted(dflist.items())]

# Streamlit UI to select the dataset
dataset_choice = st.selectbox("Select the dataset", options=dataset_names)

if st.button('Save Selection'):
    # Get the dataset name, path, and schema based on the selected dataset
    selected_dataset, df_path, df_schema = select_dataset(dataset_choice)

    # Update session state
    st.session_state["DF_PATH"] = df_path
    st.session_state["DF_SCHEMA"] = df_schema
    st.session_state["DATASET_NAME"] = selected_dataset
    st.success("Dataset selection saved!")

