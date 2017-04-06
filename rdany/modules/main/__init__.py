from flask import abort
from flask import Flask
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import g

import json
import time
import requests
import datetime

import random as rd

from rdany import app

main = Blueprint('main', __name__)

from difflib import SequenceMatcher

def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

if 0:
    import sqlite3

    DATABASE = 'database.db'

    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
        return db

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()



## SQLITE

import sqlite3
from flask import g

DATABASE = 'queue.db'
DATABASE_SIMSIMI = 'simsimi_log.db'


def get_db(dbname=''):
    if not dbname:
        dbfile = DATABASE
    elif dbname == 'simsimi':
        dbfile = DATABASE_SIMSIMI
    db = getattr(g, '_database_{0}'.format(dbname), None)
    if db is None:
        setattr(g, '_database_{0}'.format(dbname), sqlite3.connect(dbfile))
        db = getattr(g, '_database_{0}'.format(dbname), None)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
    db = getattr(g, '_database_simsimi', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False, dbname=None):
    cur = get_db(dbname).execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def sqlite_execute(query, name, debug = False, dbname=None):
    try:
        cur = get_db(dbname).execute(query)
        get_db(dbname).commit()
        print ('{0} applied'.format(name))
        return True
    except sqlite3.OperationalError:
        print ('{0} already applied'.format(name))
        if debug:
            raise
        return False
    except:
        raise


def init_db ():
    sqlite_execute('''CREATE TABLE queue
                        (id integer primary key,
                        platform string,
                        user_id string,
                        message_id string,
                        message_text string,
                        answer_text string,
                        answered integer,
                        datetime integer,
                        day integer,
                        proposed_answer_text string)''', "stats")


    sqlite_execute('''CREATE TABLE queue
                        (id integer primary key,
                        platform string,
                        user_id string,
                        message_id string,
                        message_text string,
                        answer_text string,
                        answered integer,
                        datetime integer,
                        day integer,
                        proposed_answer_text string)''', "stats", dbname="simsimi")

##

## TELEGRAM

def send_request(access_point, data=None, retry=None):
    headers = {'user-agent': "rDany"}
    token = app.config["TELEGRAM_TOKEN"]
    r = None
    tries = 0
    while 1:
        tries = tries + 1
        if tries > 1:
            print ("Tries: {0}".format(tries))
        try:
            r = requests.get('https://api.telegram.org/bot{0}/{1}'.format(token, access_point), data=data, timeout=10, headers=headers)
            if r.status_code != requests.codes.ok:
                if r.status_code == 403:
                    print ("Telegram: User blocked us")
                break
            if r:
                r_json = r.json()
                if not r_json["ok"]:
                    print ("Telegram: API not ok {0}".format(access_point))
                    print (r.text)
                else:
                    print ("Telegram: API ok")
                break
            else:
                print (r)
                print ("Telegram: none r Error {0}".format(access_point))
        except requests.exceptions.ConnectionError:
            print ("Telegram: ConnectionError {0}".format(access_point))
            if not retry:
                break
        except requests.exceptions.Timeout:
            if retry:
                print ("Telegram: Timeout {0}".format(access_point))
            else:
                break
        time.sleep(5+tries)
    return r

##

def save_message(platform, user_id, message_id, message_text, dbname=None, answer=None, group=0, muted=0):
    epoch = datetime.datetime.utcfromtimestamp(0)
    today = datetime.datetime.today()
    d = today - epoch
    if not answer:
        get_db(dbname).execute("INSERT INTO queue VALUES (null, ?, ?, ?, ?, '', 0, ?, ?, '', ?, ?)", [platform, user_id, message_id, message_text, int(time.time()), d.days, group, muted])
    else:
        get_db(dbname).execute("INSERT INTO queue VALUES (null, ?, ?, ?, ?, ?, 1, ?, ?, '', ?, ?)", [platform, user_id, message_id, message_text, answer, int(time.time()), d.days, group, muted])
    get_db(dbname).commit()


@main.route('/', methods=['POST', 'GET']) 
def index():
    init_db()
    msg = request.json
    
    welcome_text = """*Welcome!* This bot is an AI, it learns every day, but is in its infancy now, so be patient.

_(And please don't give personal information 🔐)_
By talking with rDany you are accepting the Terms of Use: /terms

*Say Hi!* - *¡Di Hola!*"""

    terms_text = """*No personal information about yourself or third parties in this chat! Be creative with names, ages, genders, occupations and locations.*

_Using this chatbot you are accepting that the conversation is stored and analyzed; and a version with some details modified (like ages, names and others) shared with third parties for academic or commercial purposes._

*Why the conversation will be shared?*
The goal of this bot is to create a corpus of conversations that will allow to train an AI agent.
To achieve this is necesary to be able to share this information with the scientific community. 🤓
I will do my best to anonymize the conversations.

rDany's Telegram Channel: @rDany
Join the [Telegram Community Group](https://t.me/joinchat/AziBHkCF1gDrrGCY33zeLA)"""


    help_text = """*rDany* is an experimental chatbot capable of holding long and interesting conversations. That means that you just chat with it!

This bot is an AI, it learns every day, but is in its infancy now, so be patient.

*By using this bot you are accepting the Terms of Use:* /terms

rDany's Telegram Channel: @rDany
Join the [Telegram Community Group](https://t.me/joinchat/AziBHkCF1gDrrGCY33zeLA)
⭐️⭐️⭐️⭐️⭐️ [Review rDany bot!](https://t.me/storebot?start=rDanyBot)

[More goodies on Patreon!](https://www.patreon.com/rDanyBot) 🍧"""


    if "message" not in msg:
        return jsonify({})
    answer = {
            'method': "sendMessage",
            'chat_id': msg["message"]["chat"]["id"],
            'text': "*Hi there!*",
            'parse_mode': 'Markdown',
            'disable_web_page_preview': True
    }
    message_text = None
    if "audio" in msg["message"]:
        msg["message"]["text"] = "[audio]"
    elif "document" in msg["message"]:
        msg["message"]["text"] = "[document]"
    elif "game" in msg["message"]:
        msg["message"]["text"] = "[game]"
    elif "photo" in msg["message"]:
        msg["message"]["text"] = "[photo]"
    elif "sticker" in msg["message"]:
        msg["message"]["text"] = "[sticker] {}".format(msg["message"]["sticker"]["emoji"])
    elif "video" in msg["message"]:
        msg["message"]["text"] = "[video]"
    elif "voice" in msg["message"]:
        msg["message"]["text"] = "[voice]"
    elif "contact" in msg["message"]:
        msg["message"]["text"] = "[contact]"
    elif "location" in msg["message"]:
        msg["message"]["text"] = "[location]"
    elif "venue" in msg["message"]:
        msg["message"]["text"] = "[venue]"
    elif "new_chat_member" in msg["message"]:
        return jsonify({})
    elif "left_chat_member" in msg["message"]:
        return jsonify({})
    elif "new_chat_title" in msg["message"]:
        return jsonify({})
    elif "new_chat_photo" in msg["message"]:
        return jsonify({})
    elif "delete_chat_photo" in msg["message"]:
        return jsonify({})
    elif "group_chat_created" in msg["message"]:
        return jsonify({})
    elif "supergroup_chat_created" in msg["message"]:
        return jsonify({})
    elif "channel_chat_created" in msg["message"]:
        return jsonify({})
    elif "migrate_to_chat_id" in msg["message"]:
        return jsonify({})
    elif "migrate_from_chat_id" in msg["message"]:
        return jsonify({})
    elif "pinned_message" in msg["message"]:
        return jsonify({})
    elif "text" in msg["message"] and msg["message"]["chat"]["type"] == "private":
        if msg["message"]["text"].startswith("/start"):
            answer["text"] = welcome_text
            return jsonify(answer)
        elif msg["message"]["text"].startswith("/terms"):
            answer["text"] = terms_text
            return jsonify(answer)
        elif msg["message"]["text"].startswith("/help"):
            answer["text"] = help_text
            return jsonify(answer)
        elif msg["message"]["text"].startswith("/settings"):
            answer["text"] = "*This bot don't have any options. Just talk to it.*"
            return jsonify(answer)
        elif msg["message"]["text"].startswith("/battery"):
            answer["text"] = "*The battery is at full capacity.*"
            return jsonify(answer)
        elif msg["message"]["text"].startswith("/stop"):
            answer["text"] = "*Nothing to stop.*"
            return jsonify(answer)
        elif msg["message"]["text"].startswith("/learn "):
            proposed_answer_text = msg["message"]["text"][7:]
            last_question = query_db("SELECT id,message_text FROM queue WHERE user_id=? ORDER BY id DESC LIMIT 1", [msg["message"]["chat"]["id"]], one=True)
            if not last_question:
                answer["text"] = "*Question not found.*"
                return jsonify(answer)
            msg_id = last_question[0]
            text = last_question[1]
            get_db().execute("UPDATE queue SET proposed_answer_text=? WHERE id=?", [proposed_answer_text, msg_id])
            get_db().commit()
            answer["text"] = "If you say \"{0}\" I will answer \"{1}\"".format(text, proposed_answer_text)
            return jsonify(answer)
    elif "text" in msg["message"]:
        pass
    else:
        msg["message"]["text"] = "[unknown]"
    muted = 0
    if msg["message"]["chat"]["type"] == "private":
        learned_question = query_db("SELECT message_text, proposed_answer_text FROM queue WHERE proposed_answer_text IS NOT NULL AND proposed_answer_text!='' AND user_id = ?", [msg["message"]["chat"]["id"]])
        learned_answer = None
        highest_similarity = 0.8
        for proposed_answer in learned_question:
            similarity = similar(str(proposed_answer[0]).lower(), str(msg["message"]["text"]).lower())
            if similarity > highest_similarity:
                learned_answer = proposed_answer[1]
                highest_similarity = similarity
        if learned_answer:
            answer["text"] = learned_answer
            return jsonify(answer)
        save_message('telegram', msg["message"]["chat"]["id"], msg["message"]["message_id"], msg["message"]["text"])
        return jsonify({})
    elif msg["message"]["chat"]["type"] in ["group", "supergroup"] and "text" in msg["message"]:
        muted = 1
        if msg["message"]["text"].lower().startswith("/dany@rdanybot"):
            msg["message"]["text"] = msg["message"]["text"][15:]
            muted = 0
        elif msg["message"]["text"].lower().startswith("/dany"):
            msg["message"]["text"] = msg["message"]["text"][5:]
            muted = 0
        elif msg["message"]["text"].lower().startswith("dany,"):
            muted = 0
        elif msg["message"]["text"].lower().startswith("rdany,"):
            muted = 0
        elif msg["message"]["text"].lower().endswith(", dany"):
            muted = 0
        elif msg["message"]["text"].lower().endswith(", dany?"):
            muted = 0
        elif msg["message"]["text"].lower().endswith(", rdany"):
            muted = 0
        elif msg["message"]["text"].lower().endswith(", rdany?"):
            muted = 0
        elif msg["message"]["text"].lower().endswith("? dany"):
            muted = 0
        elif msg["message"]["text"].lower().endswith("? rdany"):
            muted = 0
        if "reply_to_message" in msg["message"]:
            if "username" in msg["message"]["reply_to_message"]["from"] and  msg["message"]["reply_to_message"]["from"]["username"].lower() == "rdanybot":
                muted = 0
        save_message('telegram', msg["message"]["chat"]["id"], msg["message"]["message_id"], msg["message"]["text"], group=1, muted=muted)
        return jsonify({})
    elif msg["message"]["chat"]["type"] == "channel":
        return jsonify({})
    return jsonify({})


@main.route('/api', methods=['GET', 'POST'])
def rdany_api():
    msg = request.json

    init_db()
    
    if request.method == 'GET':
        next_question = query_db("SELECT * FROM queue WHERE answered=0 AND muted=0", one=True)
        if not next_question:
            return jsonify({})
        return jsonify({'platform': next_question[1], 'message_text': str(next_question[4]).lower(), 'user_id': next_question[2], 'message_id': next_question[3]})
    elif request.method == 'POST':
        msg = request.json
        msg["message_text"] = msg["message_text"].replace(" ?", "?")
        msg["message_text"] = msg["message_text"].replace(" !", "!")
        msg["message_text"] = msg["message_text"].replace(" .", ".")
        msg["message_text"] = msg["message_text"].replace(" '", "'")
        msg["message_text"] = msg["message_text"].replace("_UNK", "*")
        if msg["platform"] == "telegram":
            send_msg = {
                        'chat_id': msg["user_id"],
                        'text': msg["message_text"],
                    }
            send_request("sendMessage", send_msg)
        elif msg["platform"] == "facebook":
            sendTextMessage(msg["user_id"], msg["message_text"])
        elif msg["platform"] == "kik":
            kik_send(msg["user_id"], msg["message_text"])
        get_db().execute("UPDATE queue SET answered=1, answer_text=? WHERE user_id=? AND message_id=?", [msg["message_text"], msg["user_id"], msg["message_id"]])
        get_db().commit()
        return "ok"


def callSendAPI(messageData):
    headers = {'user-agent': 'rDany', 'Content-Type': 'application/json'}
    page_access_token = app.config["PAGE_ACCESS_TOKEN"]
    r = None
    while 1:
        try:
            r = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(page_access_token), data=json.dumps(messageData), headers=headers)
            break
        except requests.exceptions.ConnectionError:
            raise
            if retry:
                print ("Facebook: ConnectionError")
            else:
                break
        except requests.exceptions.Timeout:
            raise
            if retry:
                print ("Facebook: Timeout")
            else:
                break
        time.sleep(5)
    return r


def sendGenericMessage():
    pass


def sendTextMessage(recipientId, messageText):
    messageData = {
        'recipient': {
          'id': recipientId
        },
        'message': {
          'text': messageText
        }
      }
    with open("Output_out.txt", "w") as text_file:
        print(messageData, file=text_file)
    callSendAPI(messageData)


def receivedMessage(message):
    senderID = message['sender']['id']
    recipientID = message['recipient']['id']
    timeOfMessage = message['timestamp']
    message_ = message['message']
    messageID = message_['mid']
    messageText = message_.get('text')
    messageAttachments = message_.get('attachments')

    with open("Output_in.txt", "w") as text_file:
        print(messageText, file=text_file)

    if messageText:
        message_text = messageText
    elif messageAttachments:
        message_text = "[photo]"

    if message_text == "/start":
        message_text = "[start]"

    save_message('facebook', senderID, messageID, message_text)
    

@main.route('/facebook', methods=['POST', 'GET'])
def facebook():
    print (request.args)
    if request.method == 'GET':
        hub_mode = request.args.get('hub.mode', '')
        hub_verify_token = request.args.get('hub.verify_token', '')
        hub_challenge = request.args.get('hub.challenge', '')
        if hub_mode == 'subscribe' and hub_verify_token == app.config["HUB_VERIFY_TOKEN"]:
            return hub_challenge
        else:
            abort(403)
    elif request.method == 'POST':
        msg = request.json
        if msg['object'] == 'page':
            for entries in msg['entry']:
                for message in entries['messaging']:
                    if "message" in message:
                        receivedMessage(message)
                    else:
                        pass
        return jsonify({})


@main.route('/kik_config', methods=['GET'])
def kik_config():
    requests.post(
        'https://api.kik.com/v1/config',
        auth=('rdanybot', app.config['KIK_TOKEN']),
        headers={
            'Content-Type': 'application/json'
        },
        data=json.dumps({
            'webhook': 'https://rdanybot.rdany.org/kik', 
            'features': {
                'receiveReadReceipts': False, 
                'receiveIsTyping': False, 
                'manuallySendReadReceipts': False, 
                'receiveDeliveryReceipts': False
            }
        })
    )
    return "ok"

@main.route('/kik', methods=['GET', 'POST'])
def kik():
    msg = request.json
    for message in msg["messages"]:
        message_text = ""
        if message["type"] == "text":
            message_text = message["body"]
        elif message["type"] == "link":
            message_text = "[unknown]"
        elif message["type"] == "picture":
            message_text = "[photo]"
        elif message["type"] == "video":
            message_text = "[video]"
        elif message["type"] == "start-chatting":
            message_text = "[start]"
        elif message["type"] == "scan-data":
            message_text = "[start]"
        elif message["type"] == "sticker":
            message_text = "[photo]"
        elif message["type"] == "is-typing":
            continue
        elif message["type"] == "delivery-receipt":
            continue
        elif message["type"] == "read-receipt":
            continue
        elif message["type"] == "friend-picker":
            continue
        save_message('kik', "{0}:{1}".format(message["from"], message["chatId"]), message["id"], message_text)
    return "ok"

def kik_send(chat_id, text):
    to_ = chat_id.split(':')[0]
    chatId = chat_id.split(':')[1]
    requests.post(
        'https://api.kik.com/v1/message',
        auth=('rdanybot', app.config["KIK_TOKEN"]),
        headers={
            'Content-Type': 'application/json'
        },
        data=json.dumps({
            'messages': [
                {
                    'body': text,
                    'to': to_,
                    'type': 'text',
                    'chatId': chatId
                }
            ]
        })
    ) 


@main.route('/simsimi', methods=['GET', 'POST'])
def simsimi():
    keywords = [
        " 10",
        " 11",
        " 12",
        " 13",
        " 14",
        " 15",
        " 16",
        " diez",
        " dies",
        " once",
        " onse",
        " doce",
        " dose",
        " trece",
        " trese",
        " catorce",
        " catorse",
        " quince",
        " quinse",
        " diesiseis",
        " dieciceis",
        " diesiceis",
        " dieciseis"
    ]
    prepend = ""
    append = ""
    msg = request.json
    if "message" not in msg:
        return jsonify({})
    if "text" not in msg["message"]:
        return jsonify({})
    if msg["message"]["text"].lower().startswith("/ssimi"):
        msg["message"]["text"] = msg["message"]["text"][7:]
    elif msg["message"]["text"].lower().startswith("/ssimi@ssimibot"):
        msg["message"]["text"] = msg["message"]["text"][16:]
    answer = {
            'method': "sendMessage",
            'chat_id': msg["message"]["chat"]["id"],
            'text': "*Hi there!*",
            'parse_mode': '',
            'disable_web_page_preview': True
    }
    payload = {'key': app.config['SIMSIMI_TOKEN'], 'lc': 'es', 'text': msg["message"]["text"]}
    if msg["message"]["text"]=="/start":
        answer["text"] = "Si eres menor de 17 años vete, no te quiero aquí, prueba @CatGenBot o algo así. *Digo muchas groserías, miento, y tengo la mente podrida*.\n\nSi las groserías te aburren visita a @rDanyBot , es mas agradable que yo..."
        answer["parse_mode"] = "Markdown"
    else:
        r = requests.get("http://api.simsimi.com/request.p", params=payload)
        if r:
            r_json = r.json()
        if any( k in msg["message"]["text"] for k in keywords ):
            prepend = "Eres menor de 17 años? Vete de aquí!\n"

        if rd.random() > 0.98:
            append = "\nSi te estás divirtiéndo dame 5 estrellas: https://telegram.me/storebot?start=ssimibot o si las groserías te aburren visita a @rDanyBot , es mas agradable que yo..."

        answer["text"] = "{}{}{}".format(prepend, r_json.get("response", ":v"), append)
    save_message('telegram', msg["message"]["chat"]["id"], msg["message"]["message_id"], msg["message"]["text"], "simsimi", answer["text"])
    return jsonify(answer)


@main.route('/rdany_backend', methods=['GET', 'POST'])
def rdany_backend():
    msg = request.json
    if "message" not in msg:
        return jsonify({})
    if "text" not in msg["message"]:
        return jsonify({})
    if msg["message"]["chat"]["id"] != app.config["TELEGRAM_ADMIN_ID"]:
        return jsonify({})
    answer = {
            'method': "sendMessage",
            'chat_id': msg["message"]["chat"]["id"],
            'text': "*Hi there!*",
            'parse_mode': '',
            'disable_web_page_preview': True
    }
    if msg["message"]["text"]=="/next":
        answer["text"] = ""
        next_question = query_db("SELECT id,message_text FROM queue WHERE proposed_answer_text IS NULL LIMIT 1", one=True)
        if not next_question:
            return jsonify({})
        answer["text"] = "ID{0} {1}".format(next_question[0], next_question[1])
    else:
        msg_id = msg["message"]["text"].split(" ")
        if len(msg_id) > 0 and msg_id[0].lower().startswith("id"):
            text = " ".join(msg_id[1:])
            try:
                msg_id = int(msg_id[0][2:])
            except:
                answer["text"] = "Bad Id"
                return jsonify(answer) 
            if text == "":
                answer["text"] = "Empty message not allowed"
            else:
                get_db().execute("UPDATE queue SET proposed_answer_text=? WHERE id=?", [text, msg_id])
                get_db().commit()
                answer["text"] = "Message <{0}> saved on ID {1}".format(text, msg_id)
        else:
            answer["text"] = "unknown"
    
    return jsonify(answer)
