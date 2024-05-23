import httpx  # Used for making asynchronous HTTP requests
import json  # Used for JSON manipulation
from main.config import API_URL, API_KEY, GENERATION_CONFIG, SAFETY_SETTINGS  # Imports configuration settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_prompt_assessment(assessment_data):
    """
    Generates a list of assessment prompts based on provided assessment data.

    Parameters:
    assessment_data (dict): A dictionary containing the keys 'role' and 'cards'.
        Each 'card' should have 'keywords', 'tools', 'level', and 'noOfQuestions'.

    Returns:
    str: A formatted prompt for generating questions, optionally including tools and technologies.

    Raises:
    ValueError: If the required keys are missing in `assessment_data` or any of its 'cards'.
    """
    required_keys = ['role', 'card']
    if not all(key in assessment_data for key in required_keys):
        raise ValueError("Missing required assessment data")

    role = assessment_data['role']
    card = assessment_data['card']

    keywords = card.get('keywords')
    tools = card.get('tools', [])
    level = card.get('level')
    no_of_questions = card.get('noOfQuestions')

    if not (keywords and tools is not None and level and no_of_questions):
        raise ValueError("Missing required fields in one of the cards")

    if int(no_of_questions) < 1:
        raise ValueError("Number of questions must be greater than 1")

    if level.lower() not in ['low', 'medium', 'high']:
        raise ValueError("Level must be 'low', 'medium', or 'high'")

    tools_str = f" using {', '.join(tools)}" if tools else ""
    # Create the prompt
    prompt = f"I want {no_of_questions} assessment questions of {level} complexity for {role} on {', '.join(keywords)}{tools_str}."

    logging.debug(f"Generated prompt: {prompt}")

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

     # Predefined prompt for setting the context of generated content
    final_prompt = ("I am creating an assessment with the following specifications. "
                    "Low complexity should be Blooms level 1 and 2 that test recall and comprehension. "
                    "Medium complexity should be Blooms level 3 of type application. "
                    "High complexity should be Blooms level 4 of type analysis, preferably scenario-based. "
                    f"\n{prompt}")

    logging.debug(f"Final prompt: {final_prompt}")

    example_format = (
            "MCQ strictly has to be in below format:\n"
            "Format:\n **Question 1 question**\n"
            "A. Option 1\n"
            "B. Option 2\n"
            "C. Option 3\n"
            "D. Option 4\n"
            "\n**Answer: Option no. Answer**\n"
            "MCQ Format Example:\n"
            "**Question 10**\n"
            "What is the purpose of the following code?\n"
            "```c\n"
            "int arr[] = {1, 2, 3, 4, 5};\n"
            "int sum, product;\n"
            "sum = product = 1;\n"
            "for (int i = 0; i < 5; i++) {\n"
            "  sum += arr[i];\n"
            "  product *= arr[i];\n"
            "}\n"
            "```\n"
            "A. To calculate the sum and product of all elements in the array\n"
            "B. To calculate the average and standard deviation of all elements in the array\n"
            "C. To reverse the order of elements in the array\n"
            "D. To sort the elements in the array\n"
            "\n**Answer: A. To calculate the sum and product of all elements in the array**\n"
            "No need to separate questions topic-wise and mention the topic and Write complete answer don't change the example format, all MCQ questions should be in given format"
        )
    
    logging.info("Generating assessment content.")
    apiUrl = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"



    request_body = {
        "contents": [{"parts": [{"text": prompt + example_format}]}],
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
