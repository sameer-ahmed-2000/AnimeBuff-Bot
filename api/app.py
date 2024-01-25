# app.py
from flask import Flask, request, jsonify
from data_processing.data_loader import DataLoader
from data_processing.data_processor import DataProcessor
from data_processing.text_preprocessor import TextPreprocessor
from chatbot.chatbot import Chatbot
from recommenders.anime_recommender import AnimeRecommenderWithDetails
from recommenders.tag_based_recommender import TagBasedRecommenderWithDetails

app = Flask(__name__)

# Load data
data_loader = DataLoader()
df = data_loader.load_data("C:/Users/samee/Videos/Project/AnimeBuff-Bot/data/anime-offline-database.json")

# Process data
data_processor = DataProcessor()
df = data_processor.process_data(df)

# Preprocess text
text_preprocessor = TextPreprocessor()
text_preprocessor.preprocess_text(df)

# Initialize components
chatbot = Chatbot(df)
anime_recommender = AnimeRecommenderWithDetails(df, chatbot)
tag_based_recommender = TagBasedRecommenderWithDetails(df, chatbot)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['user_input']
    response = chatbot.chat(user_input)
    return jsonify({'response': response})

@app.route('/recommend/anime', methods=['POST'])
def recommend_anime():
    anime_title = request.json['anime_title']
    recommendations = anime_recommender.recommend_anime(anime_title)
    return jsonify({'recommendations': recommendations})

@app.route('/recommend/tags', methods=['POST'])
def recommend_tags():
    input_tags = request.json['input_tags']
    recommendations = tag_based_recommender.recommend_by_tags(input_tags)
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)
