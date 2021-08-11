from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_first_response

my_bot = ChatBot(name = "guanhulk2", read_only=True,
                 logic_adapters=["chatterbot.logic.BestMatch"])

#list_trainer = ListTrainer(my_bot)

#list_trainer.train(small_talk)

print (my_bot.get_response("what time is it now?"))