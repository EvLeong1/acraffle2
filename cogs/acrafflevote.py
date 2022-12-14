import discord 
import config
from discord import app_commands
from discord.ext import commands
import pymongo
import os
from pymongo import MongoClient
import asyncio

import datetime
import random


# client = pymongo.MongoClient("mongodb+srv://evanL:EvLardbag573@cluster0.ym2yg.mongodb.net/?retryWrites=true&w=majority")
# acrdb = client.acrafflebot

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

logChannelID = 865757247933251584
banklogChannelID = 873120153498423366
cooldownChannelID = 876653890605563904
previewChannelID = 876654247423385630
newUserChannelID = 876658814269661185
shopChannelID = 879180765726912593
profileChannelID = 881954966103801856
loadingCannelID = 884247812936699905
presChannelID = 919091316401528834
wagerChannelID = 949486966930559066

def setRandTime():
    randseed = random.randint(1,1000)
    random.seed(randseed)
    randTime = random.randint(14400,21600)
    return randTime

acrpRarities = ["rare","epic","legendary"]
acrpChance = [66,30,4]

#chance =[100,0,0,0,0] #for testing
#chance=[0,0,0,0,100] #for testing

def addfunds(member,amount):
    user = shopDB.find_one({"id":member.id})
    shopDB.update_one({"id":member.id}, {"$inc":{"money":amount}})

    if user["money"] >= 100000:
        shopDB.update_one({"id":member.id}, {"$set":{"money":100000}})
        return

def addfundsdupe(member,rarity):
    user = shopDB.find_one({"id":member.id})
    if rarity == "common":
        amount = 150
    if rarity == "uncommon":
        amount = 250
    if rarity == "rare":
        amount = 500
    if rarity == "epic":
        amount = 1500
    if rarity == "legendary":
        amount = 5000

    shopDB.update_one({"id":member.id}, {"$inc":{"money":amount}})
    if user["money"] >= 100000:
        shopDB.update_one({"id":member.id}, {"$set":{"money":100000}})
        return

def getpricedupe(rarity):
    if rarity == "common":
        amount = 50
    if rarity == "uncommon":
        amount = 100
    if rarity == "rare":
        amount = 200
    if rarity == "epic":
        amount = 750
    if rarity == "legendary":
        amount = 3000
    return amount

def updateCharsAmount(member):
        user = userDB.find_one({"id":member.id})
        userchars = len(user["characters"])
        userDB.update_one({"id":user["id"]}, {"$set":{"charsunlocked":userchars}})
        
def updateLegendaryandEpic(member):
        user = userDB.find_one({"id":member.id})
        Leg=0
        Ep=0
        for x in user["characters"]:
            if x["rarity"] == "legendary":
                Leg+=1
            if x["rarity"] == "epic":
                Ep+=1
                
        userDB.update_one({"id":member.id}, {"$set":{"legendsunlocked":Leg}})
        userDB.update_one({"id":member.id}, {"$set":{"legunlocked":Ep}})

def checkDupes(member,name):
        duplicate = "New"
        user = userDB.find_one({"id":member.id})
        try:
            userchars = user["characters"]
        except:
            return duplicate
        for x in userchars:
            if x["name"] == name:
                duplicate = "Duplicate"
                break
        return duplicate
    
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
    
def addfundspres(member,level):
    botStats = botstatsDB.find_one({"id":573})
    sznDB.update_one({"id":member.id}, {"$inc":{"xp":3 * level}})
    shopDB.update_one({"id":member.id}, {"$inc":{"money":level*botStats['presBonus']}})
    

        

async def send_logs_newuser(self, member, server):
    channel = await self.bot.get_channel(newUserChannelID)
    try:
        await channel.send(f'**New User!** - User: **{member.name}** - Server: **{server.name}**')
    except:
        pass
    return

async def createuser(member,guild):
        data = userDB.find_one({"id":member.id})
        if data is None:
            # guildid = guild.id
            # guildname = guild.name
            newuser = {"id": member.id,"name":member.name,"currentchar":None}
            userDB.insert_one(newuser)
            userDB.update_one({"id":member.id}, {"$set":{"favorites": [] }})
        
            # await addUniqueUser()
            return
        else:
            if data["name"] == member.name:
                return
            else:
                userDB.update_one({"id":member.id}, {"$set":{"name":member.name}})
                return
        
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

async def createpres(member):
    data = presDB.find_one({"id":member.id})
    if data is None:
        newuser = {"id": member.id,"name":member.name}
        presDB.insert_one(newuser)
        presDB.update_one({"id":member.id}, {"$set":{"shows":[]}})
        presDB.update_one({"id":member.id}, {"$set":{"dates":[]}})
        presDB.update_one({"id":member.id}, {"$set":{"totPres":0}})
        return
    else:
        if data["name"] == member.name:
            return
        else:
            presDB.update_one({"id":member.id}, {"$set":{"name":member.name}})
            return

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

async def createshopuser(member,guild):
    data = shopDB.find_one({"id":member.id})
    if data is None:
        newuser = {"id": member.id,"name":member.name,'money':0}
        shopDB.insert_one(newuser)
        shopDB.update_one({"id":member.id}, {"$set":{"characterShop": [] }})
        try:
            oldProf = userDB.find_one({'id':member.id})
            try:
                shopDB.update_one({"id":member.id}, {"$set":{"money": oldProf['money']}})
                userDB.update_one({"id":member.id}, {"$unset":{"money":""}})
            except:
                pass
            try:
                userDB.update_one({"id":member.id}, {"$unset":{"characterShop":""}})
            except:
                pass
            try:
                userDB.update_one({"id":member.id}, {"$unset":{"boughtuncommon":""}})
                userDB.update_one({"id":member.id}, {"$unset":{"boughtrare":""}})
                userDB.update_one({"id":member.id}, {"$unset":{"boughtepic":""}})
                userDB.update_one({"id":member.id}, {"$unset":{"boughtlegendary":""}})
                userDB.update_one({"id":member.id}, {"$unset":{"boughtloading":""}})
            except:
                pass
            try:
                userDB.update_one({"id":member.id}, {"$unset":{"month":""}})
                userDB.update_one({"id":member.id}, {"$unset":{"tomorrow":""}})
            except:
                pass
                
        except:
            pass

        return
    else:
        if data["name"] == member.name:
            return
        else:
            shopDB.update_one({"id":member.id}, {"$set":{"name":member.name}})
            return

async def createsznuser(member):
    data = sznDB.find_one({"id":member.id})
    if data is None:
        newuser = {"id": member.id,"name":member.name,"xp":0}
        sznDB.insert_one(newuser)
        return
    else:
        if data["name"] == member.name:
            return
        else:
            sznDB.update_one({"id":member.id}, {"$set":{"name":member.name}})
            return

async def createsznWinuser(member):
    data = sznWinDB.find_one({"id":member.id})
    if data is None:
        newuser = {"id": member.id,"name":member.name}
        sznWinDB.insert_one(newuser)
        sznWinDB.update_one({"id":member.id}, {"$set":{"prevSeasons":[]}})
        return
    else:
        if data["name"] == member.name:
            return
        else:
            sznWinDB.update_one({"id":member.id}, {"$set":{"name":member.name}})
            return

async def createachuser(member):
    data = achDB.find_one({"id":member.id})
    if data is None:
        newuser = {"id": member.id,"name":member.name,"votes":0, "trades":0}
        achDB.insert_one(newuser)
        return
    else:
        if data["name"] == member.name:
            return
        else:
            achDB.update_one({"id":member.id}, {"$set":{"name":member.name}})
            return
        
        
class yesRaffle(discord.ui.View):
    def __init__(self,author,bot, *, timeout=10):
        self.author = author
        self.bot = bot
        super().__init__(timeout=timeout)
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    async def on_timeout(self) -> None:
        # Step 2
        for item in self.children:
            yesRaffle.remove_item(self,item)

        # Step 3
        await self.message.edit(view=self)
        
    @discord.ui.button(label="Raffle Once", style=discord.ButtonStyle.green)
    async def raffleVote(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        for child in self.children:
            yesRaffle.remove_item(self,child)
        await interaction.edit_original_response(view=self)
        member = interaction.user
        voteDB.update_one({"id":member.id}, {"$inc":{"credits":-1}})
        result = random.choices(acrpRarities,acrpChance,k=1)
        user = userDB.find_one({"id":member.id})
        botStats = botstatsDB.find_one({"id":573})

        newuser = True
        try:
            userChars = user["characters"]
            newuser = False
        except:
            pass
        
        duperate = int(botStats["duperate"])
        for x in range(len(acrpRarities)):
            if result[0] == acrpRarities[x]:
                #print(rarities[x])
                max = charDB.count_documents({"rarity":acrpRarities[x]})
                randomInt = random.randint(1,max) 
                Char = charDB.find_one({"rarity":acrpRarities[x], "raritynumber": randomInt})
                try:
                    ublocks = blockDB.find_one({'id':member.id})
                    blist = ublocks['blocklist']
                    newblist = []
                    for itm in blist:
                        newblist.append(itm['show'])
                except:
                    newblist=[]
                if acrpRarities[x] == 'legendary':
                    while checkDupes(member,Char["name"]) == "Duplicate":
                        if checkDupes(member,Char["name"]) == "Duplicate":
                            random.seed(random.randint(1,5000000))
                            randomInt = random.randint(1,max) 
                            Char = charDB.find_one({"rarity":acrpRarities[x], "raritynumber": randomInt})
                        if Char['show'] in newblist:
                            random.seed(random.randint(1,5000000))
                            randomInt = random.randint(1,max) 
                            Char = charDB.find_one({"rarity":acrpRarities[x], "raritynumber": randomInt})
                else:
                    for y in range(duperate):
                        if checkDupes(member,Char["name"]) == "Duplicate":
                            random.seed(random.randint(1,5000000))
                            randomInt = random.randint(1,max) 
                            Char = charDB.find_one({"rarity":acrpRarities[x], "raritynumber": randomInt})
                        if Char['show'] in newblist:
                            random.seed(random.randint(1,5000000))
                            randomInt = random.randint(1,max) 
                            Char = charDB.find_one({"rarity":acrpRarities[x], "raritynumber": randomInt})
                        else:
                            break


                showFound = showDB.find_one({"name":Char["show"]})

                isDupe = checkDupes(member,Char["name"])

                oldChar = Char
                if isDupe == "Duplicate":
                    charlist = charDB.find({'show':showFound['name'],'rarity':Char['rarity']})
                    for x in charlist:
                        if isDupe == "Duplicate":
                            Char = charDB.find_one({"name":x['name']})
                            isDupe = checkDupes(member,Char["name"])
                        else:
                            break
                        
                
                if isDupe == "Duplicate":
                    Char = oldChar

                pres = presDB.find_one({'id':member.id})
                level = 0
                if pres != None:
                    pshows = pres['shows']
                    for shw in pshows:
                        if Char['show'] == shw['show']:
                            level = shw['tier']

                # await outputEmbed(Char["name"],Char["rarity"],showFound["title"],Char["gif"],getColor(Char["rarity"]), isDupe,level)
                # try:
                #     await send_logs_acraffle_more(member, guild, "acrafflevote",Char["name"], isDupe,Char["rarity"])
                # except:
                #     # await send_logs_error(member,"acr worked but dont have manage permissions")
                #     pass
                addfunds(member,botStats["amountacrp"])
                userDB.update_one({"id":member.id}, {"$addToSet":{"characters":{"name":Char["name"],"show":Char["show"],"rarity":Char["rarity"]}}})
                updateLegendaryandEpic(member)
                updateCharsAmount(member)

                if isDupe == "Duplicate" and level == 0:    #duplicate no pres  
                    addfundsdupe(member, Char['rarity'])
                elif isDupe == "Duplicate" and level != 0:  #duplicate and pres
                    addfundspres(member,level)
                    addfundsdupe(member, Char['rarity'])
                elif isDupe != "Duplicate" and level != 0:  #new and pres
                    addfundspres(member,level)
                    addfundsdupe(member, Char['rarity'])

                # sznDB.update_one({"id":member.id}, {"$inc":{"xp":10}})
                
                if newuser == True:
                    em = discord.Embed(title = f"ACrafflevote - {member.name} got {Char['name'].capitalize()}",color = getColor(Char['rarity']))
                    em.add_field(name=f"**Details**",value=f"Show: **{showFound['title']}**\nRarity: **{Char['rarity'].capitalize()}**\n**{isDupe}**")
                    if isDupe == "Duplicate" and level == 0:
                        em.add_field(name=f"**Money**",value=f"${botStats['amountacrp']} for raffling\n${getpricedupe(Char['rarity'])} for duplicate")
                    elif isDupe == "Duplicate" and level != 0:
                        em.add_field(name=f"**Money**",value=f"${botStats['amountacrp']} for raffling\n${botStats['presBonus']*level + getpricedupe(Char['rarity'])} Prestige Bonus")
                    elif isDupe != "Duplicate" and level != 0:
                        em.add_field(name=f"**Money**",value=f"${botStats['amountacrp']} for raffling\n${botStats['presBonus']*level + getpricedupe(Char['rarity'])} Prestige Bonus")
                    else:
                        em.add_field(name=f"**Money**",value=f"${botStats['amountacrp']} for raffling")
                    em.add_field(name=f"**Thanks for using ACraffle!**",value=f"If you are new and want to get started use **/actutorial**",inline=False)
                    em.set_image(url=Char['gif'])
                    em.set_thumbnail(url = member.avatar)
                    acraffleNote = botStats["acraffleNote"]
                    em.set_footer(text=f"{acraffleNote} - See /acan")
                    
                    
                else:
                    em = discord.Embed(title = f"ACrafflevote - {member.name} got {Char['name'].capitalize()}",color = getColor(Char['rarity']))
                    em.add_field(name=f"**Details**",value=f"Show: **{showFound['title']}**\nRarity: **{Char['rarity'].capitalize()}**\n**{isDupe}**")
                    if isDupe == "Duplicate" and level == 0:
                        em.add_field(name=f"**Money**",value=f"${botStats['amountacrp']} for raffling\n${getpricedupe(Char['rarity'])} for duplicate")
                    elif isDupe == "Duplicate" and level != 0:
                        em.add_field(name=f"**Money**",value=f"${botStats['amountacrp']} for raffling\n${botStats['presBonus']*level + getpricedupe(Char['rarity'])} Prestige Bonus")
                    elif isDupe != "Duplicate" and level != 0:
                        em.add_field(name=f"**Money**",value=f"${botStats['amountacrp']} for raffling\n${botStats['presBonus']*level + getpricedupe(Char['rarity'])} Prestige Bonus")
                    else:
                        em.add_field(name=f"**Money**",value=f"${botStats['amountacrp']} for raffling")
                    em.set_image(url=Char['gif'])
                    em.set_thumbnail(url = member.avatar)
                    acraffleNote = botStats["acraffleNote"]
                    em.set_footer(text=f"{acraffleNote} - See /acan")
                
                # print('ham')
                    
                chl = self.bot.get_channel(config.ACR_LOG_ID)
                    
                await chl.send(f"**/acrafflevote** - User: **{interaction.user.name}** - Server: **{interaction.guild}** - Character: **{Char['name']}** - Show: {Char['show']} - Rarity: {Char['rarity']}")
                await interaction.edit_original_response(embed=em)
                    

                
    
    @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            yesRaffle.remove_item(self,child)
    
        view = yesRaffle(interaction.user,self.bot)
        await interaction.response.edit_message(view=self)
        view.message = await interaction.original_response()
        

                   
        
class ACRVOTE(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("ACRVOTE Cog loaded!")
        
    #Test Command
    @app_commands.command(name="acrv",description="Acrafflevote - Roll for a Rare, Epic, or Legendary character! - Uses one vote credit from /acvote")
    @app_commands.checks.cooldown(1,10,key=lambda i: (i.user.id))
    async def acrv(self,interaction: discord.Interaction):
        member = interaction.user
        guild= interaction.guild
        botStats=botstatsDB.find_one({'id':573})
        if botStats['botOffline']==True:
            em = discord.Embed(title = f"ACrafflevote - {member.name}\nThe bot is rebooting...\nTry again in a few minutes.",color = getColor('botColor'))
            em.set_thumbnail(url = member.avatar)
            await interaction.response.send_message(embed=em)
            return
        await createvoter(member)
        await createuser(member, guild)
        await createshopuser(member,guild)
        await createsznuser(member)
        await createsznWinuser(member)

        userProf = voteDB.find_one({'id':member.id})
        creds = userProf['credits']
        
        if creds > 0:
            em = discord.Embed(title = f"ACrafflevote - {member.name}",description = f"**Vote Credits: {creds}**\n(You can raffle {creds} times!)\nTo get vote credits do **/acvote**",color = discord.Color.teal())
            em.set_thumbnail(url = member.avatar)


            user = userDB.find_one({"id":member.id})

            try:
                if user['lstype'] == "Select":
                    loadingscreen = user['currentloadingscreen']
                    em.set_image(url = loadingscreen)
                    
                elif user['lstype'] == "Random":
                    screenList = []
                    screens = user['loadingscreens']
                    it =0
                    for var in screens:
                        it+=1
                        screenList.append(int(var['number']))
                    it = it-1
                    randScreen = random.randint(0,it)
                    screenFound = loadingScreenDB.find_one({'number':screenList[randScreen]})
                    em.set_image(url = screenFound['gif'])
                    
            except:
                pass    
            
            
            view = yesRaffle(interaction.user,self.bot)
            await interaction.response.send_message(embed=em, view=view)
            view.message = await interaction.original_response()
            
        else:
            em = discord.Embed(title = f"ACrafflevote - {member.name}",description = f"**Vote Credits: {creds}**\n(You can raffle {creds} times!)\nTo get vote credits do **/acvote**",color = discord.Color.teal())
            em.set_thumbnail(url = member.avatar)

            user = userDB.find_one({"id":member.id})

            try:
                if user['lstype'] == "Select":
                    loadingscreen = user['currentloadingscreen']
                    em.set_image(url = loadingscreen)
                    
                elif user['lstype'] == "Random":
                    screenList = []
                    screens = user['loadingscreens']
                    it =0
                    for var in screens:
                        it+=1
                        screenList.append(int(var['number']))
                    it = it-1
                    randScreen = random.randint(0,it)
                    screenFound = loadingScreenDB.find_one({'number':screenList[randScreen]})
                    em.set_image(url = screenFound['gif'])
                    
            except:
                pass    
            
            
            await interaction.response.send_message(embed=em)
            return
          

       
            
        
        
async def setup(bot):
    await bot.add_cog(ACRVOTE(bot))
    