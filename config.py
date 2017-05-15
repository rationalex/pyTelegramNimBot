# ===================== Tech info ============================
AUTH_TOKEN = "347011927:AAFmXo0oJUmtL82-Q4J6PMjFIYaP4e4-xFI"
MY_TELEGRAM_ID = "11298983"

# ===================== Service  =============================
NEW_ARGUMENTS_REGEXP = """\
((\d+)\s*)+\s*(me|you)
"""

# ===================== Messages =============================
HELP_TEXT = """Available commands:
/start_game 11 2 57 179 me|you <- example input for new game request. "me" if you want to go first, "you" otherwise.
/reduce <pile_num> <number_of_stones>
/end_game - terminate current game
/help - get some helpful info
"""

BOT_STARTUP_TEXT = """\
Nim-Bot v.0.1
[I'm up]
"""

BOT_SHUTDOWN_TEXT = """\
Bye!
"""

# ====================== In-game messages ====================
GAME_ALREADY_STARTED_ERR = """\
Game is already in process.
Type /end_game to throw in the towel.
"""

GAME_NOT_STARTED_ERR = """\
Game is not started.
Enter /start_game with proper arguments to start it
"""

GAME_FINISHED_ERR = """\
Game is finished.
Enter /start_game with proper arguments to start it
"""

INVALID_GAME_ARGUMENTS_ERR = """
Incorrect arguments. Please follow this regexp\n{args_re}
""".format(args_re=NEW_ARGUMENTS_REGEXP)

INCORRECT_TURN_DESCRIPTION = """\
Incorrect turn. Please enter number of pile and number of stones to reduce
"""

GAME_STARTED_TEXT = """\
Game is on!
"""

TURN_REQUEST_TEXT = """\
Now it's your turn!
"""

VICTORY_TEXT = """\
You are victorious!
"""

DEFEAT_TEXT = """\
AI wins!
Good luck next time.
"""

NOT_PLAYERS_TURN_ERR = """\
"It's not your turn now, wait a bit!"
"""
