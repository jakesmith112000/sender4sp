import telebot
import random
import requests
from telebot import types
from telebot.types import Message
from SE.sender import Inboxing as SeSender
from logs.logging import safe_log,load_log


bot = telebot.TeleBot("6434792104:AAHSDKA-ABFI5jgr2TDhCoko0wfQGu9Cp5o")


authorized_users = [1973099958,5084753170,1971995086]

user_selection = {}

# Load subjects from subject.txt into a list
with open('subject.txt', 'r') as file:
    subjects = file.readlines()

# Function to get a random subject from the list
def get_random_subject():
    return random.choice(subjects).strip()  # Use strip() to remove newline characters

@bot.message_handler(func=lambda message: message.text == "Run Sender")
def runner_message_handler(message):
    user_id = message.chat.id
    if user_selection.get(str(user_id)) == None or None in list(user_selection[str(user_id)].values())[:5]:
        bot.send_message(user_id, "Please SET Up requirements before starting the sending. restart on /start")
        return None
    bot.send_message(user_id, "Loading informations ... ")
    bot.send_message(user_id, "Subject : {}".format(user_selection[str(user_id)]["subject"]))
    bot.send_message(user_id, "Spoofed : {}".format(user_selection[str(user_id)]["spoof"]))
    bot.send_message(user_id, "SMTP : {}".format(user_selection[str(user_id)]["SMTP"]))
    bot.send_message(user_id, "Please SEND Emails \n\n Emails format should be : \nfname,email\n\nPlease Respect the format. you can either send a file or text. \nyou can send more than one email (per line)")
    user_selection[str(user_id)]["emails"] = True
    # Update the subject before sending each email
    user_selection[str(user_id)]["subject"] = get_random_subject()

@bot.message_handler(commands=['start'],func = lambda message : message.chat.id in authorized_users)
def main_function(message):
    if user_selection.get(str(message.chat.id)) == None: 
        user_selection[str(message.chat.id)] = {
            "subject" : None,
            "spoof":None,
            "content":None,
            "SMTP":None,
            "emails":False,
            "status": None
        }
    print(user_selection[str(message.chat.id)])
    keyboard_layout = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
    subject = types.KeyboardButton("Subject")
    smtp = types.KeyboardButton("SMTP")
    spoof = types.KeyboardButton("Spoof")
    content = types.KeyboardButton("content")
    run = types.KeyboardButton("Run Sender")
    test = types.KeyboardButton("Test")

    keyboard_layout.row_width = 3
    keyboard_layout.row(subject,smtp)
    keyboard_layout.row(spoof,content)
    keyboard_layout.row(run)
    keyboard_layout.row(test)
    start_message = """
Welcome to SE Sender.
The ultimate Spoofed Sender

Please set up required informations from the following buttons before running the sender.

SPOOFED INFO, SMTP, Subject

those infos can change whenever you want
"""
    bot.send_message(message.chat.id,start_message,reply_markup=keyboard_layout,parse_mode="html")



@bot.message_handler(func= lambda message: message.text == "Run Sender")
def runner_message_handler(message):
    user_id = message.chat.id
    if user_selection.get(str(user_id)) == None or None in list(user_selection[str(user_id)].values())[:5]:
        bot.send_message(user_id,"Please SET Up requirements before starting the sending. restart on /start")
        return None
    bot.send_message(user_id,"Loading informations ... ")
    bot.send_message(user_id,"Subject : {}".format(user_selection[str(user_id)]["subject"]))
    bot.send_message(user_id,"Spoofed : {}".format(user_selection[str(user_id)]["spoof"]))
    bot.send_message(user_id,"SMTP : {}".format(user_selection[str(user_id)]["SMTP"]))
    bot.send_message(user_id,"Please SEND Emails \n\n Emails format should be : \nfname,email\n\nPlease Respect the format. you can either send a file or text. \nyou can send more than one email (per line)")
    user_selection[str(user_id)]["emails"] = True


@bot.message_handler(func= lambda message: message.text == "Test")
def runner_message_handler(message):
    user_id = message.chat.id
    if user_selection.get(str(user_id)) == None or None in list(user_selection[str(user_id)].values())[:5]:
        bot.send_message(user_id,"Please SET Up requirements before starting the sending. restart on /start")
        return None
    infos = user_selection[str(message.chat.id)]
    bot.send_message(user_id,"Loading informations ... ")
    bot.send_message(user_id,"Subject : {}".format(user_selection[str(user_id)]["subject"]))
    bot.send_message(user_id,"Spoofed : {}".format(user_selection[str(user_id)]["spoof"]))
    bot.send_message(user_id,"SMTP : {}".format(user_selection[str(user_id)]["SMTP"]))
    bot.send_message(user_id,"Testing ...")
    sn = SeSender(spoofed=infos["spoof"][0],smtps=infos["SMTP"],letter=infos["content"],subject=infos["subject"])
    try: sn.start(["TEST,frankmartz09@mail.com"],bot,user_id)
    except Exception as e:
        name = safe_log(str(e))
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        logs = types.InlineKeyboardButton(" Display Log !",callback_data=f"{name}")
        cancel = types.InlineKeyboardButton("❌ Cancel",callback_data="cancel")
        keyboard.add(logs,cancel)
        bot.send_message(user_id,"An Error Occurred",reply_markup=keyboard)
@bot.message_handler(func= lambda message: message.text == "content")
def content_message_handler(message):
    text = """
📨 <b>OLD content </b>: 

{0}

Enter New Content <i>(a file or text)</i>

Supported Tags :
🟢 [email] : Victim email
🟢 [name] : Victim name
🟢 [spoofedfname] : Spoof First Name
🟢 [spoofedlname] : Spoof Last Name
🟢 [spoofedfullname] : Spoof Full Name

example : 

Dear [name]

we happy to speak to you about this opportunities
yapping...
yapping...
yapping...

[spoofedfullname]
    """.format(user_selection.get(str(message.chat.id)).get("content"))
    bot.send_message(message.chat.id,text,parse_mode="html")
    user_selection[str(message.chat.id)]["status"] = "content"


@bot.message_handler(func= lambda message: message.text == "Subject")
def subject_message_handler(message):
    text = """
📨 <b>OLD SUBJECT </b>: {0} 

Enter New subject <i>(a file or text)</i>

Supported Tags :
🟢 [email] : Victim email
🟢 [name] : Victim name
🟢 [spoofedfname] : Spoof First Name
🟢 [spoofedlname] : Spoof Last Name
🟢 [spoofedfullname] : Spoof Full Name

example : Invitation to [name] by [spoofedfname]
    """.format(user_selection.get(str(message.chat.id)).get("subject"))
    bot.send_message(message.chat.id,text,parse_mode="html")
    user_selection[str(message.chat.id)]["status"] = "subject"

@bot.message_handler(func= lambda message: message.text == "Spoof")
def spoof_message_handler(message):
    text = """
📨 <b>OLD Spoof </b>: {0} 

Enter New spoof <i>(a file or text)</i>

format : fname,lname,spoofmail@spoof.xyz
    """.format(user_selection.get(str(message.chat.id)).get("spoof"))
    bot.send_message(message.chat.id,text,parse_mode="html")
    user_selection[str(message.chat.id)]["status"] = "spoof"

@bot.message_handler(func= lambda message: message.text == "SMTP")
def smtp_message_handler(message):
    text = """
📨 <b>OLD SMTP </b>: {0} 

Enter New SMTP <i>(a file or text)</i>

format : host|port|username|password
    """.format(user_selection.get(str(message.chat.id)).get("SMTP"))
    bot.send_message(message.chat.id,text,parse_mode="html")
    user_selection[str(message.chat.id)]["status"] = "SMTP"


@bot.message_handler(func = lambda message: True)
def _handle_inputs(message):
    user_id = message.chat.id
    if not choose_status(user_id,message.text):
        if user_selection.get(str(user_id)) != None and user_selection[str(user_id)]["emails"]:    
            emails = message.text.splitlines()
            infos = user_selection[str(user_id)]
            user_selection[str(message.chat.id)]["emails"] = False
            for spoof in infos["spoof"]:
                sn = SeSender(spoofed=spoof, smtps=infos["SMTP"],letter=infos["content"], subject=infos["subject"])
                sn.start(emails,bot,user_id)

@bot.message_handler(content_types=['document'])
def doc_handler(message):
    user_id = message.chat.id
    successful = 0
    file_id = message.document.file_id
    file_info = bot.get_file(file_id)
    file_url = f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}'
    response = requests.get(file_url)
    if response.status_code == 200:
        document_content = response.content.decode("utf-8")
        if not choose_status(user_id,document_content):
            if user_selection.get(str(user_id)) != None and user_selection[str(user_id)]["emails"]:
                emails = document_content.splitlines()
                infos = user_selection[str(user_id)]
                user_selection[str(message.chat.id)]["emails"] = False
                sn = SeSender(spoofed=infos["spoof"],smtps=infos["SMTP"],letter=infos["content"],subject=infos["subject"])
                # start multithreaded
                sn.start(emails,bot,user_id)


# callback query

@bot.callback_query_handler(func= lambda call: call.data == "cancel")
def add_balance_callback_handler(call):
    if isinstance(call, types.Message): user_id = call.chat.id
    else:user_id = call.message.chat.id
    if isinstance(call, types.Message): message_id = call.message_id
    else: message_id =  call.message.message_id
    bot.delete_message(user_id,message_id)

@bot.callback_query_handler(func= lambda call: call.data.isnumeric())
def __get_logs(call):
    user_id = call.message.chat.id
    name = int(call.data)
    try:bot.send_message(user_id,load_log(name))
    except: bot.send_message(user_id,"Couldn't Load Log")
# functions

def choose_status(user_id,text):
    if user_selection.get(str(user_id)) != None and user_selection[str(user_id)]["status"] != None:
        st = user_selection[str(user_id)]["status"] 
        if st  == "content":
            user_selection[str(user_id)]["content"] = text
        elif st == "subject":
            user_selection[str(user_id)]["subject"] = text
        elif st == "SMTP":
            try:
                text = text.splitlines()[0]
                if len(text.split("|"))<4: raise Exception
                user_selection[str(user_id)]["SMTP"] = text.split("|")
            except:
                bot.send_message(user_id,"INVALID FORMAT FOR SMTP\nrestart : /start")
        elif st == "spoof":
            text = text.splitlines()
            texts = []
            for text_ in text:
                try:
                    if len(text_.split(","))<3: raise Exception
                    texts.append(text_)
                    user_selection[str(user_id)]["spoof"] = texts
                except:
                    pass
            if texts == [] : bot.send_message(user_id,"INVALID FORMAT FOR SPOOF INFO\nrestart : /start")

        user_selection[str(user_id)]["status"] = None
        bot.send_message(user_id,"Done !")
        return True
    return False

if "__main__" == __name__:
    bot.infinity_polling()
