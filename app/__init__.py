import time
import os
from datetime import datetime
from flask import Flask, json
import requests
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
    url = "https://api.perplexity.ai/chat/completions"
    payload = {
        "model": "llama-3.1-sonar-large-128k-online",
        "messages": [
            {
                "role": "system",
                "content": "You are a highly knowledgeable language model specialized in retrieving precise and up-to-date information from the live web about companies and e-commerce websites. Your output should focus on providing accurate details that can be used to analyze the trustworthiness of these entities. Prioritize factual data, current standings, recent news, user reviews, and any other relevant information that can influence credibility assessments. Ensure the information is clear, detailed, and verifiable to assist in making informed trustworthiness evaluations."
            },
            {
                "role": "user",
                "content": query
            }
        ],
        # "max_tokens": 4096,
        "temperature": temp,
        "top_p": top_p,
        "search_domain_filter": ["perplexity.ai"],
        "return_images": False,
        "return_related_questions": False,
        "search_recency_filter": "month",
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1
    }
    headers = {
        "Authorization": f"Bearer {perp_api_key}",
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    json = response.json()['choices'][0]['message']['content']
    if json[0] == '`':
        json = json[8:-3]
    else:
        json = '{' + json + '}'
    json = json[::-1]
    length = len(json)
    for i in range(length):
        if json[i] == '"':
            json = json[:i] + json[i + 1:length]
            break
    json = json[::-1]
    length = len(json)
    json = json[:length - 2] + '"' + json[length - 2:]

    return json

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


def construct_prompt(name: str, question : str):
    return f""" INFORMATION: The website/company is called {name}
    INSTRUCTION: Using the given information, answer to the following question, which is delimited by "=====" Answer with a json object containing the "answer" field which is boolean true/false, and "reason" field which is the reason for the given answer. Only output valid JSON. Do not use any extra syntax or characters. Make sure you do not forget the brackets. Make sure the last quotation mark is right behind the last bracket. Write the JSON after the "CUE:".
    EXAMPLE OUTPUT FORMAT:
{{"answer": true, "reason": "text"}}
    =====
    {question}
    =====
    CUE:
    """

@app.route('/hal/<name>', methods=['GET'])
def hallucinate(name : str):
    with open('questions.txt', 'r') as f:
        questions = f.read().splitlines()

    # question_count = len(questions)
    question_count = 10

    output_json = '['
    for i in range(question_count):
        prompt = construct_prompt(name, questions[i])
        result = ask_perplexity(prompt)
        print(result)
        print('=======')
        output_json += result
        if i != question_count - 1:
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
