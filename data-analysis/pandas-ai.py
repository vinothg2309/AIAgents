from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

print(os.getenv("GOOGLE_API_KEY"))

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

df = pd.read_csv(
    "https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv"
)

agent = create_pandas_dataframe_agent(llm, df, verbose=True,allow_dangerous_code=True)

# print(agent.invoke("how many rows are there?"))

# print(agent.invoke("how many peoples are servived?"))

# print(agent.invoke("whats the square root of the average age?"))

print(agent.invoke("Draw a bar chart for number of people survived vs not survived?"))

print(agent.invoke("Draw a stacked chart for number of people survived vs not survived group by gender?"))



