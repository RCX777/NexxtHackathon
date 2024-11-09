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

@app.route('/hal/<name>', methods=['GET'])
def hallucinate(name : str):
    query = f"""Please provide me the following information about {name}: Key Facts, Services and Features,
        Notable Innovations and Initiatives, Subsidiaries and Partnerships, Reputation and Trustworthiness and Challenges.        Keep the information concise and relevant."""
    response = ask_perplexity(query)

    question = f"Is there any recent controversy regarding {name}?"

    prompt = f"""\
        INSTRUCTION: Please use only the following information:
        {response}
        INSTRUCTION: Using the given information, answer to the following question.\
        Answer with a json object containing the "answer" field which is boolean true/false,
        and "reason" field which is the reason for the given answer. Only output valid JSON.
        Write the JSON after the "CUE:".
        {question}
        CUE:
    """
    print(prompt)

    return ask_4o(prompt), 200

@app.route('/', methods=['GET'])
def get_current_time():
    return "", 200

def main():
    app.run()

if __name__ == '__main__':
    main()
