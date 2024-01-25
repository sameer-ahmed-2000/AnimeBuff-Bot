import json
import os 
import pandas as pd

class DataLoader:
    @staticmethod
    def load_data(file_path='data/anime-offline-database.json'): 
        file_path = os.path.join(os.path.dirname(__file__), file_path)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            anime_data = json.load(file)
        return pd.DataFrame(anime_data['data'])

