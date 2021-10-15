from functools import update_wrapper
import logging
from serial.serialwin32 import Serial

#libraries for telegram bot
#pip3 install python-telegram-bot
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

#libraries for arduino comms
import threading
import serial
import time

conected = False 
port = 'COM3' 
velBaud = 9600

receivedMessages = 1
offArduinoThread = False 
receivedText = "" 

try: 
    SerialArduino = serial.Serial(port,velBaud, timeout = 0.5) 
except: 
    print("Verificar porta serial ou religar Arduino") 

#def handle_data(data):  
    #global receivedMessages, receivedText
    #print("Recebi " + str(receivedMessages) + ": " + data) 
    
    #receivedMessages += 1 
    #receivedText = data 

def read_from_port(ser): 
    global conected, offArduinoThread 
    while not conected: 
        conected = True 
        
        #while True:
           #reading = ser.readline().decode()
           #if reading != "": 
               #handle_data(reading)
        if offArduinoThread: 
            print("Desligando Arduino")
            break 



readSerialThread = threading.Thread(target=read_from_port, args=(SerialArduino,)) 
readSerialThread.start()

readSerialThread.join() 
print (SerialArduino.read().decode())

print("Preparando Arduino") 
time.sleep(2) 
print("Arduino Pronto") 

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

chaveObj = ["cortina", "led", "luz"]


def TeleTokens(path, shoudSplit):
    archive = open(path, "r+")
    value = archive.read()
    if shoudSplit:
        value.splitlines()
    archive.close()
    return(value)

token = TeleTokens("token.txt", 0)
permID = TeleTokens("ids.txt", 1)   


def trust(id):
    convID = str(id)
    if convID in permID:
        return 1


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    id = update.effective_user.id
    print(id)
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
        update.message.reply_text("Palavras Chaves para condições: Abrir, Fechar, Ligar, Desligar \nPalavras Chaves para objetos: " + chaveObj)
        update.message.reply_text("Basta enviar uma mensagem com uma palavra chave de condição e do objeto!")
    else:
        update.message.reply_text("Acesso Negado!!")


def signal(update: Update, context: CallbackContext) -> None:
    Bobj = False
    id = update.effective_user.id
    print(id)
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

        if Bobj and cond != "":
            SerialArduino.write((cond + " " + obj + '\n').encode())
            offArduinoThread = True 
            #SerialArduino.close() 
            readSerialThread.join() 
            print (SerialArduino.read())
            update.message.reply_text(cond +" "+ obj)
    else:
        update.message.reply_text("Acesso Negado!!")
        

def main() -> None:
    
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher


    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - run function signal
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, signal))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()