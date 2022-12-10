import discord 
import config
from discord import app_commands
from discord.ext import commands

import pymongo
import datetime

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


def updateHyperLeg(member):
        user = userDB.find_one({"id":member.id})
        HypLeg = 0
        for x in user["characters"]:
            if x["rarity"] == "hyperlegendary":
                HypLeg+=1
                
        userDB.update_one({"id":member.id}, {"$set":{"hypersunlocked":HypLeg}})
        
async def createuser(member,guild):
    data = userDB.find_one({"id":member.id})
    if data is None:
        # guildid = guild.id
        # guildname = guild.name
        newuser = {"id": member.id,"name":member.name,"currentchar":None}
        userDB.insert_one(newuser)
        userDB.update_one({"id":member.id}, {"$set":{"favorites": [] }})
       
        #await send_logs_newuser(member,guild)
        return
    else:
        if data["name"] == member.name:
            return
        else:
            userDB.update_one({"id":member.id}, {"$set":{"name":member.name}})
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

class Buttons(discord.ui.View):
    def __init__(self,author,commanduser,charGive,charRec, *, timeout=20):
        self.author = author
        self.commanduser = commanduser
        self.charGive = charGive
        self.charRec = charRec
        super().__init__(timeout=timeout)
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    async def on_timeout(self) -> None:
        # Step 2
        em = discord.Embed(title = "ACtrade",description=f"**Trade Canceled!**\n{self.author.name} did not respond within 20 seconds.",color = discord.Color.red())
        em.set_thumbnail(url=self.author.avatar)
        for item in self.children:
            Buttons.remove_item(self,item)

        # Step 3
        await self.message.edit(embed=em, view=self)
        
        
    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def acceptTrade(self, interaction: discord.Interaction, button: discord.ui.Button):
        #recheck if both users still have the characters
        commanduser = self.commanduser
        member = interaction.user
        characterGive = self.charGive
        characterRecieve = self.charRec
        check1 = userDB.find_one({"id":commanduser.id, "characters":{"$elemMatch": {"name":characterGive}}})
        check2 = userDB.find_one({"id":member.id, "characters":{"$elemMatch": {"name":characterRecieve}}})
        if check1 is None:
            blankcomp = []
            em = discord.Embed(title = "ACtrade",description=f"**Trade Cancelled!**\n{commanduser.name} no longer has {characterGive.capitalize()} in their bank. This probably happened if one of you accepted a trade for the same character while this window was open.",color = discord.Color.teal())
            em.set_thumbnail(url = commanduser.avatar)
            for item in self.children:
                Buttons.remove_item(self,item)
            await self.message.edit(embed=em, view=self)
            return
        
        if check2 is None:
            blankcomp = []
            em = discord.Embed(title = "ACtrade",description=f"**Trade Cancelled!**\n{member.name} no longer has {characterGive.capitalize()} in their bank. This probably happened if one of you accepted a trade for the same character while this window was open.",color = discord.Color.teal())
            em.set_thumbnail(url = member.avatar)
            for item in self.children:
                Buttons.remove_item(self,item)
            await self.message.edit(embed=em, view=self)
            return

        #proceed with trade
        characterRecieveProf = charDB.find_one({"name":characterRecieve})
        characterGiveProf = charDB.find_one({"name":characterGive})

        charrecievename = characterRecieveProf["name"]
        chargivename = characterGiveProf["name"]
        
        charrecieveshow = characterRecieveProf["show"]
        chargiveshow = characterGiveProf["show"]
        
        charrecieverarity = characterRecieveProf["rarity"]
        chargiverrarity = characterGiveProf["rarity"]
        
        userDB.update_one({"id":commanduser.id}, {"$pull":{"characters":{"name":chargivename,"show":chargiveshow,"rarity":chargiverrarity}}})
        userDB.update_one({"id":member.id}, {"$pull":{"characters":{"name":charrecievename,"show":charrecieveshow,"rarity":charrecieverarity}}})
        
        userDB.update_one({"id":commanduser.id}, {"$addToSet":{"characters":{"name":charrecievename,"show":charrecieveshow,"rarity":charrecieverarity}}})
        userDB.update_one({"id":member.id}, {"$addToSet":{"characters":{"name":chargivename,"show":chargiveshow,"rarity":chargiverrarity}}})
        
        characterRecfound = charDB.find_one({"name":characterRecieve})
        characterGivefound = charDB.find_one({"name":characterGive})
        
        userProf = userDB.find_one({"id":commanduser.id})
        userhasHL = False
        try:
            userChars = userProf['characters']
        except:
            pass
        for x in userChars:
            if characterGivefound["show"] == x["show"]:
                if x["rarity"] == "hyperlegendary":
                    userhasHL = True
                    break


        userpres = presDB.find_one({'id':commanduser.id})
        if userpres == None:
            userisPres = False
        else:
            userisPres = False
            preslist = userpres['shows']
            for shws in preslist:
                if shws['show'] == characterGivefound['show']:
                    userisPres = True
            


        memberProf = userDB.find_one({"id":member.id})
        memberhasHL = False
        try:
            memberChars = memberProf['characters']
        except:
            pass
        
        for x in memberChars:
            if characterRecfound["show"] == x["show"]:
                if x["rarity"] == "hyperlegendary":
                    memberhasHL = True
                    break
        
        memberpres = presDB.find_one({'id':member.id})
        if memberpres == None:
            memberisPres = False
        else:
            memberisPres = False
            preslist = memberpres['shows']
            for shws in preslist:
                if shws['show'] == characterRecfound['show']:
                    memberisPres = True

        if userProf["currentchar"] == characterGive:
            userDB.update_one({"id":commanduser.id}, {"$set":{"currentchar":characterRecieve}})
        if memberProf["currentchar"] == characterRecieve:
            userDB.update_one({"id":member.id}, {"$set":{"currentchar":characterGive}})

            
        if userhasHL is True and userisPres == False:
            userDB.update_one({"id":commanduser.id}, {"$pull":{"characters":{"show":chargiveshow,"rarity":"hyperlegendary"}}})
            hyperlegUser = charDB.find_one({"show":chargiveshow,"rarity":"hyperlegendary"})
            if userProf["currentchar"] == hyperlegUser["name"]:
                userDB.update_one({"id":commanduser.id}, {"$set":{"currentchar":characterRecieve}})
            try:
                userFavs= userProf["favorites"]
                for x in userFavs:
                    if x["name"] == hyperlegUser["name"]:
                        userDB.update_one({"id":commanduser.id}, {"$pull":{"favorites":{"name":hyperlegUser["name"]}}})
            except:
                pass


        if memberhasHL is True and memberisPres == False:
            userDB.update_one({"id":member.id}, {"$pull":{"characters":{"show":charrecieveshow,"rarity":"hyperlegendary"}}})
            hyperlegMember = charDB.find_one({"show":charrecieveshow,"rarity":"hyperlegendary"})
            if memberProf["currentchar"] == hyperlegMember["name"]:
                userDB.update_one({"id":member.id}, {"$set":{"currentchar":characterGive}})
            try:
                memberFavs= memberProf["favorites"]
                for x in memberFavs:
                    if x["name"] == hyperlegMember["name"]:
                        userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":hyperlegMember["name"]}}})
            except:
                pass
            
        try:
            userFavs= userProf["favorites"]
            for x in userFavs:
                if x["name"]== chargivename:
                    userDB.update_one({"id":commanduser.id}, {"$pull":{"favorites":{"name":chargivename}}})
        except:
            pass
        try:
            memberFavs= memberProf["favorites"]
            for x in memberFavs:
                if x["name"]== charrecievename:
                    userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":charrecievename}}})
        except:
            pass
        
        updateHyperLeg(member)
        updateHyperLeg(commanduser)


        em = discord.Embed(title = f"ACtrade",description=f"Trade successful!",color = discord.Color.green())
        em.add_field(name="Results:",value=f"{commanduser.name.capitalize()} got **{characterRecieve.capitalize()}** and {member.name.capitalize()} got **{characterGive.capitalize()}**")
        em.set_thumbnail(url = member.avatar)

        currenttime = datetime.datetime.utcnow()
        achMem = achDB.find_one({'id':member.id})
        achCom = achDB.find_one({'id':commanduser.id})


        try:
            cooldownVal = achMem['tradecool']
            secadded = datetime.timedelta(seconds=30)
            futureTime = cooldownVal + secadded
            if currenttime > futureTime:
                achDB.update_one({"id":member.id}, {"$inc":{'trades':1}})
                achDB.update_one({"id":member.id}, {"$set":{'tradecool':currenttime}}) 
        except:
            achDB.update_one({"id":member.id}, {"$inc":{'trades':1}})
            achDB.update_one({"id":member.id}, {"$set":{'tradecool':currenttime}}) 
        
        try:
            cooldownVal = achCom['tradecool']
            secadded = datetime.timedelta(seconds=30)
            futureTime = cooldownVal + secadded
            if currenttime > futureTime:
                achDB.update_one({"id":commanduser.id}, {"$inc":{'trades':1}})
                achDB.update_one({"id":commanduser.id}, {"$set":{'tradecool':currenttime}}) 
        except:
            achDB.update_one({"id":commanduser.id}, {"$inc":{'trades':1}})
            achDB.update_one({"id":commanduser.id}, {"$set":{'tradecool':currenttime}}) 


        for child in self.children:
            Buttons.remove_item(self,child)
            
        await interaction.response.edit_message(embed=em, view=self)
        
    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger)
    async def denyTrade(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        em = discord.Embed(title = "ACtrade",description=f"Trade denied by {member.name}",color = discord.Color.red())
        em.set_thumbnail(url = member.avatar)
        
        for child in self.children:
            Buttons.remove_item(self,child)
            
        await interaction.response.edit_message(embed=em, view=self)
                
        
        
        
class ACTRADE(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("ACTRADE Cog loaded!")
        
    
        
    
    @app_commands.command(name='actrade', description='Trade another user for a character of the same rarity')
    @app_commands.describe(user="Specify the user you want to trade with",
                           give="Character you give away",
                           want="Character you want to get")
    async def actrade(self, interaction: discord.Interaction, user: discord.User, give: str, want: str):
        commanduser = interaction.user
        guild= interaction.guild
        botStats = botstatsDB.find_one({"id":573})
        if botStats['botOffline']==True:
            em = discord.Embed(title = f"ACtrade - {commanduser.name}\nThe bot is rebooting...\nTry again in a few minutes.",color = getColor('botColor'))
            em.set_thumbnail(url = commanduser.avatar)
            await interaction.response.send_message(embed=em)
            return
        
        #await send_logs_actrade(commanduser, guild, "actrade",member,characterGive,characterRecieve)
    
        characterGive=give.lower()
        characterRecieve=want.lower()

        member = user
        
        if member.id == commanduser.id:
            em = discord.Embed(title = "ACtrade",description=f"Can't trade with yourself!!",color = discord.Color.teal())
            em.set_thumbnail(url = commanduser.avatar)
            await interaction.response.send_message(embed=em)
            return
        if characterGive == characterRecieve:
            em = discord.Embed(title = "ACtrade",description=f"Can't trade for the same character **{characterGive.capitalize()}**!",color = discord.Color.teal())
            em.set_thumbnail(url = commanduser.avatar)
            await interaction.response.send_message(embed=em)
            return


        characterRecfound = charDB.find_one({"name":characterRecieve})
        characterGivefound = charDB.find_one({"name":characterGive})

        if characterRecfound == None:
            em = discord.Embed(title = "ACtrade",description=f"Character, **{characterRecieve.capitalize()}**, not found.\nFor a list of characters do **/acbank**",color = discord.Color.teal())
            em.set_thumbnail(url = commanduser.avatar)
            await interaction.response.send_message(embed=em)
            return
        
        if characterGivefound == None:
            em = discord.Embed(title = "ACtrade",description=f"Character, **{characterGive.capitalize()}**, not found.\nFor a list of characters do **/acbank**",color = discord.Color.teal())
            em.set_thumbnail(url = commanduser.avatar)
            await interaction.response.send_message(embed=em)
            return
        
        # userhasChar = False
        # memberhasChar = False
        # guild = ctx.message.guild
        await createuser(commanduser,guild)
        await createuser(member,guild)
        await createachuser(member)
        await createachuser(commanduser)
        

        userhasChar = userDB.find_one({"id":commanduser.id, "characters":{"$elemMatch": {"name":characterGive}}})
        memberhasChar = userDB.find_one({"id":member.id, "characters":{"$elemMatch": {"name":characterRecieve}}})

        userProf = userDB.find_one({"id":commanduser.id})
        # userhasHL = False
        # try:
        #     userChars = userProf['characters']
        # except:
        #     pass
        # for x in userChars:
        #     if characterGivefound["show"] == x["show"]:
        #         if x["rarity"] == "hyperlegendary":
        #             userhasHL = True
        #             break


        # userpres = presDB.find_one({'id':commanduser.id})
        # if userpres == None:
        #     userisPres = False
        # else:
        #     userisPres = False
        #     preslist = userpres['shows']
        #     for shws in preslist:
        #         if shws['show'] == characterGivefound['show']:
        #             userisPres = True
            


        memberProf = userDB.find_one({"id":member.id})
        # memberhasHL = False
        # try:
        #     memberChars = memberProf['characters']
        # except:
        #     pass
        
        # for x in memberChars:
        #     if characterRecfound["show"] == x["show"]:
        #         if x["rarity"] == "hyperlegendary":
        #             memberhasHL = True
        #             break
        
        # memberpres = presDB.find_one({'id':member.id})
        # if memberpres == None:
        #     memberisPres = False
        # else:
        #     memberisPres = False
        #     preslist = memberpres['shows']
        #     for shws in preslist:
        #         if shws['show'] == characterRecfound['show']:
        #             memberisPres = True


        if userhasChar is None:
            em = discord.Embed(title = "ACtrade",description=f"{commanduser.name.capitalize()} doesn't have {characterGive.capitalize()} unlocked.",color = discord.Color.teal())
            em.set_thumbnail(url = commanduser.avatar)
            await interaction.response.send_message(embed=em)
            return

        if memberhasChar is None:
            em = discord.Embed(title = "ACtrade",description=f"{member.name.capitalize()} doesn't have {characterRecieve.capitalize()} unlocked.",color = discord.Color.teal())
            em.set_thumbnail(url = member.avatar)
            await interaction.response.send_message(embed=em)
            return

        if characterRecfound['rarity'] != characterGivefound['rarity']:
            em = discord.Embed(title = "ACtrade",description=f"**{characterGive.capitalize()}** is not the same rarity as **{characterRecieve.capitalize()}**.",color = discord.Color.teal())
            em.add_field(name="You can only trade characters of the same rarity.",value=f"For example:\nCommon for Common")
            em.set_thumbnail(url = commanduser.avatar)
            await interaction.response.send_message(embed=em)
            return

        if characterRecfound == "hyperlegendary" or characterGivefound == "hyperlegendary":
            em = discord.Embed(title = "ACtrade",description=f"**Hyper Legendaries can't be traded**!",color = discord.Color.teal())
            # em.add_field(name="Trade Between:",value=f"{commanduser.name.capitalize()} and {member.name.capitalize()}")
            em.set_thumbnail(url = commanduser.avatar)
            await interaction.response.send_message(embed=em)
            return
        

        characterRecieveProf = charDB.find_one({"name":characterRecieve})
        # characterGiveProf = charDB.find_one({"name":characterGive})

        # charrecievename = characterRecieveProf["name"]
        # chargivename = characterGiveProf["name"]

        # charrecieveshow = characterRecieveProf["show"]
        # chargiveshow = characterGiveProf["show"]
        
        charrecieverarity = characterRecieveProf["rarity"]
        # chargiverrarity = characterGiveProf["rarity"]

        maxRar = charDB.count_documents({"rarity":charrecieverarity})

        rcp = 0
        rcm = 0
        for chars in userProf['characters']:
            if chars['rarity'] == charrecieverarity:
                rcp += 1

        if rcp == maxRar:
            em = discord.Embed(title = "ACtrade",description=f"**{commanduser.name} has the max number of {charrecieverarity.capitalize()} characters. Please prestige at least 1 show in order to trade with this rarity",color = discord.Color.teal())
            # em.add_field(name="Trade Between:",value=f"{commanduser.name.capitalize()} and {member.name.capitalize()}")
            em.set_thumbnail(url = commanduser.avatar)
            await interaction.response.send_message(embed=em)
            return
        
        for chars in memberProf['characters']:
            if chars['rarity'] == charrecieverarity:
                rcm += 1

        if rcm == maxRar:
            em = discord.Embed(title = "ACtrade",description=f"**{member.name} has the max number of {charrecieverarity.capitalize()} characters. Please prestige at least 1 show in order to trade with this rarity",color = discord.Color.teal())
            # em.add_field(name="Trade Between:",value=f"{commanduser.name.capitalize()} and {member.name.capitalize()}")
            em.set_thumbnail(url = commanduser.avatar)
            await interaction.response.send_message(embed=em)
            return
        

        acceptPage = discord.Embed (
            title = f"ACtrade\nRarity: {charrecieverarity.capitalize()}",
            description = f"**{commanduser.name.capitalize()}** gets **{characterRecieve.capitalize()}**\n**{member.name.capitalize()}** gets **{characterGive.capitalize()}**\n\n{member.name.capitalize()} press accept to confirm the trade!\nYou have 20 seconds.",
            colour = getColor(charrecieverarity)
        )
        acceptPage.set_thumbnail(url = commanduser.avatar)
        
        

        # message = await ctx.send(embed = acceptPage,components=buttons)
        
        view = Buttons(user,commanduser,characterGive,characterRecieve)
        await interaction.response.send_message(embed=acceptPage, view=view)
        view.message = await interaction.original_response()
        
        
    #Test Command
    # @app_commands.command(name="test",description="A Test Command!")
    # async def test(self,interaction: discord.Interaction):
    #     await interaction.response.send_message(view=Buttons())    
        
        
        
async def setup(bot):
    await bot.add_cog(ACTRADE(bot))