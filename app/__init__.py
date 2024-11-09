import time
import os
from datetime import datetime
from flask import Flask
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

def ask_perplexity(query : str):
    result = client_perp.search(
        query=query,
        date_context=datetime.today().strftime('%Y-%m-%d'),
        location="ro",
        pro_mode=False,
        response_language="en",
        answer_type="text",
        verbose_mode=False,
        search_type="general",
        return_citations=False,
        return_sources=False,
        return_images=False
    )

    return result['llm_response']

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

    return {"response" : completion.choices[0].message.content}

@app.route('/hal/<name>', methods=['GET'])
def hallucinate(name : str):
    query = f"""Please provide me the following information about {name}: Key Facts, Services and Features,
        Notable Innovations and Initiatives, Subsidiaries and Partnerships, Reputation and Trustworthiness and Challenges."""

    return {"response" : ask_perplexity(query)}

@app.route('/', methods=['GET'])
def get_current_time():
    return "", 200
