import streamlit as st
import pandas as pd
import google.generativeai as genai

# --------------------------
# CONFIG
# --------------------------
GENAI_API_KEY = "your_api_key_here"  # put your Gemini API key here
genai.configure(api_key=GENAI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

# --------------------------
# STREAMLIT UI
# --------------------------
st.set_page_config(page_title="✈️ Flight Data Insights Assistant", layout="wide")

st.title("✈️ Flight Data Insights Assistant")
st.write("Upload your flight dataset (Excel/CSV) and ask questions about schedules, delays, and optimization.")

# --------------------------
# FILE UPLOAD
# --------------------------
uploaded_file = st.file_uploader("Upload Flight Dataset", type=["xlsx", "csv"])

if uploaded_file is not None:
    # Read dataset
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("📊 Preview of Data")
    st.dataframe(df.head(10))

    # Convert dataframe to a compact string to pass to Gemini
    data_sample = df.head(50).to_csv(index=False)  # send only first 50 rows to avoid token limit

    st.subheader("💬 Ask a Question")
    user_prompt = st.text_area("Enter your query:", 
                               placeholder="e.g., Find peak hours for departures, Analyze average delay times...")

    if st.button("Get Insights"):
        if user_prompt.strip() == "":
            st.warning("Please enter a query first.")
        else:
            with st.spinner("Thinking..."):
                try:
                    # Combine dataset + user question
                    prompt = f"""
                    You are analyzing flight data from Mumbai airport.
                    Here is a sample of the dataset:\n{data_sample}\n
                    Now answer the following user query in detail:\n{user_prompt}
                    """

                    response = model.generate_content(prompt)
                    st.success("Result:")
                    st.write(response.text)

                except Exception as e:
                    st.error(f"Error: {str(e)}")

else:
    st.info("⬆️ Please upload a flight dataset (Excel/CSV) to begin.")
