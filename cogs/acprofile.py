import discord 
import config
from discord import app_commands
from discord.ext import commands
import pymongo
import math

#intents = discord.Intents.default()
#bot = commands.Bot(command_prefix= '!', intents=intents, application_id = config.APP_ID)
#tree = app_commands.CommandTree(bot)

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


CCcharDB = cluster["acraffleCartoon"]["characters"]
CCuserDB = cluster["acraffleCartoon"]["users"]
CCshopDB = cluster["acraffleCartoon"]["usershops"]
CCshowDB = cluster["acraffleCartoon"]["shows"]
CCpresDB = cluster["acraffleCartoon"]["userprestige"]
CCloadingScreenDB = cluster["acraffleCartoon"]["loadingscreens"]
# voteDB = cluster["acrafflebot"]["uservotes"]
# moneyDB = cluster["acrafflebot"]["usershops"]

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
        
def getSznTier(percent):
    if percent >= 90: #Top 90%
        return "⬜️"
    elif percent >= 80 and percent < 90: #Top 80%
        return "⬛️"
    elif percent >= 70 and percent < 80:
        return "🟫"
    elif percent >= 60 and percent < 70:
        return "🟧"
    elif percent >= 50 and percent < 60:
        return "🟥"
    elif percent >= 40 and percent < 50:
        return "🟩"
    elif percent >= 30 and percent < 40:
        return "🟦"
    elif percent >= 20 and percent < 30:
        return "🟪"
    elif percent > 5 and percent < 20: #Top 10
        return "🟨"
    elif percent > 1 and percent <= 5: #Top 10
        return "⭐️"
    elif percent <= 1:
        return "👑"
    
    

class acpr1(discord.ui.View):
    def __init__(self,author, *, timeout=15):
        self.author = author
        super().__init__(timeout=timeout)
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    async def on_timeout(self) -> None:
        # Step 2
        for item in self.children:
            acpr1.remove_item(self,item)

        # Step 3
        await self.message.edit(view=self)
        
    @discord.ui.button(label=1, style=discord.ButtonStyle.blurple)
    async def remove1(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = userDB.find_one({"id":member.id})
        favs = []
        try:
            userfavorites = user["favorites"]
        except:
            userfavorites=[]

        for x in userfavorites:
            if x["name"] is not None:
                favs.append(x["name"])
        
        userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":favs[0]}}})
        em = discord.Embed(title = f"ACprofileremove - {member.name}",description=f"**{favs[0].capitalize()} removed from your favorites**",color = discord.Color.teal())
        em.set_thumbnail(url = member.avatar)
        
    
        
        for child in self.children:
            acpr1.remove_item(self,child)
            
        await interaction.response.edit_message(embed=em, view=self)
        
class acpr2(discord.ui.View):
    def __init__(self,author, *, timeout=15):
        self.author = author
        super().__init__(timeout=timeout)
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    async def on_timeout(self) -> None:
        # Step 2
        for item in self.children:
            acpr2.remove_item(self,item)

        # Step 3
        await self.message.edit(view=self)
        
    @discord.ui.button(label=1, style=discord.ButtonStyle.blurple)
    async def remove1(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = userDB.find_one({"id":member.id})
        favs = []
        try:
            userfavorites = user["favorites"]
        except:
            userfavorites=[]

        for x in userfavorites:
            if x["name"] is not None:
                favs.append(x["name"])
        
        userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":favs[0]}}})
        em = discord.Embed(title = f"ACprofileremove - {member.name}",description=f"**{favs[0].capitalize()} removed from your favorites**",color = discord.Color.teal())
        em.set_thumbnail(url = member.avatar)
        
    
        
        for child in self.children:
            acpr2.remove_item(self,child)
            
        await interaction.response.edit_message(embed=em, view=self)
        
    @discord.ui.button(label=2, style=discord.ButtonStyle.blurple)
    async def remove2(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = userDB.find_one({"id":member.id})
        favs = []
        try:
            userfavorites = user["favorites"]
        except:
            userfavorites=[]

        for x in userfavorites:
            if x["name"] is not None:
                favs.append(x["name"])
        
        userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":favs[1]}}})
        em = discord.Embed(title = f"ACprofileremove - {member.name}",description=f"**{favs[1].capitalize()} removed from your favorites**",color = discord.Color.teal())
        em.set_thumbnail(url = member.avatar)
        
    
        
        for child in self.children:
            acpr2.remove_item(self,child)
            
        await interaction.response.edit_message(embed=em, view=self)
        
class acpr3(discord.ui.View):
    def __init__(self,author, *, timeout=15):
        self.author = author
        super().__init__(timeout=timeout)
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    async def on_timeout(self) -> None:
        # Step 2
        for item in self.children:
            acpr2.remove_item(self,item)

        # Step 3
        await self.message.edit(view=self)
        
    @discord.ui.button(label=1, style=discord.ButtonStyle.blurple)
    async def remove1(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = userDB.find_one({"id":member.id})
        favs = []
        try:
            userfavorites = user["favorites"]
        except:
            userfavorites=[]

        for x in userfavorites:
            if x["name"] is not None:
                favs.append(x["name"])
        
        userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":favs[0]}}})
        em = discord.Embed(title = f"ACprofileremove - {member.name}",description=f"**{favs[0].capitalize()} removed from your favorites**",color = discord.Color.teal())
        em.set_thumbnail(url = member.avatar)
        
    
        
        for child in self.children:
            acpr3.remove_item(self,child)
            
        await interaction.response.edit_message(embed=em, view=self)
        
    @discord.ui.button(label=2, style=discord.ButtonStyle.blurple)
    async def remove2(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = userDB.find_one({"id":member.id})
        favs = []
        try:
            userfavorites = user["favorites"]
        except:
            userfavorites=[]

        for x in userfavorites:
            if x["name"] is not None:
                favs.append(x["name"])
        
        userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":favs[1]}}})
        em = discord.Embed(title = f"ACprofileremove - {member.name}",description=f"**{favs[1].capitalize()} removed from your favorites**",color = discord.Color.teal())
        em.set_thumbnail(url = member.avatar)
        
        for child in self.children:
            acpr3.remove_item(self,child)
            
        await interaction.response.edit_message(embed=em, view=self)
        
    @discord.ui.button(label=3, style=discord.ButtonStyle.blurple)
    async def remove3(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = userDB.find_one({"id":member.id})
        favs = []
        try:
            userfavorites = user["favorites"]
        except:
            userfavorites=[]

        for x in userfavorites:
            if x["name"] is not None:
                favs.append(x["name"])
        
        userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":favs[2]}}})
        em = discord.Embed(title = f"ACprofileremove - {member.name}",description=f"**{favs[2].capitalize()} removed from your favorites**",color = discord.Color.teal())
        em.set_thumbnail(url = member.avatar)
        
    
        
        for child in self.children:
            acpr3.remove_item(self,child)
            
        await interaction.response.edit_message(embed=em, view=self)
        
class acpr4(discord.ui.View):
    def __init__(self,author, *, timeout=15):
        self.author = author
        super().__init__(timeout=timeout)
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    async def on_timeout(self) -> None:
        # Step 2
        for item in self.children:
            acpr2.remove_item(self,item)

        # Step 3
        await self.message.edit(view=self)
        
    @discord.ui.button(label=1, style=discord.ButtonStyle.blurple)
    async def remove1(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = userDB.find_one({"id":member.id})
        favs = []
        try:
            userfavorites = user["favorites"]
        except:
            userfavorites=[]

        for x in userfavorites:
            if x["name"] is not None:
                favs.append(x["name"])
        
        userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":favs[0]}}})
        em = discord.Embed(title = f"ACprofileremove - {member.name}",description=f"**{favs[0].capitalize()} removed from your favorites**",color = discord.Color.teal())
        em.set_thumbnail(url = member.avatar)
        
    
        
        for child in self.children:
            acpr4.remove_item(self,child)
            
        await interaction.response.edit_message(embed=em, view=self)
        
    @discord.ui.button(label=2, style=discord.ButtonStyle.blurple)
    async def remove2(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = userDB.find_one({"id":member.id})
        favs = []
        try:
            userfavorites = user["favorites"]
        except:
            userfavorites=[]

        for x in userfavorites:
            if x["name"] is not None:
                favs.append(x["name"])
        
        userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":favs[1]}}})
        em = discord.Embed(title = f"ACprofileremove - {member.name}",description=f"**{favs[1].capitalize()} removed from your favorites**",color = discord.Color.teal())
        em.set_thumbnail(url = member.avatar)
        
        for child in self.children:
            acpr4.remove_item(self,child)
            
        await interaction.response.edit_message(embed=em, view=self)
        
    @discord.ui.button(label=3, style=discord.ButtonStyle.blurple)
    async def remove3(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = userDB.find_one({"id":member.id})
        favs = []
        try:
            userfavorites = user["favorites"]
        except:
            userfavorites=[]

        for x in userfavorites:
            if x["name"] is not None:
                favs.append(x["name"])
        
        userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":favs[2]}}})
        em = discord.Embed(title = f"ACprofileremove - {member.name}",description=f"**{favs[2].capitalize()} removed from your favorites**",color = discord.Color.teal())
        em.set_thumbnail(url = member.avatar)
        
    
        
        for child in self.children:
            acpr4.remove_item(self,child)
            
        await interaction.response.edit_message(embed=em, view=self)
        
    @discord.ui.button(label=4, style=discord.ButtonStyle.blurple)
    async def remove4(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = userDB.find_one({"id":member.id})
        favs = []
        try:
            userfavorites = user["favorites"]
        except:
            userfavorites=[]

        for x in userfavorites:
            if x["name"] is not None:
                favs.append(x["name"])
        
        userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":favs[3]}}})
        em = discord.Embed(title = f"ACprofileremove - {member.name}",description=f"**{favs[3].capitalize()} removed from your favorites**",color = discord.Color.teal())
        em.set_thumbnail(url = member.avatar)
        

        for child in self.children:
            acpr4.remove_item(self,child)
            
        await interaction.response.edit_message(embed=em, view=self)
        
        
        
class acpr5(discord.ui.View):
    def __init__(self,author, *, timeout=15):
        self.author = author
        super().__init__(timeout=timeout)
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    async def on_timeout(self) -> None:
        # Step 2
        for item in self.children:
            acpr2.remove_item(self,item)

        # Step 3
        await self.message.edit(view=self)
        
    @discord.ui.button(label=1, style=discord.ButtonStyle.blurple)
    async def remove1(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = userDB.find_one({"id":member.id})
        favs = []
        try:
            userfavorites = user["favorites"]
        except:
            userfavorites=[]

        for x in userfavorites:
            if x["name"] is not None:
                favs.append(x["name"])
        
        userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":favs[0]}}})
        em = discord.Embed(title = f"ACprofileremove - {member.name}",description=f"**{favs[0].capitalize()} removed from your favorites**",color = discord.Color.teal())
        em.set_thumbnail(url = member.avatar)
        
    
        
        for child in self.children:
            acpr5.remove_item(self,child)
            
        await interaction.response.edit_message(embed=em, view=self)
        
    @discord.ui.button(label=2, style=discord.ButtonStyle.blurple)
    async def remove2(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = userDB.find_one({"id":member.id})
        favs = []
        try:
            userfavorites = user["favorites"]
        except:
            userfavorites=[]

        for x in userfavorites:
            if x["name"] is not None:
                favs.append(x["name"])
        
        userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":favs[1]}}})
        em = discord.Embed(title = f"ACprofileremove - {member.name}",description=f"**{favs[1].capitalize()} removed from your favorites**",color = discord.Color.teal())
        em.set_thumbnail(url = member.avatar)
        
        for child in self.children:
            acpr5.remove_item(self,child)
            
        await interaction.response.edit_message(embed=em, view=self)
        
    @discord.ui.button(label=3, style=discord.ButtonStyle.blurple)
    async def remove3(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = userDB.find_one({"id":member.id})
        favs = []
        try:
            userfavorites = user["favorites"]
        except:
            userfavorites=[]

        for x in userfavorites:
            if x["name"] is not None:
                favs.append(x["name"])
        
        userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":favs[2]}}})
        em = discord.Embed(title = f"ACprofileremove - {member.name}",description=f"**{favs[2].capitalize()} removed from your favorites**",color = discord.Color.teal())
        em.set_thumbnail(url = member.avatar)
        
    
        
        for child in self.children:
            acpr5.remove_item(self,child)
            
        await interaction.response.edit_message(embed=em, view=self)
        
    @discord.ui.button(label=4, style=discord.ButtonStyle.blurple)
    async def remove4(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = userDB.find_one({"id":member.id})
        favs = []
        try:
            userfavorites = user["favorites"]
        except:
            userfavorites=[]

        for x in userfavorites:
            if x["name"] is not None:
                favs.append(x["name"])
        
        userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":favs[3]}}})
        em = discord.Embed(title = f"ACprofileremove - {member.name}",description=f"**{favs[3].capitalize()} removed from your favorites**",color = discord.Color.teal())
        em.set_thumbnail(url = member.avatar)
        
    
        for child in self.children:
            acpr5.remove_item(self,child)
            
        await interaction.response.edit_message(embed=em, view=self)
    
    @discord.ui.button(label=5, style=discord.ButtonStyle.blurple)
    async def remove5(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = userDB.find_one({"id":member.id})
        favs = []
        try:
            userfavorites = user["favorites"]
        except:
            userfavorites=[]

        for x in userfavorites:
            if x["name"] is not None:
                favs.append(x["name"])
        
        userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":favs[4]}}})
        em = discord.Embed(title = f"ACprofileremove - {member.name}",description=f"**{favs[4].capitalize()} removed from your favorites**",color = discord.Color.teal())
        em.set_thumbnail(url = member.avatar)
        
        for child in self.children:
            acpr5.remove_item(self,child)
            
        await interaction.response.edit_message(embed=em, view=self)
        
        

        
        
class ACPROF(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("ACPROFILE Cog loaded!")
        
        
    @app_commands.command(name='acprofile', description='Profile Displaying Favorite Characters and Stats')
    async def acprofile(self,interaction: discord.Interaction, user: discord.User):
        await interaction.response.defer()
        
        # await interaction.edit_original_response(view=self)
        member = user
        favorites = []
        #commandUser = ctx.author
        guild = interaction.guild
        botStats = botstatsDB.find_one({"id":573})
        if botStats['botOffline']==True:
            em = discord.Embed(title = f"ACprofile - {member.name}\nThe bot is rebooting...\nTry again in a few minutes.",color = getColor('botColor'))
            em.set_thumbnail(url = member.avatar)
            await interaction.edit_original_response(embed=em)
            return
        
        await createuser(member, guild)
        await createshopuser(member,guild)
        await createsznuser(member)
        await createsznWinuser(member)
        #await send_logs_profile(commandUser, member, guild, "acprofile")

        user = userDB.find_one({"id":member.id})
        moneyProf = shopDB.find_one({'id':member.id})
        usermoney = moneyProf["money"]

        # em = discord.Embed(title = f"ACprofile - {member.name}\nLoading...",color = getColor("botColor"))
        # em.set_thumbnail(url = member.avatar)
        # message = await ctx.send(embed = em)
        hasmal = True
        hasanilist = True
        hasbio = True
        try:
            usermal = user["mal"]
        except:
            hasmal = False

        try:
            useranilist = user["anilist"]
        except:
            hasanilist = False

        try:
            userbio = user["bio"]
        except:
            hasbio = False

        try:
            userfavorites = user["favorites"]
        except:
            userfavorites=[]

        for x in userfavorites:
            if x["name"] is not None:
                favorites.append(x["name"])
        
        gifList = []
        for x in userfavorites:
            char = charDB.find_one({"name":x["name"]})
            if char == None:
                char = CCcharDB.find_one({"name":x["name"]})
            gifList.append(char["gif"])

        try:
            charsUnlocked = user["charsunlocked"]
        except:
            charsUnlocked = 0

        try:
            hypersUnl = user["hypersunlocked"]
        except:
            hypersUnl = 0

        # i = userDB.count_documents({"charsunlocked": { "$gt" : charsUnlocked}}) + 1

        #hypers = userDB.count_documents({"hypersunlocked": { "$gt" : hypersUnl}}) + 1
        #totHypUsers = userDB.count_documents({"hypersunlocked": { "$gt" : 0}})

        pres = presDB.find_one({'id':member.id})
        try:
            totPres = pres['totPres']
        except:
            totPres = 0

        # presRank = presDB.count_documents({"totPres": { "$gt" : totPres}}) + 1
        # totPresUsers = presDB.count_documents({"totPres": { "$gt" : 0}})
        
        botstat = botstatsDB.find_one({"id": 573})
        # uniqueuser = botstat["uniqueUser"]
        totalChars = charDB.estimated_document_count()

        charFound = True
        try:
            currentchar = user["currentchar"]
        except:
            pass
        if currentchar == None:
            charFound = False
            try:
                userChars = user['characters']
                for x in userChars:
                    currentchar = x['name']
                    break
            except:
                em = discord.Embed(title = f"ACprofile",description=f"{member.name} does not have any characters unlocked!\nTo unlock a character to display on your profile do **/acr and /acrp**",color = getColor("botColor"))
                em.set_thumbnail(url = member.avatar)
                await interaction.edit_original_response(embed=em)
                return


        # try:
        #     hypleg = user["hypersunlocked"]
        # except:
        #     hypleg = 0

        try:
            leg = user["legendsunlocked"]
        except:
            leg = 0

        try:
            epics = user["legunlocked"]
        except:
            epics = 0


        try:
            color = user["profilecolor"]
        except:
            color = getColor("common")
            
        char = charDB.find_one({"name":currentchar})
        if char == None:
            char = CCcharDB.find_one({"name":currentchar})
        charname=char["name"]
        chargif=char["gif"]
        charshow=char["show"]
        # charrarity=char["rarity"]

        show = showDB.find_one({"name":charshow})
        if show == None:
            show = CCshowDB.find_one({"name":charshow})
        showOutput = show["title"]

        # sznUser = sznDB.find_one({'id':member.id})
        # sznRank = sznDB.count_documents({"xp": { "$gt" : sznUser['xp']}}) + 1
        # totSzn = sznDB.count_documents({})
        
        
        com=0
        uncom=0
        rar =0
        for x in user["characters"]:
            if x["rarity"] == "common":
                com+=1
            if x["rarity"] == "uncommon":
                uncom+=1
            if x["rarity"] == "rare":
                rar+=1
                
                
        totcom = charDB.count_documents({"rarity": "common"}) 
        totuncom = charDB.count_documents({"rarity": "uncommon"}) 
        totrar = charDB.count_documents({"rarity": "rare"}) 
        totEpics = charDB.count_documents({"rarity": "epic"}) 
        totlegs = charDB.count_documents({"rarity": "legendary"}) 
        tothypers = charDB.count_documents({"rarity": "hyperlegendary"}) 
 
        # sznPer = math.ceil(100 * (sznRank / totSzn))
        
        # if sznPer <= 10:
        #     rounded = round(sznPer/5)*5
        # else:
        #     sznPer = sznPer - (sznPer % 10)
        #     rounded = round(sznPer/10)*10
        
        # if rounded == 0:
        #     rounded = 1

        joinVar = ' - '
        
        homeem = discord.Embed(title = f"ACprofile - {member.name}",color = color)
        homeem.add_field(name=f"**Character:  {charname.capitalize()}**",value=f"\nShow: {showOutput}", inline=True)
        homeem.add_field(name=f'**Money**', value=f'${usermoney}', inline=True)
        if len(favorites) != 0:
            homeem.add_field(name="**Favorites**",value = f'{joinVar.join(favorites[i].capitalize() for i in range(0,len(favorites)))}',inline = False)
        
       
        # homeem.add_field(name=f'**League Season**', value=f'Rank: {sznRank}/{totSzn}\nLeague: {getSznTier(rounded)} Top {rounded}%', inline=False)
        
        homeem.add_field(name=f'**Stats**', value=f'Total Characters: {charsUnlocked}/{totalChars} ({"{:.2f}".format((charsUnlocked/totalChars)*100)}%) \nPrestige Level: {totPres}\n\nCommons: {com} / {totcom} \nUncommons: {uncom} / {totuncom}\nRares: {rar} / {totrar}\nEpics: {epics} / {totEpics}\nLegendaries: {leg} / {totlegs}\nHyper Legendaries: {hypersUnl} / {tothypers}', inline=True)
        
        
        if hasmal is True:
            homeem.add_field(name=f"**MAL**",value=f"{usermal}", inline=False)
        if hasanilist is True:
            homeem.add_field(name=f"**Anilist**",value=f"{useranilist}", inline=False)
        if hasbio is True:
            userbio = str(userbio)
            homeem.add_field(name=f"**Bio**",value=f"{userbio}", inline=False)

        if color == getColor("common") and charFound == True:
            homeem.set_footer(text=f"Tip: Change profile color with /acpc")
        if color == getColor("common") and charFound == False:
            homeem.set_footer(text=f"Your profile is displaying the first character you unlocked.\nTo choose a different character you have unlocked use /acsc\nYou can also change your profile color with /acpc")

        homeem.set_thumbnail(url = member.avatar)
        homeem.set_image(url=chargif)

        await interaction.edit_original_response(embed=homeem)
       
    @app_commands.command(name='acprofilecharacter', description='Sets the character displayed on your profile')
    async def acprofilecharacter(self,interaction: discord.Interaction, character: str):
        member = interaction.user
        guild = interaction.guild
        await createuser(member, guild)
        if character is None:
            em = discord.Embed(title = "ACprofilecharacter",description=f"Sets a character that you have unlocked to appear on your /acprofile.\nUse /acbs *show* to see your unlocked characters.",color = discord.Color.teal())
            await interaction.response.send_message(embed=em)
            return
        character = character.lower()
        charfound = charDB.find_one({"name":character})
        
        user = userDB.find_one({"id":member.id})
        try:
            userChars = user['characters']
        except:
            userChars = []
        for p in userChars:
            if p["name"] == character:
                userDB.update_one({"id":member.id}, {"$set":{"currentchar":character}})
                char = charDB.find_one({"name":character})
                gif = char["gif"]
                show = char["show"]
                rarity = char["rarity"]
                em = discord.Embed(title = f"ACprofilecharacter - {member.name}",description=f"Character: **{character.capitalize()}**\nShow: **{show.capitalize()}**\nRarity: **{rarity.capitalize()}**\n\n**Do /acprofile to check it out!**",color = getColor(rarity))
                em.set_image(url=gif)
                em.set_thumbnail(url=member.avatar)
                await interaction.response.send_message(embed=em)
                if char['name'] == 'eren':
                    achDB.update_one({"id":member.id}, {"$set":{"setEren":True}})
                # await send_logs_profile_change(member, guild, "acsetcharacter",character)
                return
            

        if charfound == None: 
            charfound2 = CCcharDB.find_one({"name":character})
            user = CCuserDB.find_one({"id":member.id})
            try:
                userChars = user['characters']
            except:
                userChars = []
            for p in userChars:
                if p["name"] == character:
                    userDB.update_one({"id":member.id}, {"$set":{"currentchar":character}})
                    char = CCcharDB.find_one({"name":character})
                    gif = char["gif"]
                    show = char["show"]
                    rarity = char["rarity"]
                    em = discord.Embed(title = f"ACprofilecharacter - {member.name}",description=f"Character: **{character.capitalize()}**\nShow: **{show.capitalize()}**\nRarity: **{rarity.capitalize()}**\n\n**Do /acprofile to check it out!**",color = getColor(rarity))
                    em.set_image(url=gif)
                    em.set_thumbnail(url=member.avatar)
                    await interaction.response.send_message(embed=em)
                    # await send_logs_profile_change(member, guild, "acsetcharacter",character)
                    return
            if charfound2 == None:
                em = discord.Embed(title = "ACprofilecharacter",description=f"{character.capitalize()} is not available.\nFor a list of characters in a show do **/acbs *show***",color = discord.Color.teal())
                em.set_thumbnail(url=member.avatar)
                await interaction.response.send_message(embed=em)
                return
            else:
                em = discord.Embed(title = "ACprofilecharacter",description=f"**{member.name}** hasn't unlocked **{character.capitalize()}**",color = discord.Color.teal())
                em.set_thumbnail(url=member.avatar)
                await interaction.response.send_message(embed=em)
                return
                
        else:
            em = discord.Embed(title = "ACprofilecharacter",description=f"**{member.name}** hasn't unlocked **{character.capitalize()}**",color = discord.Color.teal())
            em.set_thumbnail(url=member.avatar)
            await interaction.response.send_message(embed=em)
            return
        
    @app_commands.command(name='acprofilecolor', description='Sets the color displayed on your profile')
    @app_commands.describe(color="Default Colors: Red, Blue, Yellow, Green, Purple, or Enter a HEX Code (No # in front)")
    async def acprofilecolor(self,interaction: discord.Interaction, color: str):
        botstat = botstatsDB.find_one({"id":573})
        member = interaction.user
        guild= interaction.guild
        await createuser(member,guild)
        await createshopuser(member,guild)
        user = userDB.find_one({"id":member.id})
        shopStuff = shopDB.find_one({'id':member.id})
        if color == None:
            em = discord.Embed(title = f"ACprofilecolor - {member.name}",description=f"**Allows you to change the color of your /acprofile.**\nChoose a listed color or enter a HEX code if you want a custom color!\n**Default Colors: Red, Blue, Green, Yellow, Purple.\nHEX Website: https://www.color-hex.com/ \nExample: /acpc red\nExample (HEX): /acpc b3346c\nPrice: ${botstat['colorprice']} - Your Balance: ${shopStuff['money']}**",color = discord.Color.teal())
            em.set_thumbnail(url = member.avatar)
            await interaction.response.send_message(embed=em)
            return

        try:
            color = color.lower()
        except:
            pass
        
        if color == "red":
            color = "ff0000"
        if color == "blue":
            color = "0000FF"
        if color == "green":
            color = "45ce00"
        if color == "yellow":
            color = "FFFF00"
        if color == "purple":
            color = "aa00e5"

        try:
            colorINT =  int(color, 16)
        except:
            em = discord.Embed(title = f"ACprofilecolor - {member.name}",description=f"**Invalid Color!**\nChoose a listed color or enter a HEX code if you want a custom color!\n**Default Colors: Red, Blue, Green, Yellow, Purple.\nHEX Website: https://www.color-hex.com/ \nExample: /acprofilecolor b3346c**",color = discord.Color.teal())
            em.set_thumbnail(url = member.avatar)
            await interaction.response.send_message(embed=em)
            return
        
    
        em = discord.Embed(title = f"ACprofilecolor - {member.name}",description=f"Change Profile Color to **{color}**?\n**Cost: ${botstat['colorprice']}**\nYour Balance: **${shopStuff['money']}**",color = discord.Color(colorINT))
        em.set_thumbnail(url = member.avatar)
        
        em = discord.Embed(title = f"ACprofilecolor - {member.name}",description=f"Profile Color changed to **{color}**",color = discord.Color(colorINT))
        em.set_thumbnail(url = member.avatar)
        
        userDB.update_one({"id":member.id}, {"$set":{"profilecolor":colorINT}})
        #await send_logs_profile_color(member,guild,"acprofilecolor",color)
        await interaction.response.send_message(embed=em)
                    
                    
    @app_commands.command(name='acprofilebio', description='Sets the Bio displayed on your profile')
    @app_commands.describe(bio="Enter your bio here (Max 300 Characters)")
    async def acprofilebio(self,interaction: discord.Interaction, bio: str):
        member = interaction.user
        guild = interaction.guild
        botStats = botstatsDB.find_one({"id":573})
        if botStats['botOffline']==True:
            em = discord.Embed(title = f"ACsetbio - {member.name}\nThe bot is rebooting...\nTry again in a few minutes.",color = getColor('botColor'))
            em.set_thumbnail(url = member.avatar)
            await interaction.response.send_message(embed=em)
            
        await createuser(member, guild)
        
        if bio == "":
            em = discord.Embed(title = "ACsetbio",description=f'Adds a bio to your /acprofile (Max **300** characters)',color = discord.Color.teal())
            em.set_thumbnail(url = member.avatar)
            await interaction.response.send_message(embed=em)
            

        if len(bio) > 300:
            em = discord.Embed(title = "ACsetbio",description=f"*Bio* has to be less than 300 characters.",color = discord.Color.teal())
            em.set_thumbnail(url = member.avatar)
            await interaction.response.send_message(embed=em)
            

        if "https" in bio:
            em = discord.Embed(title = "ACsetbio",description=f"You cannot have links in your bio",color = discord.Color.teal())
            em.set_thumbnail(url = member.avatar)
            await interaction.response.send_message(embed=em)
         
        
        
        userDB.update_one({"id":member.id}, {"$set":{"bio":bio}})
        em = discord.Embed(title = f"ACsetbio - {member.name}",description=f"Bio Updated: **{bio}**\nUse **/acprofile** to check it out!",color = discord.Color.teal())
        em.set_thumbnail(url = member.avatar)
        
        #await send_logs_profile_change(member, guild, "acsetbio",bio)
        await interaction.response.send_message(embed=em)
        
    @app_commands.command(name='acprofilemal', description='Display a link to a MAL account on your acprofile')
    async def acprofilemal(self,interaction: discord.Interaction, mal: str):
        member = interaction.user
        guild = interaction.guild
        await createuser(member, guild)
        
        if "myanimelist" and "profile" not in mal:
            em = discord.Embed(title = "ACsetmal",description=f"*Link:* {mal}\n is not valid, please use a *My Anime List* profile link.",color = discord.Color.teal())
            await interaction.response.send_message(embed=em)
            return
            
        userDB.update_one({"id":member.id}, {"$set":{"mal":mal}})
        em = discord.Embed(title = f"ACsetmal",description=f"{member.name.capitalize()}'s MAL: {mal}\nUpdated on your profile use /acprofile to check it out",color = discord.Color.teal())
        await interaction.response.send_message(embed=em)
        
    @app_commands.command(name='acprofileanilist', description='Display a link to a Anilist account on your acprofile')
    async def acprofileanilist(self,interaction: discord.Interaction, anilist: str):
        member = interaction.user
        guild = interaction.guild
        await createuser(member, guild)
        
        if "anilist" and "user" not in anilist:
            em = discord.Embed(title = "ACsetanilist",description=f"*Link:* {anilist}\n is not valid, please use a *Anilist* profile link.",color = discord.Color.teal())
            await interaction.response.send_message(embed=em)
            return
            
        userDB.update_one({"id":member.id}, {"$set":{"anilist":anilist}})
        em = discord.Embed(title = f"ACsetanilist",description=f"{member.name.capitalize()}'s Anilist: {anilist}\nUpdated on your profile use /acprofile to check it out",color = discord.Color.teal())
        await interaction.response.send_message(embed=em)
        
    @app_commands.command(name='acprofileremove', description='Remove something from your /acprofile')
    @app_commands.choices(remove=[
        discord.app_commands.Choice(name='Bio',value=1),
        discord.app_commands.Choice(name='MAL',value=2),
        discord.app_commands.Choice(name='Anilist',value=3),
        discord.app_commands.Choice(name='Favorite',value=4)
    ])
    async def acprofileremove(self,interaction: discord.Interaction, remove: discord.app_commands.Choice[int]):
        member = interaction.user
        guild = interaction.guild
        if(remove.value == 1):
            userDB.update_one({"id":member.id}, {"$unset":{"bio":""}})
            em = discord.Embed(title = f"ACprofileremove - {member.name}",description=f"Bio successfully removed from your profile.",color = discord.Color.teal())
            em.set_thumbnail(url=member.avatar)
            await interaction.response.send_message(embed=em)
        
        elif(remove.value == 2):
            userDB.update_one({"id":member.id}, {"$unset":{"mal":""}})
            em = discord.Embed(title = f"ACprofileremove - {member.name}",description=f"Mal successfully removed from your profile.",color = discord.Color.teal())
            em.set_thumbnail(url=member.avatar)
            await interaction.response.send_message(embed=em)
        
        elif(remove.value == 3):
            userDB.update_one({"id":member.id}, {"$unset":{"anilist":""}})
            em = discord.Embed(title = f"ACprofileremove - {member.name}",description=f"Anilist successfully removed from your profile.",color = discord.Color.teal())
            em.set_thumbnail(url=member.avatar)
            await interaction.response.send_message(embed=em)
        
        elif(remove.value == 4):
            user = userDB.find_one({"id":member.id})
            favs = []
            try:
                userfavorites = user["favorites"]
            except:
                userfavorites=[]

            for x in userfavorites:
                if x["name"] is not None:
                    favs.append(x["name"])
                    
            if len(favs) == 0:
                em = discord.Embed(title = f"ACprofileremove - {member.name}",description=f"You do not have any favorites to remove",color = discord.Color.teal())
                em.set_thumbnail(url=member.avatar)
                await interaction.response.send_message(embed=em)
                return
                    
            joinVar = ' - '
        
            favem = discord.Embed(title = f"ACprofileremove - {member.name}",description=f"Please Choose a favorite to remove by typing it in the box",color = discord.Color.teal())
            
            if len(favs) != 0:
                favem.add_field(name="**Favorites**",value = f'{joinVar.join(favs[i].capitalize() for i in range(0,len(favs)))}',inline = False)
                     
            
            # userDB.update_one({"id":member.id}, {"$unset":{"anilist":""}})
            # em = discord.Embed(title = f"ACprofileremove - {member.name}",description=f"Anilist successfully removed from your profile.",color = discord.Color.teal())
            favem.set_thumbnail(url=member.avatar)
            print(len(favs))
            if len(favs) == 1:
                await interaction.response.send_message(embed=favem,view=acpr1(interaction.user))
            if len(favs) == 2:
                await interaction.response.send_message(embed=favem,view=acpr2(interaction.user))
            if len(favs) == 3:
                await interaction.response.send_message(embed=favem,view=acpr3(interaction.user))
            if len(favs) == 4:
                await interaction.response.send_message(embed=favem,view=acpr4(interaction.user))
            if len(favs) == 5:
                await interaction.response.send_message(embed=favem,view=acpr5(interaction.user))
                
    @app_commands.command(name='acprofilefavorite', description='Adds a character to your favorites (Max 5)')
    async def acprofilefavorite(self,interaction: discord.Interaction, character: str):
        member = interaction.user
        botStats = botstatsDB.find_one({"id":573})
        if botStats['botOffline']==True:
            em = discord.Embed(title = f"ACsetfavorite - {member.name}\nThe bot is rebooting...\nTry again in a few minutes.",color = getColor('botColor'))
            em.set_thumbnail(url = member.avatar)
            await interaction.response.send_message(embed=em)
            return

        
        character=character.lower()

        guild = interaction.guild

        character1Found = charDB.find_one({"name":character})
        
        if character1Found == None:
            character2Found = CCcharDB.find_one({"name":character})
            if character2Found == None:
                em = discord.Embed(title = "ACsetfavorite",description=f"Character, **{character.capitalize()}**, not found.\nFor a list of your unlocked characters do **/ccbank**",color = discord.Color.teal())
                em.set_thumbnail(url = member.avatar)
                await interaction.response.send_message(embed=em)
                return
            
            user = userDB.find_one({"id":member.id})
            CCuser = CCuserDB.find_one({"id":member.id})
            userchars= CCuser["characters"]
            haschar = False
            
            #userDB.update_one({"id":member.id}, {"$addToSet":{"favorites":{"name":"placeHolder"}}})
            userFavorites = user["favorites"]
            userfavlist = []
            amountFavs = 0
            for x in userFavorites:
                userfavlist.append(x["name"])
                amountFavs+=1
                if character == x["name"]:
                    em = discord.Embed(title = "ACsetfavorite",description=f"**{x['name'].capitalize()}** is already in your favorites.",color = discord.Color.teal())
                    em.set_thumbnail(url=member.avatar)
                    await interaction.response.send_message(embed=em)
                    return


            for x in userchars:
                if x["name"] == character:
                    haschar = True
                else:
                    continue

            if haschar == False:
                em = discord.Embed(title = "ACsetfavorite",description=f"**{member.name}** hasn't unlocked **{character.capitalize()}**",color = discord.Color.teal())
                em.set_thumbnail(url=member.avatar)
                await interaction.response.send_message(embed=em)
                return
            
            if amountFavs >= 5:
                em = discord.Embed(title = "ACsetfavorite",description=f"**{member.name}** already has 5 favorites, please use **/acprofileremove favorite** to remove a favorite, and then try again.",color = discord.Color.teal())
                em.set_thumbnail(url=member.avatar)
                await interaction.response.send_message(embed=em)
                return
            else:
                userDB.update_one({"id":member.id}, {"$addToSet":{"favorites":{"name":character}}})
                em = discord.Embed(title = "ACsetfavorite",description=f"**{character.capitalize()}** added to your favorites.",color = getColor("botColor"))
                em.set_thumbnail(url=member.avatar)
                em.set_image(url=character2Found['gif'])
                await interaction.response.send_message(embed=em)
                return
    
            
        
        user = userDB.find_one({"id":member.id})
        userchars= user["characters"]
        haschar = False
        
        #userDB.update_one({"id":member.id}, {"$addToSet":{"favorites":{"name":"placeHolder"}}})
        userFavorites = user["favorites"]
        userfavlist = []
        amountFavs = 0
        for x in userFavorites:
            userfavlist.append(x["name"])
            amountFavs+=1
            if character == x["name"]:
                em = discord.Embed(title = "ACsetfavorite",description=f"**{x['name'].capitalize()}** is already in your favorites.",color = discord.Color.teal())
                em.set_thumbnail(url=member.avatar)
                await interaction.response.send_message(embed=em)
                return


        for x in userchars:
            if x["name"] == character:
                haschar = True
            else:
                continue

        if haschar == False:
            em = discord.Embed(title = "ACsetfavorite",description=f"**{member.name}** hasn't unlocked **{character.capitalize()}**",color = discord.Color.teal())
            em.set_thumbnail(url=member.avatar)
            await interaction.response.send_message(embed=em)
            return
        
        if amountFavs >= 5:
            em = discord.Embed(title = "ACsetfavorite",description=f"**{member.name}** already has 5 favorites, please use **/acprofileremove favorite** to remove a favorite, and then try again.",color = discord.Color.teal())
            em.set_thumbnail(url=member.avatar)
            await interaction.response.send_message(embed=em)
            return
        else:
            userDB.update_one({"id":member.id}, {"$addToSet":{"favorites":{"name":character}}})
            em = discord.Embed(title = "ACsetfavorite",description=f"**{character.capitalize()}** added to your favorites.",color = getColor("botColor"))
            em.set_thumbnail(url=member.avatar)
            em.set_image(url=character1Found['gif'])
            await interaction.response.send_message(embed=em)
            return
                
            
        #await send_logs_profile_change(member,guild,'acsetfavorite',character)
        
            
        

        
    
        
async def setup(bot):
    await bot.add_cog(ACPROF(bot))