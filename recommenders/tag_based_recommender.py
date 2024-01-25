# recommenders/tag_based_recommender.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from difflib import SequenceMatcher

class TagBasedRecommenderWithDetails:
    def __init__(self, dataset, chatbot):
        self.dataset = dataset
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tag_matrix = self.vectorizer.fit_transform(dataset['combined_tags'].apply(lambda tags: ' '.join(tags)))
        self.chatbot = chatbot

    def recommend_by_tags(self, input_tags, num_recommendations=5):
        expanded_tags = self.expand_tags(input_tags)
        input_vector = self.vectorizer.transform([' '.join(expanded_tags)])
        cosine_similarities = linear_kernel(input_vector, self.tag_matrix).flatten()
        similar_anime_indices = cosine_similarities.argsort()[:-num_recommendations-1:-1]

        recommendations = []
        for i in similar_anime_indices:
            anime_details = self.dataset.iloc[i]
            title = anime_details['title']
            recommendation_details = self.chatbot.generate_response_from_data(title)
            recommendations.append({
                'title': title,
                'details': recommendation_details
            })

        return recommendations[:num_recommendations]

    def expand_tags(self, input_tags):
        expanded_tags = set(input_tags)
        for tag in input_tags:
            similar_tags = self.find_similar_tags(tag)
            expanded_tags.update(similar_tags)
        return list(expanded_tags)

    def find_similar_tags(self, input_tag):
        similar_tags = []
        for tag in self.vectorizer.get_feature_names():
            similarity = SequenceMatcher(None, input_tag, tag).ratio()
            if similarity > 0.6:
                similar_tags.append(tag)
        return similar_tags
