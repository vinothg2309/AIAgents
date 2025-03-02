from browser_use import Agent
import asyncio
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

async def main():
    agent = Agent(
        task="""Goto google travel, search hotels in Europe with best deals between 20th and 25th March. Return the hotel name, price and full web URL to book hotel in json format.""",
        llm=llm,
    )
    agent = Agent(
        task="""Find the cheapest nonstop flight from Dubai to CHN (Chennai) in economy and business class for tomorrow for one passenger.""",
        llm=llm,
    )

    agent = Agent(
        task="""Goto google travel, search hotels in Europe with best deals between 20th and 25th March. Return the hotel name, price and full web URL to book hotel in json format.""",
        llm=llm,
    )
    response = await agent.run()
    print('*'*20,'Response','*'*20)
    print(response)

asyncio.run(main())