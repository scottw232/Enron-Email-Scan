import pandas as pd
import json
import os
import glob
import string as st

    
if __name__ == '__main__':

    sent_df = pd.read_csv('./dataset/post_sentiment.csv')
    racist_df = pd.read_csv('racist_terms_abbr.csv')
    racist_list = racist_df.iloc[:, 0].to_list()
    pattern = '|'.join(racist_list)
    full_racist_email_df = sent_df[sent_df.apply(lambda row: row.astype(str).str.contains(pattern, case=False).any(), axis=1)]
    full_racist_email_df.to_csv('./temp_data/racist_scan.csv')
