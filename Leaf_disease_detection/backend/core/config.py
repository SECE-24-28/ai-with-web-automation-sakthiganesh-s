from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR /'backend'/'models' / 'best_model.h5'
DATA_PATH = BASE_DIR /'backend'/'data' / 'disease_info.json'
