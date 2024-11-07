#!/usr/bin/env python
# coding: utf-8
  
## Import Module Requirements:
import random
from random import randrange
import pandas as pd

## Import Variables via Files from Directory:
from songStructureVariables import song_form_list, phrase_list, PC2_phrase_list

## Constant Variables:
# Consistent Sections:
I1 = 'Intro'
O1 = 'Outro'

# Primary Sections:
V1 = 'Verse'
C1 = 'Chorus'

# Secondary Sections:
S2  = 'Solo'
B2  = 'Bridge'
M2  = 'Middle 8'
R2  = 'Refrain'
# PV2 = 'Pre-Verse'
PC2 = 'Pre-Chorus'

def get_connecting_sections(index, form, section):
    if (index + 1 < len(form) and index - 1 >= 0):
        prev_section = str(form[index - 1])
        curr_section = str(section)
        next_section = str(form[index + 1])
        return prev_section, curr_section, next_section
    else:
        prev_section = 'None'
        curr_section = 'None'
        next_section = 'None'
        return prev_section, curr_section, next_section
    
def random_song_form_selector(song_form_list, I1, O1, V1, C1, S2, B2, M2, R2, PC2, phrase_list, PC2_phrase_list):
    ## Randomly Select a Song Form:
    random_form = random.choice(song_form_list)
    # print('Randomly Selected Song Form: {0}'.format(random_form))

    ## Tokenize Randomized Form into Sections:
    tokenized_form = list(random_form) # Tokenize Randomized Form into Sections
    tokenized_form = [section.replace('A', V1) for section in tokenized_form] # Add Verse Sections
    tokenized_form = [section.replace('B', C1) for section in tokenized_form] # Add Chorus Sections
    tokenized_form.insert(0, I1) # Add Intro Section

    ## Randomly Add Pre-Chorus Section:
    PC2_duplicates = 'False' # Allows for adding Multiple Pre-Chorus Sections
    for index, section in enumerate(tokenized_form):
        prev_section, curr_section, next_section = get_connecting_sections(index, tokenized_form, section)
        ## Randomly Add Pre-Chorus Section:
        if curr_section == C1 and prev_section == V1:
            if random.choice([True, False]) == True:
                PC2_duplicates = 'True'
                tokenized_form.insert(index, PC2)
                # print(tokenized_form)

    if PC2_duplicates == 'True':
        for index, section in enumerate(tokenized_form):
            prev_section, curr_section, next_section = get_connecting_sections(index, tokenized_form, section)
            ## Randomly Add Pre-Chorus Section:
            if curr_section == C1 and prev_section == V1:
                tokenized_form.insert(index, PC2)
                # print(tokenized_form)
    else:
        pass

    ## Randomly Add Bridge OR Middle 8 Section:
    B2_duplicates = 'False' # Allows for only 1 Bridge
    M2_duplicates = 'False' # Allows for only 1 Middle 8
    for index, section in enumerate(tokenized_form):
        prev_section, curr_section, next_section = get_connecting_sections(index, tokenized_form, section)

        ## Randomly Add Bridge Section:
        if curr_section == C1 and next_section == V1 and B2_duplicates == 'False':
            if random.choice([True, False]) == True:
                B2_duplicates = 'True'
                tokenized_form.insert(index + 1, B2)
                # print(tokenized_form)
        if curr_section == V1 and next_section == C1 and B2_duplicates == 'False':
            if random.choice([True, False]) == True:
                B2_duplicates = 'True'
                tokenized_form.insert(index + 1, B2)
                # print(tokenized_form)

        ## Randomly Add Middle 8 Section:
        if curr_section == C1 and next_section == C1 and M2_duplicates == 'False':
            if random.choice([True, False]) == True:
                M2_duplicates = 'True'
                tokenized_form.insert(index + 1, M2)
                # print(tokenized_form)
        if curr_section == V1 and next_section == V1 and M2_duplicates == 'False':
            if random.choice([True, False]) == True:
                M2_duplicates = 'True'
                tokenized_form.insert(index + 1, M2)
                # print(tokenized_form)

    ## Trim Excess Bridge OR Middle 8 Sections:
    section_dictionary = {section: index for index, section in enumerate(tokenized_form)}
    for index, section in enumerate(tokenized_form):
        prev_section, curr_section, next_section = get_connecting_sections(index, tokenized_form, section)

        ## Remove Middle 8 Section IF it's before a Bridge:
        if curr_section == M2 and B2 in tokenized_form:
            if index < section_dictionary[B2]:
                tokenized_form.remove(section)
                # print(tokenized_form)

        ## Remove Bridge Section IF it's before a Middle 8:
        if curr_section == B2 and M2 in tokenized_form:
            if index < section_dictionary[M2]:
                tokenized_form.remove(section)
                # print(tokenized_form)

    ## Randomly Add Solo Section:
    form_range = len(tokenized_form) # Get Range of the Song Form
    range_limiter = randrange(form_range) # Used later to randomly add a Solo Section
    if random.choice([True, False]) == True:
        tokenized_form.insert(range_limiter + 2, S2)
        # print(tokenized_form)

    ## Add Outro Section:
    tokenized_form.append(O1)
    
    ## Randomly Select Phrase Structure:
    V1_random_phrase = random.choice(list(phrase_list))
    C1_random_phrase = random.choice(list(phrase_list))
    B2_random_phrase = random.choice(list(phrase_list))
    M2_random_phrase = random.choice(list(phrase_list))
    PC2_random_phrase = random.choice(list(PC2_phrase_list))
    I1_random_phrase = random.choice(['(chorus phrase)', '(verse phrase)'])
    
    section_phrase_dict = {'Verse' : V1_random_phrase
                          ,'Chorus' : C1_random_phrase
                          ,'Bridge' : B2_random_phrase
                          ,'Middle 8' : M2_random_phrase
                          ,'Pre-Chorus' : PC2_random_phrase
                          ,'Intro' : I1_random_phrase
                          ,'Solo' : '(prev or next)'
                          ,'Outro' : '(prev)'}
    
    form_df = pd.DataFrame(tokenized_form, columns=['Section'])
    form_df['Phrase'] = form_df['Section'].map(section_phrase_dict)

    return form_df

def export_csv(df):
    with open('random-song-structure.csv','w') as export_file: # 'w' rewrites export file each time the script runs
        df.to_csv('random-song-structure.csv', mode='w', encoding='utf-8', index=False, header=False) # mode='w' rewrites export file each time the script runs

random_song_form = random_song_form_selector(song_form_list, I1, O1, V1, C1, S2, B2, M2, R2, PC2, phrase_list, PC2_phrase_list)

export_csv(random_song_form)