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

# charDB = cluster["acrafflebot"]["characters"]
# userDB = cluster["acrafflebot"]["users"]
# botstatsDB = cluster["acrafflebot"]["botstats"]
# showDB = cluster["acrafflebot"]["shows"]
# loadingScreenDB = cluster["acrafflebot"]["loadingscreens"]
# shopDB = cluster["acrafflebot"]["usershops"]
# voteDB = cluster["acrafflebot"]["uservotes"]
# blockDB = cluster["acrafflebot"]["blocks"]
# presDB = cluster["acrafflebot"]["userprestige"]
# achDB = cluster["acrafflebot"]["achievements"]
# sznDB = cluster["acrafflebot"]["seasons"]
# sznWinDB = cluster["acrafflebot"]["sznwinners"] 

botstatsDB = cluster["acrafflebot"]["botstats"]

charDB = cluster["acraffleCartoon"]["characters"]
userDB = cluster["acraffleCartoon"]["users"]
shopDB = cluster["acraffleCartoon"]["usershops"]
showDB = cluster["acraffleCartoon"]["shows"]
presDB = cluster["acraffleCartoon"]["userprestige"]
loadingScreenDB = cluster["acraffleCartoon"]["loadingscreens"]
voteDB = cluster["acrafflebot"]["uservotes"]
moneyDB = cluster["acrafflebot"]["usershops"]

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
            
             
class CCBR(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("CCBR Cog loaded!")
        
    
    @app_commands.command(name="ccbr",description="CCbankrarity - Shows all unlocked characters for a specified rarity")
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
            em = discord.Embed(title = f"CCbr - {member.name}\nThe bot is rebooting...\nTry again in a few minutes.",color = getColor('botColor'))
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
            title = f"CCbankrarity\nUser: {interaction.user.name} - Viewing: {membername}\nPage: ({acbrX+1}/{acbrE})",
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
            await chl.send(f"**/CCbankrarity** - User: **{interaction.user.name}** - Viewed: **{member.name}** - Server: **{interaction.guild}**- Rarity: **{rarity.name}**")
            await interaction.response.send_message(embed=bankraritypages[0]) 
            #await send_logs_acbr(commanduser,member, guild, "acbankrairty",userRarity)
            return
        else:
        

            acbrT = 0
            

    
            chl = self.bot.get_channel(config.BANK_LOG_ID)
            await chl.send(f"**/CCbankrarity** - User: **{interaction.user.name}** - Viewed: **{member.name}** - Server: **{interaction.guild}**- Rarity: **{rarity.name}**")
            #await interaction.response.edit_message(embed=em, view=self)
            
            view = Buttons(interaction.user,acbrT,acbrE,bankraritypages)
            await interaction.response.send_message(embed=bankraritypages[acbrT],view=view) 
            view.message = await interaction.original_response()

    
            
        
        
        
async def setup(bot):
    await bot.add_cog(CCBR(bot))