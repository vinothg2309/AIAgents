import os

from groq import Groq

client = Groq()

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain why fast inference is critical for reasoning models",
        }
    ],
    model="deepseek-r1-distill-llama-70b",
)

print(chat_completion.choices[0].message.content)