from phi.model.groq import Groq
from phi.agent import Agent
from phi.tools.yfinance import YFinanceTools

agent = Agent(
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True)],
    model = Groq(id="llama-3.3-70b-versatile"),
    show_tool_calls=True,
    description="You are an investment analyst that researches stock prices, analyst recommendations, and stock fundamentals.",
    instructions=["Format your response using markdown and use tables to display data where possible."],
)
agent.print_response("Share the NVDA stock price and analyst recommendations", markdown=True)
