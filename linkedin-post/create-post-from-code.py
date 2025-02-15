from google import genai

import os, prompts

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=prompts.CODE_TO_POST_PROMPT
)

print('*'*20)
print(response.text)
print('*'*20)
print(response.model_dump_json(
    exclude_none=True, indent=4))
