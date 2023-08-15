import os
import torch
import datasets
from InstructorEmbedding import INSTRUCTOR
import json

def initialize_koko():
    torch.set_grad_enabled(False)

    # Check if config.json exists, if not, create it
    BASE_DIR = os.path.dirname(__file__)
    
    config_path = os.path.join(BASE_DIR, 'config.json')
    if not os.path.exists(config_path):
        default_config = {
            "column": "embedding",
            "prompt": "Represent the Stackoverflow question for retrieving corresponding codes: ",
            "model_path": "bin/model.bin",
            "dataset_path": "bin/dataset.bin",
            "faiss_path": "bin/faiss.bin"
        }

        with open(config_path, 'w') as f:
            json.dump(default_config, f)

    # Load the config file
    with open(config_path, 'r') as f:
        CONFIG = json.load(f)

    COLUMN = CONFIG['column']
    MODEL_PATH = os.path.join(BASE_DIR, CONFIG['model_path'])
    DATASET_PATH = os.path.join(BASE_DIR, CONFIG['dataset_path'])
    FAISS_PATH = os.path.join(BASE_DIR, CONFIG['faiss_path'])

    # Check if setup has already been done
    if not (os.path.exists(MODEL_PATH) and os.path.exists(DATASET_PATH) and os.path.exists(FAISS_PATH)):
        bin_dir = os.path.join(BASE_DIR, "bin")
        os.makedirs(bin_dir, exist_ok=True)
        
        # Initialize the sentence transformer model
        model = INSTRUCTOR('hkunlp/instructor-large')
        torch.save(model, MODEL_PATH)

        # Load the huggingface dataset with the API descriptions and embeddings
        ds = datasets.load_dataset('Maurus/APIBench')['train']
        ds.save_to_disk(DATASET_PATH)

        # Create FAISS index
        ds.add_faiss_index(COLUMN)
        ds.save_faiss_index(COLUMN, file=FAISS_PATH)

    print("Initialization complete. Datasets and models downloaded.")

if __name__ == "__main__":
    initialize_koko()