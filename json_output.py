import csv
import json
import os
import re

from dotenv import load_dotenv


def format_would_you_rather_strings(titles: list[str], csv_title: str) -> list[tuple[str,str]] | None:
    """
    Formats a list of "Would You Rather" titles into a CSV file.
    Each row contains a list of two options.
    """
    load_dotenv()
    output_dir = os.environ.get("OUTPUT_DIR")

    if not output_dir:
        print("Error: OUTPUT_DIR environment variable is not set.")
        return None

    # Construct the full path to the output file
    output_path = os.path.join(output_dir, csv_title)
    if not output_path.endswith('.json'):
        output_path += '.json'

    unique_questions = []
    seen_questions = set()

    for title in titles:
        original_title = title.strip()
        lower_title = original_title.lower()

        wyr_pattern = r'^(?:(\d+\.\s+))?(wyr|would you rather|would you rather:|wyr:)\s+(.*)\s+or\s+(.*)'
        match = re.search(wyr_pattern, lower_title, re.IGNORECASE)

        if match:
            option1 = match.group(3).strip()
            option2 = match.group(4).strip()

            option1 = re.sub(r'\s+', ' ', option1)
            option2 = re.sub(r'\s+', ' ', option2)

            option1 = re.sub(r'[?.!]$', '', option1)
            option2 = re.sub(r'[?.!]$', '', option2)

            question_tuple = (option1, option2)

            if question_tuple not in seen_questions:
                # Build the prompt and completion for AI training

                # Create a dictionary for the JSON output
                question_dict = {
                    "text": f"Would you rather {option1} or {option2}?",
                }

                unique_questions.append(question_dict)
                seen_questions.add(question_tuple)

        # Write the list of dictionaries to a JSON file
        with open(output_path, mode='w', encoding='utf-8') as json_file:
            json.dump(unique_questions, json_file, indent=4)


    return unique_questions