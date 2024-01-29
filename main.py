from data_processing.data_loader import DataLoader
from data_processing.data_processor import DataProcessor
from data_processing.text_preprocessor import TextPreprocessor
from chatbot.chatbot import Chatbot
from recommenders.anime_recommender import AnimeRecommenderWithDetails

from recommenders.tag_based_recommender import TagBasedRecommenderWithDetails
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

while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break

    # Get chatbot response from your dataset
    chatbot_response = tag_based_recommender.recommend_by_tags(user_input)
    
    print("Chatbot:", chatbot_response)

while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break

    # Get chatbot response from your dataset
    chatbot_response = anime_recommender(user_input)
    
    print("Chatbot:", chatbot_response)