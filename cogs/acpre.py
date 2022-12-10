import discord 
import config
from discord import app_commands
from discord.ext import commands
import pymongo

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
        
class ACPRE(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("ACPRE Cog loaded!")
        
    
        
    @app_commands.command(name='acpreview', description='Previews a Character')
    async def acpreview(self,interaction: discord.Interaction,character: str):
        member = interaction.user
        guild= interaction.guild
        
        character=character.lower()
        characterFound = charDB.find_one({"name":character})
        if characterFound == None:
            em = discord.Embed(title = "ACpreview",description=f"Character, **{character.capitalize()}**, not found.\nFor a list of characters you can trade do **/acbankshow *show***",color = discord.Color.teal())
            em.set_thumbnail(url = member.avatar)
            await interaction.response.send_message(embed=em)
            return
    
        hasChar = userDB.find_one({'id':member.id},{"characters":{"$elemMatch": {"name":character}}})
        owned = '❌'
        try:
            chList = hasChar['characters']
            owned = '✅'
        except:
            owned = '❌'


        usersWithChar = userDB.count_documents({"characters":{"$elemMatch": {"name":character}}})
    
        charname = characterFound["name"]
        show = showDB.find_one({"name":characterFound["show"]})
        rarity = characterFound["rarity"]
        gif = characterFound["gif"]
        if usersWithChar == 1:
            em = discord.Embed(title = f"ACpreview - {member.name}" ,description= f"**Name:** {charname.capitalize()} {owned}\n**Show:** {show['title']}\n**Rarity:** {rarity.capitalize()}\n**Stats**: {usersWithChar} person has {charname.capitalize()} unlocked",color = getColor(rarity))
            
        else:
            em = discord.Embed(title = f"ACpreview - {member.name}" ,description= f"**Name:** {charname.capitalize()} {owned}\n**Show:** {show['title']}\n**Rarity:** {rarity.capitalize()}\n**Stats**: {usersWithChar} people have {charname.capitalize()} unlocked",color = getColor(rarity))
        
        em.set_image(url=gif)
        em.set_thumbnail(url=member.avatar)
        # await send_logs_preview(member,guild,character)
        await interaction.response.send_message(embed=em)
        
    #Test Command
    # @app_commands.command(name="test",description="A Test Command!")
    # async def test(self,interaction: discord.Interaction):
    #     await interaction.response.send_message(view=Buttons())    
        
        
        
async def setup(bot):
    await bot.add_cog(ACPRE(bot))