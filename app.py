from flask import Flask, render_template, request, jsonify
from data_processing.data_loader import DataLoader
from data_processing.data_processor import DataProcessor
from data_processing.text_preprocessor import TextPreprocessor
from chatbot.chatbot import Chatbot
from recommenders.anime_recommender import AnimeRecommenderWithDetails
from recommenders.tag_based_recommender import TagBasedRecommenderWithDetails
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

# Define routes for website pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['GET','POST'])
def chat():
    return render_template('chat.html')

@app.route('/recommend/anime', methods=['GET','POST'])
def recommend_anime():
    return render_template('recommend_anime.html')

@app.route('/recommend/tags', methods=['GET','POST'])
def recommend_tags():
    return render_template('recommend_tags.html')

# Define routes for API endpoints

@app.route('/api/chat', methods=['GET','POST'])
def api_chat():
    user_input = request.json.get('user_input')  # Use get method to handle potential missing key
    print("Received user input:", user_input)  # Add this line for debugging
    response = chatbot.chat(user_input)
    print("Generated response:", response)  # Add this line for debugging
    return jsonify({'response': response})

@app.route('/api/recommend/anime', methods=['GET','POST'])
def api_recommend_anime():
    anime_title = request.json['anime_title']
    recommendations = anime_recommender.recommend_anime(anime_title)
    return jsonify({'recommendations': recommendations})

@app.route('/api/recommend/tags', methods=['GET','POST'])
def api_recommend_tags():
    input_tags = request.json['input_tags']
    recommendations = tag_based_recommender.recommend_by_tags(input_tags)
    return jsonify({'recommendations': recommendations})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
