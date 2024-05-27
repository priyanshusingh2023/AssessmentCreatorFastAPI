import httpx  # Used for making asynchronous HTTP requests
import json  # Used for JSON manipulation
from main.config import API_URL, API_KEY, GENERATION_CONFIG, SAFETY_SETTINGS  # Imports configuration settings
import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Jinja environment
env = Environment(
    loader=FileSystemLoader('templates'),  # Load templates from the 'templates' directory
    autoescape=select_autoescape(['html', 'xml', 'jinja'])  # Autoescape HTML, XML, and Jinja templates
)


def generate_prompt_assessment(assessment_data):
    """
    Generates a list of assessment prompts based on provided assessment data.

    Parameters:
    assessment_data (dict): A dictionary containing the keys 'role' and 'card'.
        Each 'card' should have 'keywords', 'tools', 'level', and 'noOfQuestions'.

    Returns:
    str: A formatted prompt for generating questions, optionally including tools and technologies.

    Raises:
    ValueError: If the required keys are missing in `assessment_data` or any of its 'cards'.
    """
    # Check if all required keys are present in assessment_data
    required_keys = ['role', 'card']
    if not all(key in assessment_data for key in required_keys):
        raise ValueError("Missing required assessment data")

    role = assessment_data['role']
    card = assessment_data['card']

    keywords = card.get('keywords')  # Get keywords from the card
    tools = card.get('tools', [])  # Get tools from the card (default to empty list if not present)
    level = card.get('level')  # Get level from the card
    no_of_questions = card.get('noOfQuestions')  # Get number of questions from the card

    # Check if any required field is missing
    if not (keywords and tools is not None and level and no_of_questions):
        raise ValueError("Missing required fields in one of the cards")

    # Check if number of questions is valid
    if int(no_of_questions) < 1:
        raise ValueError("Number of questions must be greater than 1")
    
    # Check if level is valid
    if level.lower() not in ['low', 'medium', 'high']:
        raise ValueError("Level must be 'low', 'medium', or 'high'")
    
    # Get the Jinja template for individual card
    template = env.get_template('individualCard.jinja')

    # Data to be passed into the template
    context = {
        'no_of_questions': no_of_questions,
        'level': level,
        'role': role,
        'keywords': keywords,
        'tools': tools
    }

    # Render the template with the context data
    prompt = template.render(context)

    return prompt


async def get_result(prompt):
    """
    Makes an asynchronous HTTP request to an external API to generate assessment content based on the provided prompt.

    Parameters:
    prompt (str): The prompt used to generate assessment content.

    Returns:
    str: The generated assessment content.

    Raises:
    Exception: If there is an error in getting a response from the external API.
    """
    # Get the Jinja template for prompt
    template = env.get_template('prompt_template.jinja')
    final_prompt = template.render(prompt=prompt)
    
    # Log the generation process
    logging.info("Generating assessment content.")
    
    # Construct API URL
    apiUrl = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

    # Construct request body
    request_body = {
        "contents": [{"parts": [{"text": final_prompt}]}],
        "generationConfig": GENERATION_CONFIG,
        "safetySettings": SAFETY_SETTINGS
    }

    headers = {"Content-Type": "application/json"}

    try:
        async with httpx.AsyncClient(timeout=1000.0) as client:
            response = await client.post(apiUrl, data=json.dumps(request_body), headers=headers)
            response.raise_for_status()

        answer = response.json().get("candidates")[0].get("content").get("parts")[0].get("text")
        logging.info("Received response from API.")
        logging.debug(f"Generated content: {answer}")
        return answer

    except httpx.RequestError as e:
        logging.error("Service Exception:", exc_info=True)
        raise Exception("Error in getting response from Gemini API")
