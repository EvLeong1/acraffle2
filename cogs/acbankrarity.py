import discord 
from discord import app_commands
from discord.ext import commands
import pymongo
import config 
import math

#ACshows and AC Hyper Legendary
acshowsPages = []

class Buttons(discord.ui.View):
    showit = 0
    def __init__(self,author,acbrT,acbrE,bankraritypages, *, timeout=30):
        self.author = author
        self.acbrT = acbrT
        self.acbrE = acbrE
        self.bankraritypages = bankraritypages
        super().__init__(timeout=timeout)
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    async def on_timeout(self) -> None:
        # Step 2
        for item in self.children:
            Buttons.remove_item(self,item)

        # Step 3
        await self.message.edit(view=self)
        
    @discord.ui.button(label="Prev", style=discord.ButtonStyle.blurple)
    async def prev(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.acbrT > 0:
            self.acbrT -= 1
        #print(Buttons.showit)
        view = Buttons(interaction.user,self.acbrT,self.acbrE,self.bankraritypages)
        await interaction.response.edit_message(embed=self.bankraritypages[self.acbrT],view=view)
        view.message = await interaction.original_response()
        
    @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.acbrT < self.acbrE-1:
            self.acbrT += 1
        #print((Buttons.showit))
        view = Buttons(interaction.user,self.acbrT,self.acbrE,self.bankraritypages)
        await interaction.response.edit_message(embed=self.bankraritypages[self.acbrT],view=view)
        view.message = await interaction.original_response()
        
    @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
    async def Close(self, interaction: discord.Interaction, child: discord.ui.Button):
        for child in self.children:
            Buttons.remove_item(self,child)
    
        await interaction.response.edit_message(view=self)
        
        
        
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

def updateHyperLeg(member):
    user = userDB.find_one({"id":member.id})
    HypLeg = 0
    for x in user["characters"]:
        if x["rarity"] == "hyperlegendary":
            HypLeg+=1
            
    userDB.update_one({"id":member.id}, {"$set":{"hypersunlocked":HypLeg}})
        
        
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

# def createPages(member):   
#     numshows = showDB.count_documents({})
#     pagesNeeded = math.ceil(numshows/15)
#     #print(pagesNeeded)

#     showlist = showDB.find().sort('title')
#     newShowsList = []
#     numInList = 1
#     for t in showlist:
#         newShowsList.append(f'{numInList}. {t["title"]} ({t["abv"]})')
#         numInList+=1
#     joinVar = '\n'

#     #print(newShowsList)
    
#     startNum = 0
#     stopNum = 15

#     for pages in range(pagesNeeded):
#         embed = discord.Embed (
#         title = f"**ACshows - User: {member.name}\nTo see the characters in a show do /acbs show\nExample: /acbs aot**",
#         description = f'{joinVar.join(newShowsList[i] for i in range(startNum,stopNum))}',
#         colour = getColor('botColor')
#         )
#         embed.set_thumbnail(url=member.avatar)
#         embed.set_footer(text=f'Page: ({pages+1}/{pagesNeeded})')
#         acshowsPages.append(embed)
#         startNum+=15
#         stopNum+=15
#         if stopNum >= numshows:
#             stopNum = numshows
#     return acshowsPages
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
            
             
class ACBR(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("ACBR Cog loaded!")
        
    
    @app_commands.command(name="acbr",description="ACbankrarity - Shows all unlocked characters for a specified rarity")
    @app_commands.choices(rarity=[
        discord.app_commands.Choice(name='Common',value=1),
        discord.app_commands.Choice(name='Uncommon',value=2),
        discord.app_commands.Choice(name='Rare',value=3),
        discord.app_commands.Choice(name='Epic',value=4),
        discord.app_commands.Choice(name='Legendary ',value=5),
        discord.app_commands.Choice(name='Hyper Legendary ',value=6)
    ])
    async def acbr(self,interaction: discord.Interaction,rarity: discord.app_commands.Choice[int], user: discord.User):
        member = user
        guild = interaction.guild
        botStats = botstatsDB.find_one({"id":573})
       
        if botStats['botOffline']==True:
            em = discord.Embed(title = f"ACsetfavorite - {member.name}\nThe bot is rebooting...\nTry again in a few minutes.",color = getColor('botColor'))
            em.set_thumbnail(url = member.avatar)
            await interaction.response.send_message(embed=em) 
            return
    
        
        
        
        await createuser(member,guild)
        membername = member.name
        
        user = userDB.find_one({"id":member.id})
        
        try:
            userChars = user["characters"]
        except:
            em = discord.Embed(title = f"{member.name} hasn't unlocked any characters!\nDo */acraffle* to get started!",color = discord.Color.teal())
            em.set_thumbnail(url=member.avatar)
            await interaction.response.send_message(embed=em) 
            return


        # embed = discord.Embed(title = f"ACbankrarity - {member.name}\nLoading...",color = discord.Color.teal())
        # embed.set_thumbnail(url=member.avatar)
        # await interaction.response.send_message(embed=em) 
        if rarity.value == 1:
            userRarity = "common"
        if rarity.value == 2:
            userRarity = "uncommon"
        if rarity.value == 3:
            userRarity = "rare"
        if rarity.value == 4:
            userRarity = "epic"
        if rarity.value == 5:
            userRarity = "legendary"
        if rarity.value == 6:
            userRarity = "hyperlegendary"
        
        
        acbrI=0
        acbrO=0
        acbrJ=18
        acbrE=1
        charlist = charDB.find().sort("show")
        for x in userChars:
            if x["rarity"] == userRarity:
                acbrI+=1

        for xx in charlist:
            if xx["rarity"] == userRarity:
                acbrO+=1
                if acbrO > acbrJ:
                    acbrJ+=18
                    acbrE+=1
        

        bankraritypages = []
        for acbrX in range(acbrE):
            embed = discord.Embed (
            title = f"ACbankrarity\nUser: {interaction.user.name} - Viewing: {membername}\nPage: ({acbrX+1}/{acbrE})",
            description = f"**{userRarity.capitalize()} characters unlocked: {acbrI}**",
            colour = getColor(userRarity)
            )
            embed.set_footer(text=f'{userRarity.capitalize()} characters unlocked: {acbrI} - Page: ({acbrX+1}/{acbrE})')
            bankraritypages.append(embed)
            
        
        def addfield(page,tempname,show):
            page.add_field(name=f"✅ **{tempname.capitalize()}**",value=f"{show}", inline=True)

        def addfield2(page,tempname,show):
            page.add_field(name=f"❌ **{tempname.capitalize()}**",value=f"{show}", inline=True)

        def setThumbnail(page):
            page.set_thumbnail(url=member.avatar)

        acbrF = 0
        acbrG = 18
        acbrnewnamelist = []
        
        for acbrZ in userChars:
            if acbrZ["rarity"] == userRarity:
                acbrnewnamelist.append(acbrZ["name"])

        charlist = charDB.find().sort("show")
        showlist = showDB.find()
    
        for acbrY in range(acbrE):
            setThumbnail(bankraritypages[acbrY])
            for z in charlist:
                if z["name"] in acbrnewnamelist:
                    # showFound = showDB.find_one({'name':z['show']})
                    acbrF+=1
                    # addfield(bankraritypages[acbrY],z["name"],showFound['abv'])
                    addfield(bankraritypages[acbrY],z["name"],z['abv'])
                    if acbrF == acbrG:
                        acbrG+=18
                        break
                elif z['name'] not in acbrnewnamelist and z['rarity'] == userRarity:
                    # showFound = showDB.find_one({'name':z['show']})
                    acbrF+=1
                    # addfield2(bankraritypages[acbrY],z["name"],showFound['abv'])
                    addfield2(bankraritypages[acbrY],z["name"],z['abv'])
                    if acbrF == acbrG:
                        acbrG+=18
                        break
                        
    
        if acbrE == 1:
            # await message.edit(embed = bankraritypages[0])
            
            # bankraritypages.clear()
            chl = self.bot.get_channel(config.ACR_LOG_ID)
            await chl.send(f"**/acbankrarity** - User: **{interaction.user.name}** - Viewed: **{member.name}** - Server: **{interaction.guild}**- Rarity: **{rarity.name}**")
            await interaction.response.send_message(embed=bankraritypages[0]) 
            #await send_logs_acbr(commanduser,member, guild, "acbankrairty",userRarity)
            return
        else:
        
            # acBRbuttons = [
            #     [
            #     Button(style=ButtonStyle.blue,label='Prev'),
            #     Button(style=ButtonStyle.blue,label='Next'),
            #     Button(style=ButtonStyle.red,label='Close')
            #     ]
                
            # ]

            # await message.edit(components=acBRbuttons,embed = bankraritypages[0])

            # def checkauthor(user):
            #     return lambda res: res.author == user and res.message == message

            acbrT = 0
            # while True:
            #     try:
            #         acbrInteract = await client.wait_for('button_click',check = checkauthor(ctx.author),timeout=15.0)

            #         if acbrInteract.component.label == 'Prev':
            #             if acbrT > 0:
            #                 acbrT -= 1
                        
            #         elif acbrInteract.component.label == 'Next':
            #             if acbrT < acbrE-1:
            #                 acbrT += 1
                    
            #         elif acbrInteract.component.label == 'Close':
            #             break

            #         await acbrInteract.respond(content='',embed=bankraritypages[acbrT],type=7)

            #     except:
            #         break


            # acBRbuttons = []
            # await message.edit(components=acBRbuttons)

            
        
            chl = self.bot.get_channel(config.BANK_LOG_ID)
            await chl.send(f"**/acbankrarity** - User: **{interaction.user.name}** - Viewed: **{member.name}** - Server: **{interaction.guild}**- Rarity: **{rarity.name}**")
            #await interaction.response.edit_message(embed=em, view=self)
            
            view = Buttons(interaction.user,acbrT,acbrE,bankraritypages)
            await interaction.response.send_message(embed=bankraritypages[acbrT],view=view) 
            view.message = await interaction.original_response()

    
            
        
        
        
async def setup(bot):
    await bot.add_cog(ACBR(bot))