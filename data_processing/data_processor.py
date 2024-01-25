# data_processing/data_processor.py
from sklearn.preprocessing import StandardScaler, LabelEncoder

class DataProcessor:
    @staticmethod
    def process_data(df):
        df['combined_tags'] = df['tags'].apply(lambda x: ', '.join(x))
        df['input_text'] = df[['title', 'synonyms', 'combined_tags']].apply(lambda x: ' '.join(map(str, x)), axis=1)
        df['year'] = df['animeSeason'].apply(lambda x: x['year'] if 'year' in x else None)
        df = df.drop(['animeSeason', 'tags', 'relations', 'synonyms', 'thumbnail', 'input_text'], axis=1)
        df = df.dropna(subset=['year']).reset_index(drop=True)
        df['year'] = df['year'].astype(int)
        df['primary_source'] = df['sources'].apply(lambda x: x[0] if x else None)
        df = df.drop('sources', axis=1)
        link_columns = ['primary_source', 'picture']
        for column in link_columns:
            df[column] = df[column].apply(lambda x: x.split(',') if isinstance(x, str) else x)
        df['primary_source'] = df['primary_source'].apply(lambda x: [x] if isinstance(x, str) else x)
        df['episodes'] = df['episodes'].astype(object)
        label_encoder = LabelEncoder()
        df['type'] = label_encoder.fit_transform(df['type'])
        df['status'] = label_encoder.fit_transform(df['status'])

        df['combined_tags'] = df['combined_tags'].apply(lambda tags: [tag.lower() for tag in tags.split(',')])

        return df
