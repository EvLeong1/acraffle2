import discord 
import config
from discord import app_commands
from discord.ext import commands
import pymongo

cluster = pymongo.MongoClient(config.MONGOTOKEN)
botstatsDB = cluster["acrafflebot"]["botstats"]     
        
class ACAN(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("ACAN Cog loaded!")
        
    
        
  
    @app_commands.command(name='acannouncements', description='See the latest updates to ACRaffle')
    async def acannouncements(self,interaction: discord.Interaction):
        member = interaction.user
        guild= interaction.guild
        botstat = botstatsDB.find_one({"id":573})
        show1 = botstat["newshow1"]
        show2 = botstat["newshow2"]
        show3 = botstat["newshow3"]
        show4 = botstat["newshow4"]
        show5 = botstat["newshow5"]

        em = discord.Embed(title = f"ACraffle Announcements\n\nFor help and other commands use ***/achelp***\nNew? Use ***/actutorial***",color = discord.Color.teal())
        em.add_field(name= f'**Newest Shows**',value=f"{show1}\n{show2}\n{show3}\n{show4}\n{show5}",inline=False)
        em.add_field(name= f'**ACraffle is Back!**',value=f"ACRaffle now uses slash commands meaning you can find all the commands by doing /achelp and looking at the list!",inline=False)
        em.add_field(name= f'**Loading Screen Channel**',value=f"Loading Screens are pretty easy to add so feel free to suggest them in the discord. Also check the discord to see the recently added loading screens.",inline=False)
        em.add_field(name= f'**ACresetshop**',value=f"/acresetshop now lets you reset individual characters alongside a full reset.",inline=False)
        em.set_thumbnail(url=member.avatar)
        await interaction.response.send_message(embed=em)
    
    @app_commands.command(name='achelp', description='See all the commands included in ACraffle')
    async def achelp(self,interaction: discord.Interaction):
        cmdPrefix = "/"
        member = interaction.user
        guild= interaction.guild
        em = discord.Embed(title = f"AChelp - {member.name}",description = f"To get started look at **/actutorial (!actut)**\To see recent changes use **{cmdPrefix}acannouncements**\nTo see all included shows do **/acshows**",color = discord.Color.teal())
        em.add_field(name = f"**Unlocking\nCharacters**", value = f"{cmdPrefix}acraffle\n{cmdPrefix}acraffleplus\n{cmdPrefix}acrafflevote\n{cmdPrefix}actrade\n{cmdPrefix}achyperlegendary\n{cmdPrefix}acblock\n{cmdPrefix}acloadingscreen")#add acupgrade back here when updated
        em.add_field(name="**Viewing\nCharacters**", value =f"{cmdPrefix}acbankshow\n{cmdPrefix}acbankrarity\n{cmdPrefix}acpreview")
        em.add_field(name='**Profile**',value =f"{cmdPrefix}acprofile\n{cmdPrefix}acprofilecolor\n{cmdPrefix}acsetcharacter\n{cmdPrefix}acsetfavorite\n{cmdPrefix}acsetmal\n{cmdPrefix}acsetanilist\n{cmdPrefix}acsetbio\n{cmdPrefix}acpremove")#\n{cmdPrefix}acleaderboard")
        em.add_field(name='**Economy**',value =f"/acshop\n{cmdPrefix}acresetshop",inline=True)
        #em.add_field(name='**Achievements and\nPrestige**',value =f"{cmdPrefix}acachievements (!acach)\n{cmdPrefix}acprestige\n{cmdPrefix}acprestigeprofile (!acpp)",inline=True)
        #em.add_field(name='**League**',value =f"{cmdPrefix}acleague\n{cmdPrefix}acwager",inline=True)
        em.add_field(name="\u200B",value='[[ACraffle Discord Server]](https://discord.gg/DjSCcaUpTg)   [[Bot Invite]](https://discord.com/api/oauth2/authorize?client_id=864733251166797835&permissions=286784&scope=bot)',inline=False)

        
        await interaction.response.send_message(embed=em)
        

        
        
        
async def setup(bot):
    await bot.add_cog(ACAN(bot))