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

        # Identify correct responses (S == U)
        correct_df = combined_df[combined_df['S'] == combined_df['U']]
        num_correct = len(correct_df)
        total_responses = len(combined_df)
        percent_accuracy = num_correct / total_responses if total_responses else 0

        # Mean and SD of column T (response time) for correct responses
        mean_rt = correct_df['T'].mean()
        sd_rt = correct_df['T'].std()

        # Display results
        result_df = pd.DataFrame([{
            "Mean RT": round(mean_rt, 2),
            "SD RT": round(sd_rt, 2),
            "Accurate Responses": num_correct,
            "Percent Accuracy": round(percent_accuracy, 4)
        }])

        st.success("✅ Analysis complete!")
        st.dataframe(result_df)

        # Prepare Excel file with stats + raw data
        final_df = pd.concat([result_df, combined_df], ignore_index=True)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            final_df.to_excel(writer, index=False)

        # Download button
        st.download_button(
            label="📥 Download Full Excel Report",
            data=output.getvalue(),
            file_name="analysis_output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")
