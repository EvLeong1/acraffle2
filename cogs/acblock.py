import discord 
import config
from discord import app_commands
from discord.ext import commands

import pymongo
import datetime
import random

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

def getColor(rarity):
    if rarity == "common":
        color = discord.Color.default()
    elif rarity == "uncommon":
        color = discord.Color.green()
    elif rarity == "rare":
        color = discord.Color.blue()
    elif rarity == "epic":
        color = discord.Color.purple()
    elif rarity == "legendary":
        color = discord.Color.gold()
    elif rarity == "hyperlegendary":
        color = discord.Color(int('ff9cfc', 16))
    elif rarity == "botColor":
        color = discord.Color.teal()
    elif rarity == "loadingscreen":
        color = discord.Color.orange()
    return color

async def createblock(member):
    data = blockDB.find_one({"id":member.id})
    if data is None:
        newuser = {"id": member.id,"name":member.name}
        blockDB.insert_one(newuser)
        blockDB.update_one({"id":member.id}, {"$set":{"blocklist": [] }})
        return
    else:
        if data["name"] == member.name:
            return
        else:
            blockDB.update_one({"id":member.id}, {"$set":{"name":member.name}})
            return
        
class Buttons(discord.ui.View):
    def __init__(self,author, *, timeout=15):
        self.author = author
        super().__init__(timeout=timeout)
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    async def on_timeout(self) -> None:
        # Step 2
        for item in self.children:
            Buttons.remove_item(self,item)

        # Step 3
        await self.message.edit(view=self)
        
    @discord.ui.button(label="Click Me!", style=discord.ButtonStyle.danger)
    async def click(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked me!")
        
        
class ACBLOCK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("ACBLOCK Cog loaded!")
        
   
        
    @app_commands.command(name='acblock', description='Add a show blocklist - "/acblock view" to view current list')
    async def acblock(self,interaction: discord.Interaction, show: str):
        member = interaction.user
        show = show.lower()
        if show == "view":
            try:
                userBlocks = blockDB.find_one({"id":member.id})
                blocklist = userBlocks['blocklist']
            except:
                em = discord.Embed(title = f"ACblock - {member.name}",description=f"{member.name} currently has no blocked shows",color = discord.Color.teal())
                em.set_thumbnail(url=member.avatar)
                await interaction.response.send_message(embed=em)
                return

            newbl = []
            numb = 0
            for t in blocklist:
                getShow = showDB.find_one({"name":t['show']})
                newbl.append(f'{numb+1}. {getShow["title"]} ({getShow["abv"]})')
                numb+=1
            joinVar = '\n'

            if numb != 0:
                em = discord.Embed (
                title = f"**ACblock - {member.name}\nShows Blocked**:",
                description = f'{joinVar.join(newbl[i] for i in range(0,numb))}',
                colour = getColor('botColor'))
            if numb == 0:
                em = discord.Embed (
                title = f"**ACblock - {member.name}\n{member.name}'s blocklist is currently empty.**",
                colour = getColor('botColor'))

            em.set_thumbnail(url=member.avatar)
            await interaction.response.send_message(embed=em)
            return
        

        try:
            showFound = showDB.find_one({'name':show})
        except:
            showFound = None

        if showFound == None:
            try:
                showFound = showDB.find_one({'abv':show})
            except:
                pass

        if showFound == None:
            em = discord.Embed(title = f"ACblock - {member.name.capitalize()}",description = f"Show '{show}' not found, please you the abbreviations found in */acshows*\nSyntax: **/acblock *show***",color = discord.Color.teal())
            em.set_thumbnail(url=member.avatar)
            await interaction.response.send_message(embed=em)
            return
        
        await createblock(member)

        try:
            userBlocks = blockDB.find_one({"id":member.id})
            blocklist = userBlocks['blocklist']
        except:
            blocklist = []


        blockFound = False
        blcount = 0
        for item in blocklist:
            blcount+=1
            if item == showFound['name']:
                blockFound = True


        if blockFound == True:
            em = discord.Embed(title = f"ACblock - {member.name}",description = f"{showFound['title'].capitalize()} already in your Block List.",color = discord.Color.teal())
            em.set_thumbnail(url=member.avatar)
            await interaction.response.send_message(embed=em)
            return
        elif blcount >= 3:
            em = discord.Embed(title = f"ACblock - {member.name}",description = f"{member.name} already has three blocked shows. Please remove one with **/acblockremove**\nTo view your current blocklist do **/acblock view**",color = discord.Color.teal())
            em.set_thumbnail(url=member.avatar)
            await interaction.response.send_message(embed=em)
            return
        else:
            blockDB.update_one({"id":member.id}, {"$addToSet":{"blocklist":{"show":showFound['name']}}})
            em = discord.Embed(title = f"ACblock - {member.name}",description = f"{showFound['title'].capitalize()} added to your blocklist. To view your current blocklist do **/acblock view**",color = discord.Color.teal())
            em.set_thumbnail(url=member.avatar)
            await interaction.response.send_message(embed=em)
            return
        
            
    @app_commands.command(name='acblockremove', description='Remove a show from your block list')
    async def acblockremove(self,interaction: discord.Interaction, show: str):
     
        member = interaction.user
        show2 = show.lower()

        try:
            showFound = showDB.find_one({'name':show2})
        except:
            showFound = None

        if showFound == None:
            try:
                showFound = showDB.find_one({'abv':show2})
            except:
                pass

        if showFound == None:
            em = discord.Embed(title = f"ACblock - {member.name.capitalize()}",description = f"Show '{show2}' not found, please you the abbreviations found in **/acshows**",color = discord.Color.teal())
            em.set_thumbnail(url=member.avatar)
            await interaction.response.send_message(embed=em)
            return
        
        try:
            userBlocks = blockDB.find_one({"id":member.id})
            blocklist = userBlocks['blocklist']
        except:
            blocklist = []

        blockFound = False

        for item in blocklist:
            if item['show'] == showFound['name']:
                blockFound = True
        
        if blockFound == False:
            em = discord.Embed(title = f"ACblock - {member.name.capitalize()}",description = f"{showFound['title'].capitalize()} not in your blocklist. To view your current blocklist do **/acblock view**",color = discord.Color.teal())
            em.set_thumbnail(url=member.avatar)
            await interaction.response.send_message(embed=em)
            return
        else:
            blockDB.update_one({"id":member.id}, {"$pull":{"blocklist":{"show":showFound['name']}}})
            em = discord.Embed(title = f"ACblock - {member.name.capitalize()}",description = f"{showFound['title'].capitalize()} removed from your blocklist. To view your current blocklist do **/acblock view**",color = discord.Color.teal())
            em.set_thumbnail(url=member.avatar)
            await interaction.response.send_message(embed=em)
            return
  
        
        
        
async def setup(bot):
    await bot.add_cog(ACBLOCK(bot))