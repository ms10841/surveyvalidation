import streamlit as st
import pandas as pd

# Required column headers
required_columns = [
    "StartDate", "EndDate", "Status", "Progress", "Duration__in_seconds_", "Finished",
    "RecordedDate", "DistributionChannel", "UserLanguage", "cantril1", "cantril2", 
    "financial_cantril", "promis1", "promis2", "promis3", "K6_1", "K6_2", "K6_3", "K6_4", 
    "K6_5", "K6_6", "mh_tx_v2", "loneliness1", "loneliness2", "loneliness3", "belonging_3", 
    "diener1", "diener2", "diener3", "diener4", "diener5", "diener6", "diener7", "diener8", 
    "expectancy1", "expectancy2", "binge", "campus1", "campus2", "campus3", "campus4", 
    "campus5", "discrimination1", "discrimination2_2", "discrimination2_10", 
    "discrimination2_1", "discrimination2_3", "discrimination2_4", "discrimination2_5", 
    "discrimination2_6", "discrimination2_7", "discrimination2_8", "discrimination2_9", 
    "discrimination2_9_TEXT", "discrimination3", "dem1", "dem2", "dem3", "dem4", "dem5_1", 
    "dem6", "dem7", "dem8", "dem9", "dem10_1", "dem10_2", "dem10_3", "dem10_4", "dem10_5", 
    "dem10_6", "dem10_7", "dem10_8", "dem10_9", "dem10_9_TEXT", "dem11", "Q145", "Q140", 
    "Q147", "Q148", "promis1_recode", "promis2_recode", "promis3_recode", "k6_sum", 
    "diener_sum", "cantril_categorical2", "loneliness_sum", "expectancy_value_mean_respondent", 
    "expectancy_value_mean_total", "expectancy_value_stdev", "expectancy_value_cut", 
    "expectancy_value_categorical", "promis_composite", "k6_categorical", "mh_tx_categorical", 
    "cantril_categorical", "loneliness_categorical", "diener_categorical", 
    "belonging_single_item_categorical", "binge_frequent", "binge_any", "health_academic_risk", 
    "campus1_friend_categorical", "campus2_learning_categorical", "campus3_extracurricular_categorical", 
    "campus4_mentor_categorical", "campus5_cares_categorical", "discrimination_any", "rdem_gender", 
    "rdem_first_gen", "rdem_international", "rdem_degree"
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
        "StartDate": "datetime64[ns]",
        "EndDate": "datetime64[ns]",
        "RecordedDate": "datetime64[ns]"
    }
    
    # Parse date columns
    for date_column in expected_types.keys():
        if date_column in df.columns:
            try:
                df[date_column] = pd.to_datetime(df[date_column], utc=True)  # Parse UTC datetime
                df[date_column] = df[date_column].dt.tz_convert(None)  # Convert to naive datetime
            except Exception as e:
                return {date_column: str(e)}
    
    incorrect_types = {}
    for column, expected_type in expected_types.items():
        if column in df.columns and df[column].dtype != expected_type:
            incorrect_types[column] = (df[column].dtype, expected_type)
    return incorrect_types
    
import numpy as np

def main():
    st.title("Survey Validation Tool")
    st.write("Welcome to the survey validation tool - this will review the file you upload and provide a message if it matches the correct format.")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # Validate columns
        is_valid, missing_columns = validate_columns(df)
        if not is_valid:
            st.error(f"Missing columns: {', '.join(missing_columns)}")
            return
        
        st.success("All required columns are present.")
        
        # Validate data types
        incorrect_types = validate_data_types(df)
        if incorrect_types:
            for column, error in incorrect_types.items():
                st.error(f"Error in column '{column}': {error}")
            return
        
        st.success("All data types are correct.")
        
        # Filter out rows with any NA values
        df_filtered = df.dropna()
        
        if df_filtered.empty:
            st.warning("No valid records found after filtering out rows with NA values.")
        else:
            # Plot Duration__in_seconds_ as a bar chart
            st.subheader("Duration__in_seconds_ Bar Chart")
            st.bar_chart(df_filtered['Duration__in_seconds_'])
            
            # Calculate statistical summary
            summary = df_filtered['Duration__in_seconds_'].describe()
            avg = summary['mean']
            std_dev = summary['std']
            upper_control_limit = avg + 3 * std_dev
            lower_control_limit = avg - 3 * std_dev
            
            # Display summary table
            st.subheader("Statistical Summary for Duration__in_seconds_")
            summary_table = pd.DataFrame({
                'Statistic': ['Average', 'Standard Deviation', 'Upper Control Limit', 'Lower Control Limit'],
                'Value': [avg, std_dev, upper_control_limit, lower_control_limit]
            })
            st.table(summary_table)

if __name__ == "__main__":
    main()
