import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from pandasai.llm import GoogleGemini
from pandasai import SmartDataframe
from pandasai.responses.response_parser import  ResponseParser
from streamlit_modal import Modal
import numpy as np

load_dotenv()

if 'questions' not in st.session_state:
    questions = [{"title":'Stats',"question":"Provide descriptive statistics on the data?"},
                 {"title":'Correlation',"question":"Draw correlation matrix in seaborn heat map(cmap='RdYlGn') along with annotation??"},
                 {"title":'Pair Plot',"question":"Plot seaborn pairplot against data with hue as survived?"}]
    st.session_state['questions'] = questions
#,{"title":'Correlation',"question":"Plot correlation between age and fare?"}

if 'chart_loaded' not in st.session_state:
    st.session_state['chart_loaded'] = False
if 'dataframe' not in st.session_state:
    st.session_state['dataframe'] = ''

# Set page title and layout
st.set_page_config(layout="wide")

st.title("🤖 AI Agent - Data Insight Dashboard")
# Sidebar for file upload
# st.sidebar.title("📊 AI Agent - Data Analysis")
# uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

class StreamLitResponse(ResponseParser):
    def __init__(self, context) -> None:
        super().__init__(context)

    def format_dataframe(self, result):
        st.dataframe(result['value'],use_container_width=True)
        return

    def format_plot(self, result):
        st.image(result['value'])
        return

    def format_other(self, result):
        st.write(result['value'])
        return

def fetchResponse(dataFrame, question):
    llm = GoogleGemini(api_key=os.getenv("GOOGLE_API_KEY"))
    pandas_agent = SmartDataframe(dataFrame, config={"llm": llm, "response_parser":StreamLitResponse, "verbose": True})
    answer = pandas_agent.chat(question)
    return answer



def execute_question():
    print('Load questions ::: ', st.session_state['questions'])
    for question in st.session_state['questions']:
        title = question['title']
        st.markdown(f'### {title}')
        with st.spinner("Processing..."):
            response = fetchResponse(df, question['question'])
    st.session_state['chart_loaded'] = True

# Load and display data
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state['dataframe'] = df
    # st.sidebar.markdown("### Uploaded Data")
    # st.sidebar.dataframe(df, use_container_width=True, height=300)

    # Expandable full table view
    with st.expander("🔍 View Full Data Table", expanded=False):
        st.dataframe(df, use_container_width=True)
    with st.expander("Ask a question about your data", expanded=False):
        query = st.text_input("Question:")
        if query:
            with st.spinner("Processing..."):
                response = fetchResponse(df, query)

    modal = Modal("Add Chart", key="add_chart_modal")
    if st.button("➕ Add Chart"):
        modal.open()
    if modal.is_open():
        with modal.container():
            columns = st.session_state['dataframe'].select_dtypes(include=np.number).columns.tolist()
            # print("columns :: ", columns, type(columns))
            if 'selected_chart' not in st.session_state:
                st.session_state['selected_chart'] = ''


            def chart_change():
                print('Selected ::: ', st.session_state['selected_chart'])


            chart_option = st.selectbox(
                "Chart?",
                ("Bar Chart", "Correlation Chart", "Stacked Chart"),
                on_change=chart_change
            )

            column_1_option = st.selectbox(
                "Column 1",
                options=columns
            )

            column_2_option = st.selectbox(
                "Column 2",
                options=columns
            )

            column_3_option = st.selectbox(
                "Group By",
                options=columns
            )

            if st.button("Save Chart"):
                query = f'Plot {chart_option} for {column_1_option} vs {column_2_option}?'
                print('question :::: ', query)
                question_obj = {'title': f'{chart_option} - {column_1_option} vs {column_2_option}',
                                'question': query}
                print("type(st.session_state['questions']) :::: ", type(st.session_state['questions']),
                      st.session_state['questions'])
                st.session_state['questions'].append(question_obj)

                print('questions ::: ', st.session_state['questions'])
                modal.close()
    # if not st.session_state['chart_loaded']:
    execute_question()
else:
    st.info("Upload a CSV/Excel file to start data analysis.")

