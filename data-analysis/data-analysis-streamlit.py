import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from pandasai.llm import GoogleGemini
from pandasai import SmartDataframe
from pandasai.responses.response_parser import  ResponseParser

load_dotenv()

print(os.getenv("GOOGLE_API_KEY"))

# Set page title and layout
st.set_page_config(page_title="AI Agent - Data Analysis", layout="wide")

# Sidebar for file upload
st.sidebar.title("📊 AI Agent - Data Analysis")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])


class StreamLitResponse(ResponseParser):
    def __init__(self, context) -> None:
        super().__init__(context)

    def format_dataframe(self, result):
        st.dataframe(result['value'])
        return

    def format_plot(self, result):
        st.image(result['value'])
        return

    def format_other(self, result):
        st.write(result['value'])
        return

def fetchResponse(dataFrame, question):
    llm = GoogleGemini(api_key=os.getenv("GOOGLE_API_KEY"))
    pandas_agent = SmartDataframe(dataFrame, config={"llm": llm, "response_parser":StreamLitResponse})
    answer = pandas_agent.chat(question)
    return answer

# Load and display data
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.markdown("### Uploaded Data")
    st.sidebar.dataframe(df, use_container_width=True, height=300)

    # Expandable full table view
    with st.expander("🔍 View Full Data Table", expanded=False):
        st.dataframe(df, use_container_width=True)

    # AI Chat Interface
    st.title("🤖 AI Chat for Data Analysis")
    st.markdown("Type a question about your dataset and get AI-powered insights.")

    # Initialize PandasAI with OpenAI LLM
    # llm = OpenAI(api_token="your-openai-api-key")  # Replace with your API key
    # pandas_ai = PandasAI(llm)
    # llm = GoogleGemini()

    query = st.text_input("Ask a question about your data:")
    if query:
        with st.spinner("Processing..."):
            response = fetchResponse(df, query)
            # st.write(response)
else:
    st.info("Upload a CSV file to start data analysis.")

