import json
from survey import Survey

from typing import List, Dict
import os


def create_surveys(file_name:str) -> List[Survey]:
    '''
    Crates Survey objects from the data in a JSON file. Returns a list of Survey objects.
    '''
    data = None
    surveys = []

    # Reading the local JSON file
    with open(file_name, 'r') as file:
        data =  json.load(file)
    
    # Creating Survey objects from the JSON data
    for item in data:
        s = Survey(item['question'], item['answers'], item['points'])
        surveys.append(s)
    
    return surveys


def get_all_surveys() -> Dict[int, List[Survey]]:
    '''
    Reads every JSON file in a directory, and creates Survey objects for all their data.
    Returns a dictionary as {Num of Questions : List of Surveys}
    '''
    survey_data = os.listdir('surveys/')
    SURVEYS = {}

    for s in survey_data:
        name = s[:-5]                                           # removes the '.json' from the file name to get just the name
        season, q_num = name.split('_')                         # splits the file name into season and number of questions
        print(f'Season: {season:4} | Questions: {q_num:4}')

        value = create_surveys(f'surveys/{s}')                  # creates Survey objects for all the surveys in this file

        SURVEYS.setdefault(int(q_num), [*value])                # *appends them to a dictionary sorted by number of questions, creating a new list if that key does not exist yet

    return SURVEYS