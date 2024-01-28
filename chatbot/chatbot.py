from sklearn.preprocessing import StandardScaler, LabelEncoder
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

class Chatbot:
    def __init__(self, dataset):
        self.gpt_model = GPT2LMHeadModel.from_pretrained("gpt2")
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.dataset = dataset
        self.status_mapping = {0: 'FINISHED', 1: 'ONGOING', 2: 'UNKNOWN', 3: 'UPCOMING'}
        self.type_mapping = {0: 'ONA', 1: 'OVA', 2: 'SPECIAL', 3: 'TV', 4: 'UNKNOWN'}
        self.scaler = StandardScaler()
        self.scaler.fit(dataset[['episodes']])

    def encode_input(self, user_input):
        input_ids = self.tokenizer.encode(user_input, return_tensors="pt")
        attention_mask = torch.ones_like(input_ids)
        return input_ids, attention_mask

    def generate_response_from_data(self, user_input):
        result = self.dataset[self.dataset['title'].str.lower() == user_input.lower()]

        if not result.empty:
            title = result['title'].values[0]
            anime_type_encoded = result['type'].values[0]
            episodes = str(result['episodes'].values[0])
            status_encoded = result['status'].values[0]
            picture = result['picture'].values[0]
            year = result['year'].values[0]
            primary_source = result['primary_source'].values[0]

            anime_type = self.type_mapping.get(anime_type_encoded, 'UNKNOWN')
            status = self.status_mapping.get(status_encoded, 'UNKNOWN')

            response = f"\nDetails for {title}:\nTitle: {title} \nType: {anime_type} \nEpisodes: {episodes} \nStatus: {status} \nPicture: {picture} \nYear: {year} \nPrimary Source: {primary_source}"
        else:
            response = "Sorry, I couldn't find information for that title."

        return response

    def chat(self, user_input):
        input_ids, attention_mask = self.encode_input(user_input)
        response = self.generate_response_from_data(user_input)
        return response
