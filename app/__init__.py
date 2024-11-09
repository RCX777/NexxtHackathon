import time
import os
from datetime import datetime
from flask import Flask, json
from openai import OpenAI, AzureOpenAI
from openperplex import OpenperplexSync

app = Flask(__name__)

# requires AZURE_OPENAI_API_KEY env variable to be set
client_4o = AzureOpenAI(
    api_version="2024-08-01-preview",
    base_url="https://rbro-openai-hackatlon.openai.azure.com/openai/deployments/gpt-4o"
)

perp_api_key = os.environ['PERP_API_KEY']
client_perp = OpenperplexSync(api_key=perp_api_key)

def ask_perplexity(query : str, temp : float = 0.2, top_p : float = 0.9):
    result = client_perp.custom_search(
        system_prompt="You are a highly knowledgeable language model specialized in retrieving precise and up-to-date information from the live web about companies and e-commerce websites. Your output should focus on providing accurate details that can be used to analyze the trustworthiness of these entities. Prioritize factual data, current standings, recent news, user reviews, and any other relevant information that can influence credibility assessments. Ensure the information is clear, detailed, and verifiable to assist in making informed trustworthiness evaluations.",
        user_prompt=query,
        location="ro",
        pro_mode=False,
        search_type="general",
        return_images=False,
        return_sources=True,
        temperature=temp,
        top_p=top_p
    )

    return result['llm_response'], result['sources']

def ask_4o(query : str):
    completion = client_4o.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )

    return str(completion.choices[0].message.content)


def get_questions(name : str):
    return [
        f'Has {name} been involved in any recent controversies?',
        f'Is {name} an untrusted website or company?',
        f'Does {name} have inexistent or bad customer support?',
    ]

def construct_prompt(perplexity_answer : str, question : str):
    # return f"""INSTRUCTION: Please use only the following information, which is in the block delimited by "=====":
    # =====
    # {perplexity_answer}
    # =====
    return f"""INSTRUCTION: Using the given information, answer to the following question, which is delimited by "=====" Answer with a json object containing the "answer" field which is boolean true/false, and "reason" field which is the reason for the given answer. Only output valid JSON. Do not use any extra syntax or characters. Write the JSON after the "CUE:".
    =====
    {question}
    =====
    CUE:
    """

@app.route('/hal/<name>', methods=['GET'])
def hallucinate(name : str):
    query = f"""Please provide me the following information about {name}: Key Facts, Services and Features,
        Notable Innovations and Initiatives, Subsidiaries and Partnerships, Reputation and Trustworthiness and Challenges.        Keep the information concise and relevant."""
    # response = ask_perplexity(query)

    questions = get_questions(name)

    output_json = '['
    for i in range(len(questions)):
        prompt = construct_prompt("", questions[i])
        # print(prompt)
        output_json += ask_perplexity(prompt) # ask_4o(prompt)
        print(output_json)
        print("========")
        if i != len(questions) - 1:
            output_json += ","
    output_json += ']'

    return json.loads(output_json), 200

@app.route('/', methods=['GET'])
def get_current_time():
    return "", 200

def main():
    app.run()

if __name__ == '__main__':
    main()
