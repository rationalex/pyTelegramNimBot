# -*- coding: utf-8 -*-

import telebot
import config
import logging

import game

# ======================== Game setup =======================
games = dict()

# ========================  Bot setup =======================
bot = telebot.TeleBot(config.auth_token)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


# ======================== Auxiliary ========================
def request_turn_from_player(chat_id, sizes):
    bot.send_message(chat_id,
                     "Current sizes: \n{}\nIt's your turn now!".format(' '.join(map(str, sizes))))


# =======================  Bot logic ========================
@bot.message_handler(commands=['start', 'help'])
def handle_help(message):
    bot.send_message(message.chat.id, config.help_text)


@bot.message_handler(commands=['start_game'], content_types=['text'])
def handle_start(message: telebot.types.Message):
    if message.chat.id in games:
        cur_game = games[message.chat.id]
        if not cur_game.is_finished():
            bot.send_message(message.chat.id, config.game_already_started)
            return

    # otherwise new game should be started
    data = message.text.split()
    turn = data[-1]
    if turn not in ['me', 'you']:
        bot.send_message(message.chat.id, config.incorrect_game_arguments)
        return

    for size in data[1:-1]:
        if not size.isdigit():
            bot.send_message(message.chat.id, config.incorrect_game_arguments)
            return

    sizes = list(map(int, data[1:-1]))
    if not sizes:
        bot.send_message(message.chat.id, config.incorrect_game_arguments)
        return

    cur_game = game.Game(piles_sizes=sizes,
                         player_id=message.chat.id,
                         whose_turn=(lambda s: game.Turn.Player
                                     if s == 'me' else game.Turn.AI)(turn))

    games[message.chat.id] = cur_game
    logging.debug("Game with {} started!".format(message.chat.id))
    bot.send_message(message.chat.id, config.game_started_text)
    if turn == 'you':
        sizes = cur_game.perform_ai_turn()
        if not sizes:
            games[message.chat.id].finish()
            bot.send_message(message.chat.id, config.defeat_text)
            logging.debug("Game with {} finished!".format(message.chat.id))
            return

    request_turn_from_player(message.chat.id, sizes)


@bot.message_handler(commands=['reduce'], content_types=['text'])
def handle_player_turn(message: telebot.types.Message):
    if message.chat.id not in games:
        bot.send_message(message.chat.id, config.game_not_started)
        return

    if games[message.chat.id].is_finished():
        bot.send_message(message.chat.id, config.game_finished)
        return

    data = message.text.split()[1:]
    if len(data) != 2:
        bot.send_message(message.chat.id, config.incorrect_turn_description)
        return

    if not data[0].isdigit() or not data[1].isdigit():
        bot.send_message(message.chat.id, config.incorrect_turn_description)
        return

    pile_num, num_to_reduce = map(int, data)
    try:
        new_piles = games[message.chat.id].accept_turn_from_player(pile_num, num_to_reduce)
        if not new_piles:
            games[message.chat.id].finish()
            bot.send_message(message.chat.id, config.victory_text)
            return
    except game.GameException as exception:
        bot.send_message(message.chat.id, exception.message)
        return

    # if everything is ok we let AI perform turn and send the result to player

    new_piles = games[message.chat.id].perform_ai_turn()
    if not new_piles:
        games[message.chat.id].finish()
        bot.send_message(message.chat.id, config.defeat_text)
        return

    request_turn_from_player(message.chat.id, new_piles)


# ======================== Running ===========================
def main():
    bot.polling(none_stop=True, interval=0)

if __name__ == "__main__":
    main()
