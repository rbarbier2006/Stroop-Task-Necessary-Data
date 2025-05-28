import streamlit as st
import pandas as pd
import io

st.title("CSV Response Accuracy Analyzer")

# Upload two CSV files
uploaded_file1 = st.file_uploader("Upload First CSV File", type=["csv"])
uploaded_file2 = st.file_uploader("Upload Second CSV File", type=["csv"])

if uploaded_file1 and uploaded_file2:
    try:
        def clean_csv(file):
            df = pd.read_csv(file, skiprows=4, engine="python")
            df = df.iloc[:, [18, 19, 20]]
            df.columns = ['S', 'T', 'U']
            return df

        # Clean both files
        df1 = clean_csv(uploaded_file1)
        df2 = clean_csv(uploaded_file2)
        combined_df = pd.concat([df1, df2], ignore_index=True)

        # Convert types
        combined_df['S'] = combined_df['S'].astype(str)
        combined_df['U'] = combined_df['U'].astype(str)
        combined_df['T'] = pd.to_numeric(combined_df['T'], errors='coerce')

        # Keep going with analysis...

except Exception as e:
    st.error(f"❌ Error: {e}")
