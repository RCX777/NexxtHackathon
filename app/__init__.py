import time
import os
from datetime import datetime
from flask import Flask, json
import requests
from requests.models import Response
from openai import OpenAI, AzureOpenAI
from litellm import completion, get_supported_openai_params
import json
import re
import concurrent.futures

reasons = []

app = Flask(__name__)

# requires AZURE_OPENAI_API_KEY env variable to be set
client_4o = AzureOpenAI(
    api_version="2024-08-01-preview",
    base_url="https://rbro-openai-hackatlon.openai.azure.com/openai/deployments/gpt-4o"
)

perp_api_key = os.environ['PERP_API_KEY']
perp_client = OpenAI(api_key=perp_api_key, base_url="https://api.perplexity.ai")
all_questions = []

def ask_perplexity(query : str, default_to_none : bool = True, temp : float = 0.1, top_p : float = 0.1) -> dict:
    response = completion(
        model="perplexity/llama-3.1-sonar-small-128k-online",
        messages=[
            {
                "role": "system",
                "content": "You are a highly knowledgeable language model specialized in retrieving precise and up-to-date information from the live web about companies and e-commerce websites. Your output should focus on providing accurate details that can be used to analyze the trustworthiness of these entities. Prioritize factual data, current standings, recent news, user reviews, and any other relevant information that can influence credibility assessments. Ensure the information is clear, detailed, and verifiable to assist in making informed trustworthiness evaluations."
            },
            {
                "role": "user",
                "content": query
            }
        ],
        api_key=perp_api_key,
        temp=temp,
        top_p=top_p
    ).json()['choices'][0]['message']['content']

    # legacy code
    # json = response.json()['choices'][0]['message']['content']
    # if json[0] == '`':
    #     json = json[8:-3]
    # else:
    #     json = '{' + json + '}'
    # json = json[::-1]
    # length = len(json)
    # for i in range(length):
    #     if json[i] == '"':
    #         json = json[:i] + json[i + 1:length]
    #         break
    # json = json[::-1]
    # length = len(json)
    # json = json[:length - 2] + '"' + json[length - 2:]

    # remove citations
    response = re.sub(r"\[\d\]", "", response)



    try:
        response = json.loads(response)
    except ValueError:
        if default_to_none:
            response = {"answer" : "none", "reason" : "none"}
        else:
            response = {"response" : response}

    return response

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
    return f""" Context: The website/company you will be asked about is called {name}.
    Task: Answer the following question, giving a simple yes/no answer, followed by a reason for the given answer.\
    Make sure your reason does not conflict with the given answer.\
    If you are not sure about your answer, just say "none".\
    Response format: {{ "answer" : "yes", "reason" : "..." }} for a valid answer or {{ "answer" : "none", "reason" : "none" }} if you're not sure.\
    Question: {question}"""

def ask_questions(questions, name, total_weight):
    score = 0
    responses = []

    for question in questions:
        prompt = construct_prompt(name, question['question'])
        response = ask_perplexity(prompt)

        # normalize weight based on question count
        weight = question['weight'] / total_weight

        if response["answer"] == "yes":
            score += weight
        elif response["answer"] == "no":
            score -= weight

        # copy question and weight in response, to be used for getting top most important reasons
        response['question'] = question['question']
        response['weight'] = weight

        responses.append(response)

    return responses, score

def get_reasons(responses, positive):
    filtered_responses = [res for res in responses if res['answer'] == ('yes' if positive else 'no')]
    sorted_responses = sorted(filtered_responses, key=lambda d: d['weight'], reverse=True)
    return sorted_responses

def get_top_reasons(responses, positive, count = 3):
    sorted_responses = get_reasons(responses, positive)
    return [res['reason'] for res in sorted_responses[:count]]

@app.route('/hal/<name>', methods=['GET'])
def hallucinate(name : str):
    question_count = len(all_questions)
    thread_count = 16

    total_weight = sum([question['weight'] for question in all_questions[:question_count]], 0)

    # total score will be between -1 and 1
    score = 0

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(ask_questions, all_questions[int(question_count / thread_count * i) : int(question_count / thread_count * (i + 1))], name, total_weight) for i in range(thread_count)]

        results = [f.result() for f in futures]

        responses = []

        # aggregate responses and partial scores
        for result in results:
            # filter invalid responses
            responses += [res for res in result[0] if res['answer'] != 'none' and res['reason'] != 'none']
            score += result[1]

    reasons[:] = responses
    return json.dumps({'score' : str(score), 'top reasons' : get_top_reasons(responses, score > 0.2)}), 200

from fpdf import FPDF
def json_to_pdf(data, pdf_path):
    # Convert JSON data to a pretty printed string
    json_str = "\t\t ===== Fraud report ===== \t\t\n"
    for row in data:
        json_str += f'Question: {row["question"]}\n'
        json_str += f'Answer:   {row["answer"]}\n'
        json_str += f'Reason:   {row["reason"]}\n'
        json_str += '=========================\n'
    print(json_str)

    # Create a PDF instance
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font("DejaVu", '', size=10)
    # Split the string into lines
    lines = json_str.split('\n')
    # Add each line to the PDF
    for line in lines:
        pdf.multi_cell(0, 10, line)
    # Save the PDF to the specified path
    pdf.output(pdf_path)

@app.route('/hal/<name>/extra', methods=['GET'])
def extra(name : str):
    json_to_pdf(reasons, f'data/{name}.pdf')
    return reasons

def load_questions():
    global all_questions

    with open('questions/questions.txt', 'r') as f:
        all_questions = json.loads(f.read())

def main():
    load_questions()

    # pilosaleltd.com -> ~0.08 score
    # morrity.com -> ~0.10 score
    # de pe Scammer website list pe google

    app.run()

if __name__ == '__main__':
    main()
