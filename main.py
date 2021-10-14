#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from functools import update_wrapper
import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

permID = ["1936859631", "1218128630"]

chaveObj = ["cortina", "led"]


def trust(id):
    convID = str(id)
    if convID in permID:
        return 1


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    id = update.effective_user.id
    if trust(id):
        user = update.effective_user
        update.message.reply_markdown_v2(
        fr'Olá {user.mention_markdown_v2()}\!',
        )
        update.message.reply_text("Acesse Permitido! Seja bem-vindo ao serviço smart Rockets ☺ \ndigite /help para ajuda")
    else:
        update.message.reply_text("Acesso Negado!!")

def help_command(update: Update, context: CallbackContext) -> None:
    id = update.effective_user.id
    if trust(id):
        update.message.reply_text("Palavras Chaves para condições: Abrir, Fechar, Ligar, Desligar \nPalavras Chaves para objetos: cortina, led, ")
        update.message.reply_text("Basta enviar uma mensagem com uma palavra chave de condição e do objeto!")
    else:
        update.message.reply_text("Acesso Negado!!")


def auto(update: Update, context: CallbackContext) -> None:
    id = update.effective_user.id
    msg = update.message.text.lower()
    if trust(id):
        if "abrir" in msg or "ligar" in msg and not "desligar" in msg:
            cond = "Abrindo/Ligando"
        elif "fechar" in msg or "desligar" in msg:
            cond = "Fechando/Desligando"
        else:
            update.message.reply_text("Erro!\nCondição não declarada ou nao disponivel :(")

        for t in chaveObj:
            if t in msg:
                obj = t
                Bobj = 1
                break
        if not Bobj:
            update.message.reply_text("Erro!\nObjeto não declarado ou nao disponivel :(")
        update.message.reply_text(cond +" "+ obj)
    else:
        update.message.reply_text("Acesso Negado!!")


def main() -> None:
    
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    tokenArchive = open("token.txt")
    token = tokenArchive.read()
    tokenArchive.close()
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher


    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - run function auto
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, auto))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()