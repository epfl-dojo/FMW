#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from telegram import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging, fmw, pprint


def build_menu(buttons,
               n_cols,
               header_buttons = None,
               footer_buttons = None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('/crimList\n')


def echo(bot, update):
    update.message.reply_text(update.message.text)


def crim(bot, update):
    for criminal in fmw.getCriminals() :
        update.message.reply_text(fmw.getCriminal_name(criminal))

def sanitizeCriminalName(criminalName):
    return criminalName.replace(" ", "_")

def crimList(bot, update):
    criminals = fmw.getCriminalsList()
    # Parameters:
    #
    # text (str) – Label text on the button.
    # url (Optional[str]) – HTTP url to be opened when button is pressed.
    # callback_data (Optional[str]) – Data to be sent in a callback query to the bot when button is pressed, 1-64 bytes.
    # switch_inline_query (Optional[str]) – If set, pressing the button will prompt the user to select one of their chats, open that chat and insert the bot’s username and the specified inline query in the input field. Can be empty, in which case just the bot’s username will be inserted.
    # switch_inline_query_current_chat (Optional[str]) – If set, pressing the button will insert the bot’s username and the specified inline query in the current chat’s input field. Can be empty, in which case only the bot’s username will be inserted.
    # callback_game (Optional[telegram.CallbackGame]) – Description of the game that will be launched when the user presses the button.
    # **kwargs (dict) – Arbitrary keyword arguments.

    button_list = [
        InlineKeyboardButton("%s" % criminal, switch_inline_query_current_chat='/getData ' + sanitizeCriminalName(criminal)) for criminal in criminals
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    update.message.reply_text('Please choose a criminal:', reply_markup=reply_markup)


def getCriminalData(bot, update):
    splitedText = update.message.text.split()
    update.message.reply_text(splitedText[1])



def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    #print(Filters.text)
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("crimList", crimList))
    dp.add_handler(CommandHandler("crim", crimList))
    dp.add_handler(CommandHandler("getData", getCriminalData))

    #telegram.ext.commandhandler.CommandHandler("getData", callback, allow_edited=False, pass_args=False, pass_update_queue=False, pass_job_queue=False)




    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
