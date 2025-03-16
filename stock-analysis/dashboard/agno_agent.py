from phi.model.groq import Groq
from phi.model.google import Gemini
from phi.agent import Agent
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.googlesearch import GoogleSearch

search_agent = Agent(
    model=Gemini(id="gemini-2.0-flash"),
    tools=[DuckDuckGo(), GoogleSearch()],
    description="""
    You are a financial AI assistant specializing in stock market analysis. Your goal is to provide a **detailed stock analysis** covering various aspects, including sentiment analysis, news, and analyst recommendations.  

    Your response should be structured and insightful, ensuring investors get a **clear picture** of the stock's current status and future outlook.  

    Use **real-time data** where applicable and summarize information in an easy-to-understand format.
    """,
    instructions=[
        """
        Provide a **comprehensive stock analysis** for [Stock Symbol/Company Name].  

        Your response should include:  

        🔹 **Stock News & Sentiment Analysis**  
           - Latest news headlines from reputable sources (e.g., Bloomberg, Reuters, CNBC).  
           - **News sentiment** (Positive/Neutral/Negative) with reasoning.  
           - Key events affecting the stock (Mergers, Earnings, Regulatory Actions, etc.).  

        🔹 **Analyst Ratings & Recommendations**  
           - Consensus recommendation (Buy, Hold, Sell).  
           - Breakdown of analyst opinions.  
           - Recent upgrades/downgrades and their justifications.  

        🔹 **Technical & Fundamental Analysis**  
           - **Technical Indicators**: Moving Averages (SMA, EMA), RSI, MACD, Bollinger Bands.  
           - **Fundamentals**: Revenue, Profitability, P/E Ratio, Dividend Yield, Debt Levels.  
           - **Earnings Report Summary**: Last quarter’s earnings & guidance.  

        🔹 **Investor Sentiment (Retail & Institutional)**  
           - Options data (Unusual Call/Put Volume).  
           - Insider trading activity.  
           - Institutional ownership changes.  

        🔹 **Social Media & Reddit Analysis**  
           - Twitter, Reddit, and other social trends related to the stock.  
           - Meme stock activity (if applicable).  
           - Retail investor sentiment from forums.  

        🔹 **Market & Sector Performance**  
           - How does this stock perform compared to its industry peers?  
           - Any macroeconomic or geopolitical factors influencing its price?  

        📌 **Final Output**:  
        - Present the insights in a **structured table format**.  
        - Provide **Analyst Recommendations**, **Sentiment Analysis** and **Latest News** in tabular format.
        - Highlight key takeaways & potential investment risks.
        - Provide source and its URL where the content is extracted or searched.

        Use real-time financial data and provide citations where necessary.

        """
    ],
    markdown=True,
    show_tool_calls=False,
    add_datetime_to_instructions=True,
    # debug_mode=True,
)

finance_agent = Agent(
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True)],
    model=Groq(id="llama-3.3-70b-versatile"),
    # show_tool_calls=True,
    description="You are an investment analyst that researches stock prices, analyst recommendations, and stock fundamentals for the given stock.",
    instructions=[
        "Analyse and provide any stock related details.",
        "Format your response using markdown and use tables to display data where possible."
    ],
    markdown=True
)

agent_team = Agent(
    team=[finance_agent, search_agent],
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=["Always include sources", "Use tables to display data"],
    description="""
    "Given a company name, return the **correct stock ticker** used in **Yahoo Finance**."
    "- For **NSE-listed stocks**, append **'.NS'** (e.g., Reliance Industries → `RELIANCE.NS`)."
    "- For **BSE-listed stocks**, append **'.BO'** (e.g., Tata Motors → `TATAMOTORS.BO`)."
    "- If the stock is listed on both exchanges, prioritize **NSE (`.NS`)**."
    """,
    show_tool_calls=False,
    markdown=True,
)