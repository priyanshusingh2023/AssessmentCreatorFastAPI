from main.utilities import get_result, generate_prompt_assessment  # Imports necessary functions from utilities module
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def generate_assessment(assessment_data):
    """
    Generates an assessment based on provided data by creating specific prompts and using an API to generate content.

    This function orchestrates the generation of assessment questions by first formatting prompts based on input
    data about the assessment, and then using these prompts to generate actual assessment content via an external API.

    Parameters:
    assessment_data (dict): A dictionary containing all necessary data to generate assessment prompts. The structure
        and required keys are dictated by the `generate_prompt_assessment` function.

    Returns:
    str: A string containing all the generated assessment questions, concatenated together.

    Raises:
    ValueError: If `assessment_data` is not a dictionary or is empty, indicating invalid or insufficient input data.
    """
    # Validate input data
    if not isinstance(assessment_data, dict) or not assessment_data:
        raise ValueError("Invalid assessment data provided")

    role = assessment_data.get('role')
    cards = assessment_data.get('cards', [])
    if not role or not cards:
        raise ValueError("Missing role or cards in assessment data")

    result = ""  # Initialize a variable to store all generated content

    for card in cards:
        print(card)
        # Ensure each card has the necessary fields
        keywords = card.get('keywords')
        tools = card.get('tools')
        level = card.get('level')
        no_of_questions = card.get('noOfQuestions')

        if not (keywords and tools is not None and level and no_of_questions):
            raise ValueError("Missing required fields in one of the cards")

        # Generate a prompt from the card data
        prompt_data = {
            'role': role,
            'card': card
        }

        # Generate the prompt using the helper function
        prompt = generate_prompt_assessment(prompt_data)
        # Generate assessment content for the prompt using an external API
        if len(cards) > 1:
                time.sleep(0.01)
        res = await get_result(prompt)
        result += res + "\n\n"  # Concatenate the results into a single string

    return result  # Return the final concatenated result
