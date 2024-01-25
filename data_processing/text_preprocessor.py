# data_processing/text_preprocessor.py

class TextPreprocessor:
    @staticmethod
    def preprocess_text(df):
        df['title'] = df['title'].str.lower().str.replace('[^\w\s]', '').str.strip()
