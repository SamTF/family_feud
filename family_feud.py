### FAMILY FEUD
### Contains all the logic for playing a game of Family Feud

### IMPORTS
from survey import Survey, get_all_surveys
from typing import Tuple
import random


### CONSTANTS
SURVEYS = get_all_surveys()             # loading all the Survey objects from disk
MAX_STRIKES = 3                         # after 3 wrong answers, you lose

### GLOBAL VARIABLES
game_survey: Survey = None              # the survey currently at play
God_mode = False                        # in god mode, you can guess forever and never lose
strikes = 0                             # current wrong answer counter
previous_attempts = []                  # answers that players have already attempted
correct_answers = []                    # answers that players have already guessed correctly


def start_game(answers:int, god_mode:bool) -> Survey:
    '''
    Initialises all the variables needed to play a game of Family Feud. Returns a survey.

    answers: If specified, the amount of answers in the Survey. Otheriwse random.
    god_mode: If true, it is impossible to strike out.
    '''
    global game_survey, God_mode

    game_survey = random_survey(answers)
    God_mode = god_mode

    return game_survey


def reset_variables() -> None:
    '''
    Resetting all game variables to their original empty state.
    '''
    global game_survey, God_mode, strikes, previous_attempts, correct_answers
    game_survey = None
    God_mode = False
    strikes = 0
    previous_attempts = []
    correct_answers = []


def random_survey(answers=0) -> Survey:
    '''
    Fetching a random Survey.
    
    answers: if specified, returns a Survey with that amount of answers to guess. Otherwise, it's random.
    '''
    i = answers if answers else random.choice(list(SURVEYS.keys()))
    s = random.choice(SURVEYS[i])
    return s


def valid_input(input:str) -> bool:
    '''
    Checks if the player's input is valid. Returns true/false.
    '''
    filtered_input = ''.join(input.split())
    return len(filtered_input) >= 3


def is_on_the_big_board(guess:str) -> Tuple[bool, str]:
    '''
    Checks if a guess is correct. Returns a bool and a message.
    '''
    global game_survey, correct_answers, previous_attempts, strikes

    # Checks of the player's guess exists as a substring within the answer string - first index of the answer tuple
    match = game_survey.try_guess(guess)
    
    # On a GOOD answer
    if(match):
        # Checks if this answer has already been gotten
        if match in correct_answers:
            return False, 'You already got this answer, champ! Try another!!'
        
        # Keeps track of the answers already guessed correctly
        correct_answers.append(match)
        msg = f'Good answer! ➜  {match[0]} for {match[1]} points'
        return True, msg
    
    # On a BAD answer
    else:
        strikes += 1
        msg = ' ❌ ' * strikes
        return False, msg


def is_game_over() -> Tuple[bool, str]:
    '''
    Checks if the game is over by victory or defeat, and if so, also returns an appropriate message.
    '''
    if victory():
        return True, '🎈🎈🎈 YOU WIN!!! 🎈🎈🎈'
    elif defeat():
        return True, '**\*\*\* STRIKE OUT \*\*\***'
    else:
        return False, 'nothing to report'

def victory() -> bool:
    return len(correct_answers) == game_survey.num_of_answers

def defeat():
    return (strikes == MAX_STRIKES and not God_mode)


# Show the board
def show_board() -> str:
    '''
    Shows the current state of the board: which answers have been gotten and which ones are missing.
    '''
    board = f'**{game_survey.question}**'

    for i, ans in enumerate(game_survey.answers):
        if ans in correct_answers:
            s = f'\n  {i+1}. {ans[0]} ➜  {ans[1]}'
        else:
            s = f"\n  {i+1}. {'❓❓❓'}"
        board += s
    return board

          


if __name__ == "__main__":    
    pass
else:
    print('FAMILY FEUD IMPORTED')