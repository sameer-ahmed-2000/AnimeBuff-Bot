class TextPreprocessor:
    @staticmethod
    def preprocess_text(df):
        df['title'] = df['title'].str.lower().str.replace('[^\w\s]', '').str.strip()
