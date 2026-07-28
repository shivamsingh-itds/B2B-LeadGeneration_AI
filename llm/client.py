import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")


client = Groq(api_key=api_key)


def get_llm_response(messages):
    """
    Send messages to Groq and return the LLM response.
    """

    response = client.chat.completions.create(
        # model="llama-3.3-70b-versatile",
        # model="Llama 3.3 70B",
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0,
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content