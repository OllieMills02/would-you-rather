import json
import os

from dotenv import load_dotenv
from sklearn.model_selection import train_test_split

def split_data_source(filename: str):
    load_dotenv()
    os_path = os.environ["OUTPUT_DIR"]

    with open(os.path.join(os_path,filename), 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Split the data into training and validation sets (80/20 split)
    train_data, val_data = train_test_split(data, test_size=0.2, random_state=42)

    # Save the split data to new files
    with open(os.path.join(os_path,'train_data.json'), 'w', encoding='utf-8') as f:
        json.dump(train_data, f, indent=2)

    with open(os.path.join(os_path,'val_data.json'), 'w', encoding='utf-8') as f:
        json.dump(val_data, f, indent=2)

    print(f"Training set size: {len(train_data)}")
    print(f"Validation set size: {len(val_data)}")