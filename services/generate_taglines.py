from groq import Groq
from dotenv import load_dotenv
import config
import json
import re
load_dotenv()

def get_company_info(company_description: str, company_sector: str, api_key: str):
    """Fetches company details using Groq AI."""
    client = Groq(api_key=api_key)

    # Create a structured prompt for the AI model
    prompt = f"""
    You are a specialized naming consultant for businesses. Create exactly 5 unique and memorable company names based on the following:

    INPUTS NEEDED:
    1. Company description: {company_description}
    2. Industry/sector: {company_sector}

    REQUIREMENTS:
    - Generate exactly 5 names
    - Each name should be maximum 2-3 words
    - Include a brief rationale (max 15 words) explaining each name
    - Names should be:
    * Memorable and distinct
    * Available as .com domains
    * Easy to pronounce
    * Reflective of company values
    * Relevant to industry

    ### Instructions:
    - Ensure the JSON response is well-formed and strictly follows valid JSON syntax.
    - **Do not include unbalanced curly braces `{{}}` inside any key or value.**
    - **Do not wrap JSON in triple backticks (` ``` `).**
    - If any data is unavailable, return "Not Available" instead of leaving fields empty.
    - Strictly always return response in JSON format as shown in example.

    OUTPUT FORMAT:
    Return response strictly in this JSON format:

    """
    prompt += """
    EXAMPLE:
    INPUT:
    {
    "company_description": "We are company selling competition analysis and AI-a-a-s company",
    "company_sector": "Artificial Intelligence"
    }

    OUTPUT:
    {
    "company_names": [
            {
                "name": "AIAlyze",
                "TagLine": "Analyzing AI with precision"
            },
            {
                "name": "Intellex",
                "TagLine": "Intelligent analysis solutions"
            },
            {
                "name": "CompeteAI",
                "TagLine": "Competitive edge through AI"
            },
            {
                "name": "PulseAI",
                "TagLine": "Pulsing with AI insights"
            },
            {
                "name": "Cerebro",
                "TagLine": "Brainpower for business"
            }
        ]
    }
    """

    # Call Groq API
    completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts structured company information."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        max_tokens=500
    )
    response_content = str(completion.choices[0].message.content).strip()
    
    if not response_content:
        raise ValueError("Empty response received from Groq AI.")

    # Remove code block formatting if present
    cleaned_json = re.sub(r"```json|```", "", response_content).strip()

    try:
        print(cleaned_json)
        return json.loads(cleaned_json)  # Convert to Python dictionary
    except json.JSONDecodeError as e:
        print("Invalid JSON Response:", response_content)
        raise ValueError("Failed to parse response as JSON.") from e