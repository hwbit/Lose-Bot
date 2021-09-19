import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


botKey = os.environ['TOKEN']
client = discord.Client()


dad_trigger = ["dad joke", "bad pun"]

starter_dad_jokes = ["Thanks for teaching me of the word many. It means a lot.", 
        "You know when a joke is a dad joke? It's a parent.", 
        "What do you call a pile of cats? A meowtain", 
        "How do you count cows? With a cowculator"]

if "responding" not in db.keys():
  db["responding"] = True

#call dad joke api
def get_dadjoke():
  response = requests.get("https://icanhazdadjoke.com", headers={"Accept":"application/json"})
  json_data = response.json()
  quote = json_data['joke'] + " (" + json_data['id'] +")"
  return(quote)

def update_dadjoke(dad_joke_message):
  if "dad_jokes" in db.keys():
    dad_jokes = db["dad_jokes"]
    dad_jokes.append(dad_joke_message)
    db["dad_jokes"] = dad_jokes
  else:
    db["dad_jokes"] = [dad_joke_message]

def delete_dadjoke(index):
  dad_jokes = db["dad_jokes"]
  if len(dad_jokes) > index:
    del dad_jokes[index]
    db["dad_jokes"] = dad_jokes

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  
  if msg.startswith('$hello'):
    await message.channel.send('Hello!')

  # get random joke
  if msg.startswith('$dadjoke'):
    quote = get_dadjoke()
    await message.channel.send(quote)

  # checks if the bot is responding to words
  if db["responding"]:
    options = starter_dad_jokes
    if "dad_jokes" in db.keys():
      options = options + list(db["dad_jokes"])

    if any(word in msg for word in dad_trigger):
      await message.channel.send(random.choice(options))

  # add joke
  if msg.startswith("$add-dadjoke"):
    dad_joke_add = msg.split("$add-dadjoke ", 1)[1]
    update_dadjoke(dad_joke_add)
    await message.channel.send("Added dad joke.")

  # delete joke - returns the joke
  if msg.startswith("$del-dadjoke"):
    dad_jokes = []
    if "dad_jokes" in db.keys():
      index = int(msg.split("$del-dadjoke", 1)[1])
      deleted_joke = db["dad_jokes"][index]
      delete_dadjoke(index)
      dad_jokes = db["dad_jokes"]
    await message.channel.send(deleted_joke)

  # list dad jokes
  if msg.startswith("$list-dadjoke"):
    dad_jokes = []
    if "dad_jokes" in db.keys():
      dad_jokes = db["dad_jokes"]
      list_jokes = ""
      for joke in dad_jokes:
        list_jokes += "[\"" + joke + "\"] "
    await message.channel.send(list_jokes)

  if msg.startswith("$responding"):
    value = msg.split("$responding ", 1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off")

keep_alive()
client.run(botKey)