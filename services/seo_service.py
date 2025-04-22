from groq import Groq
from dotenv import load_dotenv
import config
import json
import re

load_dotenv()

def get_company_info(company_name: str, location: str, api_key: str):
    """Fetches company details using Groq AI."""
    client = Groq(api_key=api_key)

    # Create a structured prompt for the AI model
    prompt = f"""    
    Company: {company_name}
    Location: {location}
    
    Provide the following details:
    1. Official Name
    2. Industry Type
    3. Headquarters / Main Office Location
    4. Key Products / Services
    5. Website (if available)
    
    Write the 3 competitiors based on the same location, sector and services

    Strictly always return response in JSON format as shown in example
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

    # Extract response
    return completion.choices[0].message.content

def get_seo_info(company_info: str, api_key: str):
    """Fetches company details using Groq AI."""
    client = Groq(api_key=api_key)

    # Create a structured prompt for the AI model
    prompt = f"""
    From the {company_info} the companies.

    Provide the following details for only the given company in input:
    1. 10 SEO Keywords    
    Only give the the company name and SEO keywords
    Strictly always return response in JSON format as shown in example. 
    Compulsarily find all the details for all the companies
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

    # Extract response
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

def get_seo(company_description: str, location: str):
    company_info = get_company_info(company_description, location, api_key=config.GROQ_API_KEY)
    return get_seo_info(str(company_info), api_key=config.GROQ_API_KEY)
