import streamlit as st
import pandas as pd

# Required column headers based on PncImportDb.dbo.IMMUNIZATIONIMPORT
required_columns = [
    "RecordID", "PRIMARYKEY", "ACTION", "ID", "FIRSTNAME", "LASTNAME", "DOB",
    "EVENTCODE", "EVENTNAME", "EVENTDATE", "ADDITIONALDATE", "BRANDNAME",
    "MANUFACT", "LOTNUM", "ADMINBY", "RSLTCODE", "RSTLNUM", "LOC_CODE",
    "LOC_DESC", "ACTIONDATE", "EDITDATE", "DELETEDATE"
]

def validate_columns(df):
    """ Validate the presence of required columns """
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, missing_columns
    return True, None

def validate_data_types(df):
    """ Validate data types of certain columns """
    # Define expected data types
    expected_types = {
        "RecordID": "int64",
        "DOB": "datetime64[ns]",
        "EVENTDATE": "datetime64[ns]",
        "ADDITIONALDATE": "datetime64[ns]",
        "ACTIONDATE": "datetime64[ns]",
        "EDITDATE": "datetime64[ns]",
        "DELETEDATE": "datetime64[ns]"
    }
    
    incorrect_types = {}
    for column, expected_type in expected_types.items():
        if column in df.columns and df[column].dtype != expected_type:
            incorrect_types[column] = (df[column].dtype, expected_type)
    return incorrect_types

def main():
    st.title("CSV Upload and Validation")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # Validate columns
        is_valid, missing_columns = validate_columns(df)
        if not is_valid:
            st.error(f"Missing columns: {', '.join(missing_columns)}")
        else:
            st.success("All required columns are present.")
            
            # Validate data types
            incorrect_types = validate_data_types(df)
            if incorrect_types:
                for column, (actual_type, expected_type) in incorrect_types.items():
                    st.error(f"Incorrect data type for column '{column}': Expected {expected_type}, got {actual_type}")
            else:
                st.success("All data types are correct.")
                
            st.write("Data Preview:", df.head())

if __name__ == "__main__":
    main()
