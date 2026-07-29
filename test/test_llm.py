from llm.client import get_llm_response


messages = [
    {
        "role": "user",
        "content": "Return only the word WORKING."
    }
]

response = get_llm_response(messages)

print(response)