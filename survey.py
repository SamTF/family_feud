from operator import itemgetter                                 # For sorting the tuple list by the second element
import json, os                                                 # For reading JSON files from disk
from typing import List, Dict, Tuple                            # For type hinting

### SURVEY CLASS
class Survey:
    def __init__(self, question:str, answers:List[str], points:List[str]) -> None:
        '''
        Creates a Survey object.

        question: The survey question.
        answers: List of all answers to the questions
        points: Points that each answer is worth
        '''
        points = [self.to_int(num) for num in points]           # Converts the points array from string to integer

        self.question = question                                # The survey question
        self.answers = list(zip(answers, points))               # Combines these two lists into a single list of tuples as (answer, points)
        self.answers.sort(key=itemgetter(1), reverse=True)      # Sorting the tuple list by descending order of points [1] (for some reason they get jumbled up)
        self.num_of_answers = len(answers)                      # How many answers total are available
        self.total_points = sum(points)                         # The total points for winning this survey
    
    # Printing out these values nicely
    def __repr__(self) -> str:
        output = f"{'*' * 30}\n{self.question}"
        for item in self.answers:
            s = f'\n  {item[0]:20}  {item[1]:4}'                # even string spacing: https://www.w3resource.com/python/python-format.php
            output += s
        
        return output
    
    def discord_msg(self) -> str:
        '''
        Returns the Survey data as a string formatted for Discord.
        '''
        msg = f"**{self.question}**"
        for i, answer in enumerate(self.answers):
            s = f'\n{i+1}. {answer[0]} ➜  {answer[1]}'
            msg += s
        return msg
    
    # Converts the Object into Dict/JSON format so that it can be saved to disk
    def to_json(self) -> dict:
        return {'question': self.question,
                'answers': [x[0] for x in self.answers],
                'points': [x[1] for x in self.answers]
        }
    
    # Since the website motherfucker has some strings in the points section, we have to use this to check whether or not the value can actually be converted to an int, and return a fallback value if not, to avoid ValueErrors
    def to_int(self, int_as_str) -> int:
        try:
            return int(int_as_str)
        except:
            return 1
    
    # Checks of the player's answer exists as a substring within the answer string - first index of the answer tuple
    def try_guess(self, guess:str) -> Tuple[str, int] or bool:
        try:
            match = [ans for ans in self.answers if guess in ans[0]][0]
            return match
        except:
            return False


### Loading Surveys from JSON
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
        value = create_surveys(f'surveys/{s}')                  # creates Survey objects for all the surveys in this file
        SURVEYS.setdefault(int(q_num), [*value])                # *appends them to a dictionary sorted by number of questions, creating a new list if that key does not exist yet

    return SURVEYS