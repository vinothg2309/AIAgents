import os

from phi.model.groq import Groq
from phi.agent import Agent
from phi.tools.yfinance import YFinanceTools
from phi.model.google import Gemini

agent = Agent(
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True)],
    model = Groq(id="llama-3.3-70b-versatile"),
    # model=Gemini(id="gemini-1.5-flash",api_key=os.getenv('GEMINI_API_KEY')),
    # show_tool_calls=True,
    description="You are an investment analyst that researches stock prices, analyst recommendations, and stock fundamentals."
                "Given a company name, return the **correct stock ticker** used in **Yahoo Finance**."
                "- For **NSE-listed stocks**, append **'.NS'** (e.g., Reliance Industries → `RELIANCE.NS`)."
                "- For **BSE-listed stocks**, append **'.BO'** (e.g., Tata Motors → `TATAMOTORS.BO`)."
                "- If the stock is listed on both exchanges, prioritize **NSE (`.NS`)**.",
    instructions=["Format your response using markdown and use tables to display data where possible."],
    markdown=True
)
# agent.print_response("Share the IDFC First bank stock price and analyst recommendations", markdown=True)
# agent.print_response("What is 52 week low and high price of PayPal?")

# Share the IDFC First bank stock price and analyst recommendations?
# What is PayPal's 52 week low?
# Share the IDFC First bank stock price and analyst recommendations?
# What is the PE and PB ratio of Microsoft?
# What is the dividend yield of ITC?

response = agent.run("Share the IDFC First bank stock price and analyst recommendations?")

print(response.content)
print('type(response) :::: ', type(response))
