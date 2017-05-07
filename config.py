# ===================== Tech info ============================
auth_token = "347011927:AAFmXo0oJUmtL82-Q4J6PMjFIYaP4e4-xFI"
my_telegram_id = "11298983"

# ===================== Service  =============================
new_game_arguments_regexp = """\
((\d+)\s*)+\s*(me|you)
"""

# ===================== Messages =============================
help_text = """Available commands:
/start_game 11 2 57 179 me|you <- example input for new game request. "me" if you want to go first, "you" otherwise.
/reduce <pile_num> <number_of_stones>
/end_game - terminate current game
/help - get some helpful info
"""

bot_startup_text = """\
Nim-Bot v.0.1
[I'm up]
"""

bot_shutdown_text = """\
Bye!
"""

# ====================== In-game messages ====================
game_already_started = """\
Game is already in process.
Type /end_game to throw in the towel.
"""

game_not_started = """\
Game is not started.
Enter /start_game with proper arguments to start it
"""

game_finished = """\
Game is finished.
Enter /start_game with proper arguments to start it
"""

incorrect_game_arguments = """
Incorrect arguments. Please follow this regexp\n{args_re}
""".format(args_re=new_game_arguments_regexp)

incorrect_turn_description = """\
Incorrect turn. Please enter number of pile and number of stones to reduce
"""

game_started_text = """\
Game is on!
"""

turn_request = """\
Now it's your turn!
"""

victory_text = """\
You are victorious!
"""

defeat_text = """\
AI wins!
Good luck next time.
"""

not_players_turn = """\
"It's not your turn now, wait a bit!"
"""
