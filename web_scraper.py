from survey import Survey                                   # My custom class to hold Survey data
from bs4 import BeautifulSoup                               # HTML scraper and parser
import requests                                             # Fetching HTML data from websites
import json                                                 # Saving Survey objects to JSON format


# Getting the website HTML
def get_HTML_content(website:str) -> BeautifulSoup:
    '''
    Fetches the HTML content of the webpage. Returns a BeautifulSoup object.
    website: webpage's URL
    '''
    source = requests.get(website).text
    soup = BeautifulSoup(source, 'lxml')
    return soup


# Getting every Survey Table
def get_all_surveys(HTML_data:BeautifulSoup):
    '''
    Finds all the HTML data containing survey questions and answers, and parses that into a Survey Object. Returns list of Survey objects.
    HTML_data: a BeautifulSoup object for the requested webpage.
    '''
    survey_tables = HTML_data.find_all('table', {"cellpadding" : "11"})     # Every <table> element with a cellpadding attr of 11... yes this website HTML layout is fucking horrendous my god
    SURVEYS = []
    
    # Getting the required data from every survey
    for survey in survey_tables:
        # Getting the question -> the previous table element with these exact attributes
        question_html = survey.find_previous('table', {'width' : '570', 'cellpadding' : '0'})
        question = question_html.p.text

        # Getting the answers and their respective points
        text = survey.center.find_all('b')                                  # Answers and points are all in <b> tags
        answers = [a.text for a in text[::2]]                               # Answers are every odd text element
        points = [p.text for p in text[1::2]]                               # Points are every even element

        SURVEYS.append(Survey(question, answers, points))
    
    return SURVEYS


# Saving to disk
def save_as_json(surveys:list, file_name:str):
    '''
    Uses the Survey's to_json method to convert the object's data into a JSON format (dict), then saves it to disk.
    surveys: list of Survey objects
    file_name: name of the JSON to write to
    '''
    SURVEYS_JSON = [survey.to_json() for survey in surveys]
    with open(file_name, 'w+') as file:
        json.dump(SURVEYS_JSON, file)




### Scraping and saving all data for seasons 16 through 21, for questions with 1 to 8 answers
def download_all_surveys():
    URL = 'https://mstiescott.neocities.org/feud{0}_{1}.html'
    FILE = 'surveys/{0}_{1}.json'

    for season in range(16, 22):
        for answers in range(4, 9):
            webpage = URL.format(season, answers)
            file_name = FILE.format(season, answers)
            print(f'Scraping {webpage}...')

            HTML_content = get_HTML_content(webpage)
            surveys = get_all_surveys(HTML_content)
            save_as_json(surveys, file_name)
            print(f'Saved data to --> {file_name}')


download_all_surveys()