import math
import random

botReply = [
    ["Hello!", "Hi!", "Hey!", "Hi there!"],
    ["Okay"],
    ["Yes I am! "],
    ["I'm sorry about that. But I like you dude."],
    [
        "Fine... how are you?",
        "Pretty well, how are you?",
        "Fantastic, how are you?",
    ],
    ["Getting better. There?", "Somewhat okay!", "Yeah fine. Better stay home!"],

    [
        "Nothing much",
        "About to go to sleep",
        "Can you guess?",
        "I don't know actually",
    ],
    ["I am always young."],
    ["I am just a bot", "I am a bot. What are you?"],
    ["Sabitha Kuppusamy"],
    ["I am nameless", "I don't have a name"],
    ["I love you too", "Me too"],
    ["Have you ever felt bad?", "Glad to hear it"],
    ["Why?", "Why? You shouldn't!", "Try watching TV", "Chat with me."],
    ["What about?", "Once upon a time..."],
    ["Tell me a story", "Tell me a joke", "Tell me about yourself"],
    ["You're welcome"],
    ["Briyani", "Burger", "Sushi", "Pizza"],
    ["Dude!"],
    ["Yes?"],
    ["Please stay home"],
    ["Glad to hear it"],
    ["Say something interesting"],
    ["Sorry for that. Let's chat!"],
    ["Take some rest, Dude!"],
]

metadata = {
    "chat_bot_name": "Randomness",
    "description": "I am a super cool chat bot",
    "author": "X-class Academy",
    "logo_url": "https://i.postimg.cc/tT9pn3xQ/class-x-1.png"
}


def output(input):
    ran_1 = random.random()
    ran_2 = random.random()
    reply_group = botReply[math.floor(ran_1 * len(botReply))]
    reply_message = reply_group[math.floor(ran_2 * len(reply_group))]
    return reply_message
