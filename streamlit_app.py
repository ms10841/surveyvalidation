import streamlit as st
import pandas as pd
import numpy as np

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

def format_duration(seconds):
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    
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
    
def categorize_duration(seconds):
    # Define bins for durations
    bins = [0, 60, 120, 300, 600, 1200, 1800, 3600, 7200, 10800, np.inf]
    labels = ['<1 min', '1-2 mins', '2-5 mins', '5-10 mins', '10-20 mins', '20-30 mins', '30-60 mins', '1-2 hrs', '2-3 hrs', '3+ hrs']
    
    # Categorize duration into bins
    for i in range(len(bins) - 1):
        if bins[i] <= seconds < bins[i + 1]:
            return labels[i]

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
        else:
            st.success("All required columns are present.")
            
            # Validate data types
            incorrect_types = validate_data_types(df)
            if incorrect_types:
                for column, error in incorrect_types.items():
                    st.error(f"Error in column '{column}': {error}")
            else:
                st.success("All data types are correct.")
                
            # Display 5 sample records without NA values
            st.subheader("Sample Records without NA values or completely blank")
            non_na_non_blank_sample = df.head(5)
            st.table(non_na_non_blank_sample)
            
            # Categorize Duration__in_seconds_ into bins
            df['Duration_Category'] = df['Duration__in_seconds_'].apply(categorize_duration)
            
            # Plot frequency of duration categories as a bar chart
            st.subheader("Duration Distribution")
            duration_counts = df['Duration_Category'].value_counts().sort_index()
            st.bar_chart(duration_counts)
            
            # Statistical summary of Duration__in_seconds_
            st.subheader("Statistical Summary for Duration__in_seconds_")
            duration_summary = df['Duration__in_seconds_'].describe()
            duration_summary.loc['mean'] = format_duration(duration_summary['mean'])
            duration_summary.loc['std'] = format_duration(duration_summary['std'])
            duration_summary.loc['min'] = format_duration(duration_summary['min'])
            duration_summary.loc['25%'] = format_duration(duration_summary['25%'])
            duration_summary.loc['50%'] = format_duration(duration_summary['50%'])
            duration_summary.loc['75%'] = format_duration(duration_summary['75%'])
            duration_summary.loc['max'] = format_duration(duration_summary['max'])
            
            st.table(duration_summary[['mean', 'std', 'min', '25%', '50%', '75%', 'max']])


if __name__ == "__main__":
    main()
