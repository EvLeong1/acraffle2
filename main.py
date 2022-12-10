import discord
from discord.ext import commands
#from discord import app_commands

import config
import asyncio
import os
import pymongo
import re

intents = discord.Intents.default()
#intents.message_content = True
bot = commands.Bot(command_prefix= '!', intents=intents, application_id = config.APP_ID)

cluster = pymongo.MongoClient(config.MONGOTOKEN)

charDB = cluster["acrafflebot"]["characters"]
userDB = cluster["acrafflebot"]["users"]
botstatsDB = cluster["acrafflebot"]["botstats"]
showDB = cluster["acrafflebot"]["shows"]
loadingScreenDB = cluster["acrafflebot"]["loadingscreens"]
shopDB = cluster["acrafflebot"]["usershops"]
voteDB = cluster["acrafflebot"]["uservotes"]
blockDB = cluster["acrafflebot"]["blocks"]
presDB = cluster["acrafflebot"]["userprestige"]
achDB = cluster["acrafflebot"]["achievements"]
sznDB = cluster["acrafflebot"]["seasons"]
sznWinDB = cluster["acrafflebot"]["sznwinners"] 

async def createvoter(member):
    data = voteDB.find_one({"id":member.id})
    if data is None:
        newuser = {"id": member.id,"name":member.name,"credits":0}
        voteDB.insert_one(newuser)
        return
    else:
        if data["name"] == member.name:
            return
        else:
            voteDB.update_one({"id":member.id}, {"$set":{"name":member.name}})
            return

@bot.event
async def on_message(msg):
    if msg.channel.id == 892219168156430336:
        
        data = msg.content.split(" ")

        user = re.sub("\D", "", data[0])
        member = bot.get_user(int(user))
        await createvoter(member)

        voteDB.update_one({"id":member.id}, {"$inc":{"credits":1}})
        achDB.update_one({"id":member.id}, {"$inc":{"votes":1}})

    await bot.process_commands(msg)
    
@bot.event
async def on_ready():
    #await bot.tree.sync()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/achelp"))
    print('Bot Online!')

    
async def load():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')

#Runs the Bot
async def main():
    await load()
    await bot.start(config.TOKEN)
    
asyncio.run(main())