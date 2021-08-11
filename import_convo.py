import json

with open("chat_history.json", "r", encoding="utf8") as read_file:
    data  = json.load (read_file)

lst = []
texts = data["messages"]
for text in texts:
    lst.append(text["text"])

