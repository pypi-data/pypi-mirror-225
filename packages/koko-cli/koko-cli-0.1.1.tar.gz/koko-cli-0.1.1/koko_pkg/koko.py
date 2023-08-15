
import os
import torch
import datasets
import questionary
import argparse
import json

torch.set_grad_enabled(False)

# Load the config file
BASE_DIR = os.path.dirname(__file__)

# Load the config file
with open(os.path.join(BASE_DIR, 'config.json'), 'r') as f:
    CONFIG = json.load(f)

# Variables from config
PROMPT = CONFIG['prompt']
COLUMN = CONFIG['column']
MODEL_PATH = os.path.join(BASE_DIR, CONFIG['model_path'])
DATASET_PATH = os.path.join(BASE_DIR, CONFIG['dataset_path'])
FAISS_PATH = os.path.join(BASE_DIR, CONFIG['faiss_path'])

# Load model and dataset
model = torch.load(MODEL_PATH)
ds = datasets.load_from_disk(DATASET_PATH)
ds.load_faiss_index(COLUMN, file=FAISS_PATH)

def suggest_commands(user_input):
    question_embedding = model.encode([[PROMPT, user_input]])
    
    results = []
    k = 20  # Initial number of results to fetch
    
    while len(results) < 5:
        scores, retrieved = ds.get_nearest_examples(COLUMN, question_embedding, k=k)
        
        for api_name, domain, description, code in zip(retrieved['api_name'], retrieved['domain'], retrieved['description'], retrieved['code']):
            if len(results) < 3 and api_name not in [res['api_name'] for res in results]:
                results.append({'api_name': api_name, 'domain': domain, 'description': description, 'code': code})
            elif len(results) >= 3 and domain not in [res['domain'] for res in results] and api_name not in [res['api_name'] for res in results]:
                results.append({'api_name': api_name, 'domain': domain, 'description': description, 'code': code})
            if len(results) == 5:
                break
        
        k += 10

    list_choices = [f"{res['domain']} ({res['api_name']})\n    - {res['description'][:100]}..." for res in results]
    choice = questionary.select("", choices=list_choices).ask()
    
    selected_data = results[list_choices.index(choice)]
    chosen = selected_data['description'] + '\n\n' + selected_data['code']
    return chosen

def main():
    parser = argparse.ArgumentParser(description='koko CLI')
    parser.add_argument('user_input', type=str, nargs='+', help='User input')  # The nargs='+' allows for multiple words to be captured as a list

    args = parser.parse_args()

    sentence = ' '.join(args.user_input)  # Join the list of words to form the sentence
    chosen = suggest_commands(sentence)
    questionary.print(chosen)