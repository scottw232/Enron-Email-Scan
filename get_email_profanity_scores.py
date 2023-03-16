## USAGE ##
# py get_email_profanity_score.py [email directoyr] [csv filename] [graph filename] [threshold]
# 0 < threshold < 1

## EXAMPLE ##
# py get_email_profanity_score.py dataset enron_profanity_scores.csv enrong_profanity_scores.graph 0.80


import csv
import json
import os
import sys
import networkx as nx
import profanity_check
# https://pypi.org/project/alt-profanity-check/

   
def isForwardOrReply(emailJson):
    if 'subject' not in emailJson: return False
    prefix = emailJson['subject'][:3].upper()
    return prefix == 'FW:' or prefix == 'RE:'


def getRowFromEmail(email, id, threshold):
    with open(email, 'r') as file:
        emailJson = json.load(file)
        
        if isForwardOrReply(emailJson):return []       
        if 'from' not in emailJson or 'to' not in emailJson: return []
        
        sender = emailJson['from'][0]['address']
        recipients = [person['address'] for person in emailJson['to']]
        date = emailJson['date'] if 'date' in emailJson else None
        text = emailJson['text'] if 'text' in emailJson else ''
        score = profanity_check.predict_prob([text])[0]
        
        if score < threshold: return []
        
        return [id, sender, recipients, date, score]
        

if __name__ == '__main__':
    emailsPath = sys.argv[1]
    csvOutFile = sys.argv[2]
    graphOutFile = sys.argv[3]
    threshold = float(sys.argv[4])
    
    print(f'Getting email profanity scores (>={threshold})...')
    
    G = nx.DiGraph()
    
    with open(csvOutFile, 'w+', newline='') as csvFile:
        allRows = []
        writer = csv.writer(csvFile, delimiter=',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        writer.writerow(['Email ID', 'Sender', 'Recipient', 'Date', 'Profanity Score'])
        for file in os.listdir(emailsPath):
            print(file)
            row = getRowFromEmail(os.path.join(emailsPath, file), os.path.splitext(file)[0], threshold)
            if row:
                allRows.append(row)
                for rpt in row[2]:
                    G.add_edge(row[1], rpt, weight = row[-1])
        
        print(f'Writing to {csvOutFile}...')
        allRows.sort(key = lambda r: -r[-1])
        for r in allRows:
            writer.writerow(r)
        print(f'{len(allRows)} total emails.')
            
#     print(f'Building graph {graphOutFile}...')
#     nx.write_adjlist(G, graphOutFile)
#     print(G)
            
    print('Done.')
        