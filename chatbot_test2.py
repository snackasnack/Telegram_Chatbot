from chatterbot import ChatBot
from chatterbot.storage import SQLStorageAdapter
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_first_response
from chatterbot.response_selection import get_random_response

import json
import requests
import time
import urllib


#corpus_trainer = ChatterBotCorpusTrainer(my_bot)
#corpus_trainer.train ('chatterbot.corpus.english')z

TOKEN = "****"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def extract_convo ():
    with open("chat_history.json", "r", encoding="utf8") as read_file:
        data  = json.load (read_file)

    lst = []
    texts = data["messages"]
    for text in texts:
        lst.append(str(text["text"]))

    return lst

def train_bot (texts,bot_name):
    list_trainer = ListTrainer(bot_name)
    list_trainer.train(texts)

def feed_data (bot_name):
    print ("Enter a sentence to get started!")
    lst = []
    while True:
        prompt = input()
        if prompt == "quit":
            train_bot(lst, bot_name)
            break
        elif prompt == "save":
            train_bot(lst,bot_name)
            continue
        else:
            lst.append(prompt)

def handle_updates(updates,bot_name):
    lst = []
    try:
        for update in updates["result"]:
            user_text = update["message"]["text"]
            #print("user text done")
            chat = update["message"]["chat"]["id"]
            name = update["message"]["chat"]["username"]
            #print("chatid: {} done".format(chat)
            reply = bot_name.get_response(user_text)
            #print("reply done")
            send_message(str(reply), chat)
            #print("send message done")
            if name in lst:
                continue
            else:
                lst.append(name)
            print (lst)
    except Exception as e:
        print (e)

def sidetrack():
    my_bot = ChatBot(name = "guanhulk2", read_only=True,
                     logic_adapters=["chatterbot.logic.BestMatch",
                                     "chatterbot.logic.TimeLogicAdapter"],
                     response_selection_method = get_random_response)

    feed_data(my_bot)

def main():
    my_bot = ChatBot(name = "guanhulk2", read_only=True,
                     logic_adapters=["chatterbot.logic.BestMatch",
                                     "chatterbot.logic.TimeLogicAdapter"],
                     response_selection_method = get_random_response)

    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            time.sleep(0.8)
            handle_updates(updates,my_bot)
        time.sleep(0.5)

    #print ("original:",my_bot.get_response("hi"))

    #handle_updates()
    #while True:
    #    user_text = input ()
    #    print (my_bot.get_response(user_text))

if __name__ == "__main__":
    main()
    #sidetrack()

