import os
from pydantic import BaseModel, Field
from typing import List
from groq import Groq
import instructor

class Character(BaseModel):
    name: str
    fact: List[str] = Field(..., description="A list of facts about the subject")

# Initialize the Groq client
client = Groq(
    api_key=os.environ.get('GROQ_API_KEY'),
)

client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)

def ask_question(question):
    resp = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        response_model=Character,
    )
    return resp.model_dump_json(indent=2)

if __name__ == "__main__":
    print("You can ask questions to the Groq API. Type 'quit' to exit.")
    while True:
        user_input = input("Ask a question: ")
        if user_input.lower() == "quit":
            print("Exiting the loop.")
            break
        response = ask_question(user_input)
        print(response)
