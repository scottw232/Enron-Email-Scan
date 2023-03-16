import pandas as pd
import json
import os
import glob
import string as st

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Based on Piazza post @317
def import_data():
    path = './dataset'
    glob_target = os.path.join(path,'*.json')
    file_list = glob.glob(glob_target)

    file_count = 0
    json_email_df_list = []
    for file in file_list:
        if file_count == 10: break
        with open(file) as f:
            json_data = pd.json_normalize(json.loads(f.read()))
            file_name = file.split('/')[2].split('.')[0]
            json_data['filename'] = file_name
            json_email_df_list.append(json_data)
    df = pd.concat(json_email_df_list, sort=False)
    df.reset_index(inplace=True)
    
    return df

# based on https://www.analyticsvidhya.com/blog/2021/06/sentiment-analysis-using-nltk-a-practical-approach/
def punc_clean(text):
    a=[w for w in text if w not in st.punctuation]
    return ''.join(a)

# based on https://www.analyticsvidhya.com/blog/2021/06/sentiment-analysis-using-nltk-a-practical-approach/
def remove_stopword(text):
    stopword=nltk.corpus.stopwords.words('english')
    stopword.remove('not')
    a=[w for w in nltk.word_tokenize(text) if w not in stopword]
    return ' '.join(a)

# based on https://www.analyticsvidhya.com/blog/2021/06/sentiment-analysis-using-nltk-a-practical-approach/
def preprocess_text(df):
    df['sentiment_text'] =  df['text'].copy()
    df['sentiment_text'] = df['sentiment_text'].apply(punc_clean)
    df['sentiment_text'] = df['sentiment_text'].apply(remove_stopword)

    
def get_polarity_score(row):
    return sia.polarity_scores(row)
    
if __name__ == '__main__':
    full_df = import_data()
    nltk.download('vader_lexicon')
    sia = SentimentIntensityAnalyzer()
    
#     smaller_df = full_df.head(100)
#     preprocess_text(smaller_df)
#     smaller_df['sia_polarity_score'] = smaller_df['sentiment_text'].apply(get_polarity_score)
#     smaller_df.to_csv('post_sentiment.csv')

    preprocess_text(full_df)
    full_df['sia_polarity_score'] = full_df['sentiment_text'].apply(get_polarity_score)
    full_df.to_csv('./temp_data/post_sentiment.csv')
        