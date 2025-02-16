import streamlit as st
from phi.model.groq import Groq
from phi.agent import Agent
from phi.tools.yfinance import YFinanceTools

# Set Streamlit Page Config
st.set_page_config(page_title="Stock Info AI", page_icon="📈", layout="wide")

# OpenAI API Key Input
openai_api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

# Define a tool to fetch stock details
def initialize_agent() -> dict:
    agent = Agent(
        tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True)],
        model = Groq(id="llama-3.3-70b-versatile"),
        # show_tool_calls=True,
        description="You are an investment analyst that researches stock prices, analyst recommendations, and stock fundamentals."
                    "Given a company name, return the **correct stock ticker** used in **Yahoo Finance**."
                    "- For **NSE-listed stocks**, append **'.NS'** (e.g., Reliance Industries → `RELIANCE.NS`)."
                    "- For **BSE-listed stocks**, append **'.BO'** (e.g., Tata Motors → `TATAMOTORS.BO`)."
                    "- If the stock is listed on both exchanges, prioritize **NSE (`.NS`)**.",
        instructions=["Format your response using markdown and use tables to display data where possible."],
        markdown=True
    )

    return agent

# Streamlit UI
st.title("📊  AI Agent: Stock Analysis")

stock_symbol = st.text_input("Enter your question")

if st.button("Search"):
   agent = initialize_agent()
# Fetch Stock Data
   with st.spinner("Fetching stock data..."):
       response = agent.run(stock_symbol)
       print("response :::: ", response)
       st.markdown(response.content)

    # Display Results
   # if "Error" in response:
   #     st.error(f"❌ {response['Error']}")
   # else:
   #      st.subheader(f"📈 Stock Details for {response['Name']} ({response['Stock']})")
   #      st.write(f"💰 **Current Price:** {response['Current Price']} INR")
   #      st.write(f"🏦 **Market Cap:** {response['Market Cap']}")
   #      st.write(f"📊 **52 Week High:** {response['52 Week High']} | **52 Week Low:** {response['52 Week Low']}")
   #      st.write(f"📉 **PE Ratio:** {response['PE Ratio']}")
   #      st.write(f"🏢 **Sector:** {response['Sector']} | **Industry:** {response['Industry']}")
   #
   #      # Show Data in a Table
   #      st.table(response)

