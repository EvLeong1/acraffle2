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
        
class ACPRESTIGE(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("ACPRESTIGE Cog loaded!")
        
    
        
    @app_commands.command(name='acprestige', description='Prestige a show (resets show except hyper legendary so you can recollect or earn extra money)')
    async def acprestige(self,interaction: discord.Interaction,show: str):
        member = interaction.user
        await createpres(member)
        
        showInput = show
        showInput = showInput.lower()

        try:
            showFound = showDB.find_one({'name':showInput})
        except:
            showFound = None

        if showFound == None:
            try:
                showFound = showDB.find_one({'abv':showInput})
            except:
                pass


        if showFound == None:
            em = discord.Embed(title = f"ACprestige - {member.name}" ,description=f"Show not found. To see a list of shows do **/acshows**",color = discord.Color.teal())
            em.set_thumbnail(url=member.avatar)
            await interaction.response.send_message(embed=em)
            return

        showInput = showFound['name']

        try:
            presTier = 1
            presProf = presDB.find_one({'id':member.id})
            showlist = presProf['shows']
            for x in showlist:
                if x['show'] == showInput:
                    presTier = x['tier']+1
        except:
            presTier = 1

        uprof = userDB.find_one({'id':member.id})
        userchars = uprof['characters']
        cntr = 0
        for char in userchars:
            if char['show'] == showInput:
                cntr+=1

        # hashyper = userDB.find_one({"id":member.id, "characters":{"$elemMatch": {"show":showInput,"rarity":'hyperlegendary'}}})
        charcnt = charDB.count_documents({"show":showInput})
        if charcnt != cntr:
            em = discord.Embed(title = f"ACprestige - {member.name}" ,description=f"{member.name} does not have all the characters unlocked for **{showFound['title']}**",color = discord.Color.teal())
            em.set_thumbnail(url=member.avatar)
            await interaction.response.send_message(embed=em)
            
        else:
            # print success message (include rewards for tier)
            em = discord.Embed(title = f"ACprestige - {member.name}" ,description=f"{member.name} successfully prestiged **{showFound['title']}**!\n**Prestige Tier: {presTier}**\n+{charcnt*10} SP",color = discord.Color.teal())
            em.set_thumbnail(url=member.avatar)
            
            # pull all from user db for that show
            userDB.update_one({"id":member.id}, {"$pull":{"characters":{"show":showInput,"rarity":{'$ne':'hyperlegendary'}}}})
            
            
            # set prestige to 1 in presDB
            try:
                presDB.update_one({"id":member.id}, {"$pull":{"shows":{"show":showInput}}})
                presDB.update_one({"id":member.id}, {"$addToSet":{"shows":{'show':showInput,'tier':presTier}}})
            except:
                presDB.update_one({"id":member.id}, {"$addToSet":{"shows":{'show':showInput,'tier':presTier}}})


            presProf = presDB.find_one({'id':member.id})
            showlist = presProf['shows']
            totPres = 0
            for x in showlist:
                totPres += x['tier'] 
            presDB.update_one({"id":member.id}, {"$set":{"totPres":totPres}})
            getTime = datetime.datetime.utcnow()
            presDB.update_one({"id":member.id}, {"$addToSet":{"dates":{'date':f'{getTime.month}-{getTime.day}-{getTime.year}','show':showInput,'tier':presTier}}})
            sznDB.update_one({"id":member.id}, {"$inc":{"xp":charcnt*10}})
            #await send_logs_pres(member,ctx.message.guild,showInput,presTier)
            await interaction.response.send_message(embed=em)
            
        
    #Test Command
    # @app_commands.command(name="test",description="A Test Command!")
    # async def test(self,interaction: discord.Interaction):
    #     await interaction.response.send_message(view=Buttons())    
        
        
        
async def setup(bot):
    await bot.add_cog(ACPRESTIGE(bot))