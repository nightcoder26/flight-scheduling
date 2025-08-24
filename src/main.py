import streamlit as st
import pandas as pd
import google.generativeai as genai


genai.configure(api_key=st.secrets["GENAI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

model = genai.GenerativeModel("gemini-1.5-flash")


# 📊 Load Preloaded Dataset (replace with actual path or cloud URL)
DATA_PATH = "../data/flight_data.xlsx"  # could also be .csv
df = pd.read_excel(DATA_PATH)

# Streamlit Page Setup
st.set_page_config(page_title="✈️ Mumbai Airport Insights", layout="wide")

st.title("✈️ Mumbai Airport Flight Insights Assistant")
st.write("Ask questions about flight schedules, congestion, delays, and more.")

# Show preview
with st.expander("📊 Preview of Flight Data"):
    st.dataframe(df.head(20))

# Convert sample to text for LLM
data_sample = df.head(50).to_csv(index=False)


# 💬 User Query Input
st.subheader("💬 Ask a Question")
user_prompt = st.text_area(
    "Enter your query:",
    placeholder="e.g., Which is the most congested departure time? What is the expected delay in peak hours?"
)

# Generate Insights
if st.button("Get Insights"):
    if user_prompt.strip() == "":
        st.warning("Please enter a query first.")
    else:
        with st.spinner("Thinking..."):
            try:
                prompt = f"""
                You are analyzing real flight data from Mumbai airport.
                Here is a sample of the dataset:\n{data_sample}\n
                The user query is:\n{user_prompt}
                Answer with insights based on patterns in the dataset.
                """

                response = model.generate_content(prompt)
                st.success("Result:")
                st.write(response.text)

            except Exception as e:
                st.error(f"Error: {str(e)}")
