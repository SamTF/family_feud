### STEVE HARVEY
### A Discord command interface to the family_feud.py game logic

###### THE IMPORTS      ##########################################################
# My Family Feud scripts
import family_feud                                                  # handles all the actual game logic
from survey import Survey                                           # my Survey class
from time import sleep                                              # for a dramatic pause when submitting a guess

import discord                                                      # the main discord module
from discord.ext import commands                                    # commands are nice

# The Slash Commands module
from discord_slash import SlashCommand, SlashContext                # used to create slash commands /
from discord_slash.utils.manage_commands import create_choice, create_option       # used to specify the type of argument required


###### CONSTANTS        ##########################################################
TOKEN_FILE = '.family_feud.token'                                   # Name of the text file storing the unique Discord bot token (very dangerous, do not share)
game_survey = None                                                  # the survey currently at play

###### DISCORD STUFF ############################################################
### Creating the bot!
bot = commands.Bot(command_prefix='!feud ')

###### EVENTS        ##########################################################
# Runs this when the bot becomes online
@bot.event
async def on_ready():
    print("Ready to feud!")
    print(bot.user.name)
    await bot.change_presence(activity=discord.Game('Surveying 100 people'))



###### SLASH COMMANDS //// #################################################
slash = SlashCommand(bot, sync_commands=True)                                                                           # Initialises the @slash dectorator - NEEDS THE SYNC COMMANDS to be true
guild_ids = [349267379991347200]                                                                                        # The Server ID - not sure why did this needed


### Start a feud game
@slash.slash(
    name='feud',
    guild_ids=guild_ids,
    description='Receive a random Survey question and get ready to feud!',
    options=[
        create_option(
            name='answers',
            description='How many answers you will have to guess',
            option_type=4,  # integer
            required=False,
            choices=[
                create_choice(name='Random',    value=0),
                create_choice(name='4',         value=4),
                create_choice(name='5',         value=5),
                create_choice(name='6',         value=6),
                create_choice(name='7',         value=7),
                create_choice(name='8',         value=8)
            ]
        ),
        create_option(
            name='god_mode',
            description='Infinite strikes: you can play forever until you guess all answers',
            option_type=5,   # bool
            required=False
        )
    ])
async def feud(ctx, answers=0, god_mode=False):
    global game_survey

    # Checks if there is a game in progress - aborts if so
    if game_survey:
        msg = 'There is a game currently being played. Finish it before you can start a new one!'
        await ctx.send(msg)
        return

    # Starts the game!
    game_survey = family_feud.start_game(answers, god_mode)

    # terminal output
    print(f'{ctx.author.name} has started a feud!')
    print(game_survey.question)
    
    # Discord output - the Survey's question
    if god_mode: await ctx.send('`[GOD MODE ENABLED]`')
    msg = family_feud.show_board()
    await ctx.send(msg)


### Playing the game and guessing the answers!
@slash.slash(
    name='guess',
    guild_ids=guild_ids,
    description='Try to guess the answers on the big board!',
    options=[
        create_option(
            name='guess',
            description='What do you think would be a good answer?',
            option_type=3,  # string
            required=True
        )
    ]
)
async def guess(ctx, guess:str):
    global game_survey

    # Checks if there is a game being played
    if not game_survey:
        msg = 'There is no survey current being played.\nUse `/feud` to start a game!'
        await ctx.send(msg)
        return

    # removing leading spaces and converting to uppercase
    guess = guess.strip().upper()

    # displaying players' guesses
    await ctx.send(f'{ctx.author.name} guessed **{guess}**')
    sleep(1)
    await ctx.send(f'Is it on the big board?')

    # Checking if the input is valid
    if not family_feud.valid_input(guess):
        msg = 'Answer must be at least 3 characters long. Try another!'
        await ctx.send(msg)
        return
    
    # If this guess has already been tried before
    if guess in family_feud.previous_attempts:
        msg = 'You already said this one. Try another!!'
        await ctx.send(msg)
        return
    
    correct, msg = family_feud.is_on_the_big_board(guess)
    print(f'{ctx.author.name}\'s guess of [{guess}] was {correct}')

    sleep(1)
    await ctx.send(msg)

    # Checks if the game is over - by victory or defeat
    game_over, msg = family_feud.is_game_over()
    if game_over:
        await ctx.send(msg)
        await ctx.send(game_survey.discord_msg())
        game_survey = None
        family_feud.reset_variables()
    

### Showing the state of the board
@slash.slash(
    name='board',
    guild_ids=guild_ids,
    description='Shows the current state of the board: which answers have been gotten, and which ones are missing.'
)
async def board(ctx):
    # Checks if there is a game being played
    if not game_survey:
        msg = 'There is no survey current being played.\nUse `/feud` to start a game!'
        await ctx.send(msg)
        return
    
    msg = family_feud.show_board()
    await ctx.send(msg)





###### RUNNING THE BOT #################################################
if __name__ == "__main__":
    print("_____________Family Feud INITIALISED_____________")
    with open(TOKEN_FILE, 'r') as f:
        token = f.read()
    
    bot.run(token)