import streamlit as st

# Default set
if "OPENAI_API_KEY" not in st.session_state:
    st.session_state["DF_PATH", "DF_SCHEMA"] = "",""

def select_dataset():
    # Dataset dictionary
    dflist = {
        1: 'NYCTLC',
        2: 'Breast Cancer'#,
        #3: 'Exit'
    }

    # Convert the dataset dictionary to a list for the dropdown
    dataset_names = [name for _, name in sorted(dflist.items())]

    # Streamlit UI to select the dataset
    dataset_choice = st.selectbox("Select the dataset", options=dataset_names)

    # Manage exit case
    #if dataset_choice == 'Exit':
        #st.stop()

    # Define paths and schemas for each dataset
    dfpath = {
        'NYCTLC': '../data/NYCTLC-2023-1.parquet',
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

    return dfpath[dataset_choice], dfSchema[dataset_choice]

st.session_state["DF_PATH", "DF_SCHEMA"] = select_dataset()


