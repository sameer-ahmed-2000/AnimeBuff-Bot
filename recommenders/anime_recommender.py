from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class AnimeRecommenderWithDetails:
    def __init__(self, dataset, chatbot):
        self.dataset = dataset
        self.chatbot = chatbot
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tag_matrix = self.vectorizer.fit_transform(dataset['combined_tags'].apply(lambda tags: ' '.join(tags)))

    def recommend_anime(self, anime_title, num_recommendations=5):
        anime_index = self.dataset[self.dataset['title'].str.lower() == anime_title.lower()].index
        if not anime_index.empty:
            anime_index = anime_index[0]
            cosine_similarities = linear_kernel(self.tag_matrix[anime_index], self.tag_matrix).flatten()
            similar_anime_indices = cosine_similarities.argsort()[:-num_recommendations-1:-1]

            recommendations = []
            for i in similar_anime_indices:
                anime_title = self.dataset.iloc[i]['title']
                anime_details = self.chatbot.generate_response_from_data(anime_title)
                recommendations.append({
                    'title': anime_title,
                    'details': anime_details
                })

            return recommendations
        else:
            return None

