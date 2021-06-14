import os
import re
from tqdm import tqdm
import nltk
tokenizer = nltk.data.load('russian.pickle')
import copy
import pandas as pd

DATA_PATH = '/Users/alexanderbaranof/Documents/r-final-project/Data/'

files = os.listdir(DATA_PATH)

result_files = list()
for file in files:
    if '.txt' in file:
        result_files.append(file)

files = result_files

MAX_POSSIBLE_INDEX = 200

pair_index = 0
result_dict = dict()

for file in tqdm(files):
    text = open(os.path.join(DATA_PATH, file)).read()
    for i in range(1, MAX_POSSIBLE_INDEX):
        first_tag = f'<first_{i}>'
        second_tag = f'<second_{i}>'
        propn_tag = f'<propn_{i}>'
        
        first_indexes = [(a.start(), a.end()) for a in list(re.finditer(first_tag, text))]
        second_indexes = [(a.start(), a.end()) for a in list(re.finditer(second_tag, text))]
        propn_indexes = [(a.start(), a.end()) for a in list(re.finditer(propn_tag, text))]

        
        antecedents = list()
        if len(first_indexes) > 0:
            for idx in range(0, len(first_indexes) // 2, 2):
                antecedents.append(text[first_indexes[idx][1]:first_indexes[idx+1][0]])
        
        pronominal_anaphora = list()
        if len(second_indexes) > 0:
            for idx in range(0, len(second_indexes) // 2, 2):
                pronominal_anaphora.append(text[second_indexes[idx][1]:second_indexes[idx+1][0]])
        
        nominal_anaphora = list()
        if len(propn_indexes) > 0:
            for idx in range(0, len(second_indexes) // 2, 2):
                nominal_anaphora.append(text[propn_indexes[idx][1]:propn_indexes[idx+1][0]])
                
        
        
        if (len(first_indexes) > 0 and len(second_indexes) > 0) or (len(first_indexes) > 0 and len(propn_indexes) > 0):
            min_index = 10000000000000
            max_index = -1
            for pair in first_indexes:
                if pair[0] < min_index:
                    min_index = copy.copy(pair[0])
                if pair[1] < min_index:
                    min_index = copy.copy(pair[1])
                    
            for pair in second_indexes:
                if pair[0] < min_index:
                    min_index = copy.copy(pair[0])
                if pair[1] < min_index:
                    min_index = copy.copy(pair[1])
             
            for pair in propn_indexes:
                if pair[0] < min_index:
                    min_index = copy.copy(pair[0])
                if pair[1] < min_index:
                    min_index = copy.copy(pair[1])
                    
                    
            ## max 
            
            
            for pair in first_indexes:
                if pair[0] > max_index:
                    max_index = copy.copy(pair[0])
                if pair[1] > max_index:
                    max_index = copy.copy(pair[1])
                    
            for pair in second_indexes:
                if pair[0] > max_index:
                    max_index = copy.copy(pair[0])
                if pair[1] > max_index:
                    max_index = copy.copy(pair[1])
             
            for pair in propn_indexes:
                if pair[0] > max_index:
                    max_index = copy.copy(pair[0])
                if pair[1] > max_index:
                    max_index = copy.copy(pair[1])
                    
                    
            # print(min_index, max_index)
            
            for ci in range(len(text[:min_index]), -1, -1):
                if text[ci] in '!?.':
                    break
                else:
                    min_index = copy.copy(ci)
            
            for ci in range(max_index+len(propn_tag), len(text)):
                if text[ci] in '!?.<>':
                    max_index = copy.copy(ci)
                    break
                else:
                    max_index = copy.copy(ci)
                
            
            final_text = str(text[min_index:max_index+1]).strip()
            
            result_dict[pair_index] = {
                'first': antecedents,
                'second': None if len(pronominal_anaphora) == 0 else pronominal_anaphora,
                'propn': None if len(nominal_anaphora) == 0 else nominal_anaphora,
                'text': final_text
            }
            pair_index += 1
    

df = pd.DataFrame().from_dict(result_dict, orient='index')
df.to_csv('corpus.csv')