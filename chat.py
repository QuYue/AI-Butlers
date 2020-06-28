# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 14:27:13 2020

@author: QuYue
"""
"""


chatbot = ChatBot('Obvious')

# Create a new trainer for the chatbot


# Train the chatbot based on the english corpus
trainer.train("chatterbot.corpus.chinese")
trainer.train("chatterbot.corpus.english")

# Get a response to an input statement

#chatbot.get_response("Hello, how are you today?")


def reply_my_friend(msg):
   print(msg)
   return bot0.get_response(msg.text).text# 使用机器人进行自动回复

print(reply_my_friend('aaa'))
"""
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from chatterbot import ChatBot
bot = ChatBot(
    'Sakura',
)
trainer = ChatterBotCorpusTrainer(bot)

trainer.train("chatterbot.corpus.chinese")
trainer.train("chatterbot.corpus.english")
trainer2 = ListTrainer(bot)

trainer2.train([
    "今天天气怎么样","还不错"
])



print(bot.get_response("天气1"))
