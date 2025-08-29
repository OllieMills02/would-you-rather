import csv
import os
import re

from dotenv import load_dotenv


def format_would_you_rather_strings(titles: list[str], csv_title: str) -> list[tuple[str,str]] | None:
    """
    Formats a list of "Would You Rather" titles into a CSV file.
    Each row contains a list of two options.
    """
    load_dotenv()
    output_dir = os.environ.get("CSV_OUTPUT_DIR")

    if not output_dir:
        print("Error: CSV_OUTPUT_DIR environment variable is not set.")
        return None

    # Construct the full path to the output file
    output_path = os.path.join(output_dir, csv_title)

    unique_questions = []
    seen_questions = set()

    for title in titles:
        original_title = title.strip()
        lower_title = original_title.lower()

        wyr_pattern = r'^(wyr|would you rather|would you rather:|wyr:)\s+(.*)\s+or\s+(.*)'
        match = re.search(wyr_pattern, lower_title, re.IGNORECASE)

        if match:
            option1 = match.group(2).strip()
            option2 = match.group(3).strip()

            option1 = re.sub(r'\s+', ' ', option1)
            option2 = re.sub(r'\s+', ' ', option2)

            option1 = re.sub(r'[?.!]$', '', option1)
            option2 = re.sub(r'[?.!]$', '', option2)

            question_tuple = (option1, option2)

            if question_tuple not in seen_questions:
                unique_questions.append(question_tuple)
                seen_questions.add(question_tuple)



    with open(output_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(unique_questions)


    return unique_questions