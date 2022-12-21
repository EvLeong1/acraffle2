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
        em.add_field(name= f'**CCraffle**',value=f"**NEW Cartoon Character Raffle!** These shows are seperate from ACraffle meaning you have different cooldowns, shops, and banks. Do **/achelp Cartoon** for all commands and check the ACraffle Discord for full announcement.",inline=False)
        em.add_field(name= f'**ACraffle is Back!**',value=f"ACRaffle now uses slash commands meaning you can find all the commands by doing /achelp and looking at the list!",inline=False)
        em.add_field(name= f'**ACresetshop**',value=f"/acresetshop now lets you reset individual characters alongside a full reset. (Seperate command for CCshop)",inline=False)
        em.set_thumbnail(url=member.avatar)
        await interaction.response.send_message(embed=em)
    
    @app_commands.command(name='achelp', description='See all the commands included in ACraffle')
    @app_commands.choices(type=[
        discord.app_commands.Choice(name='Anime',value=1),
        discord.app_commands.Choice(name='Cartoon',value=2)
    ])
    async def achelp(self,interaction: discord.Interaction, type:  discord.app_commands.Choice[int]):
        cmdPrefix = "/"
        member = interaction.user
        guild= interaction.guild
        if type.value == 1:
            em = discord.Embed(title = f"AChelp - {member.name}",description = f"To get started look at **/actutorial**\nTo see recent changes use **{cmdPrefix}acannouncements**\nTo see all included shows do **/acshows**\nTo Invite the bot to your own server click **Add To Server** on its profile",color = discord.Color.teal())
            em.add_field(name = f"**Unlocking\nCharacters**", value = f"{cmdPrefix}acraffle\n{cmdPrefix}acrp\n{cmdPrefix}acrv\n{cmdPrefix}actrade\n{cmdPrefix}achyperlegendary\n{cmdPrefix}acblock\n{cmdPrefix}acloadingscreen")#add acupgrade back here when updated
            em.add_field(name="**Viewing\nCharacters**", value =f"{cmdPrefix}acbs\n{cmdPrefix}acbr\n/acbank\n{cmdPrefix}acpreview")
            em.add_field(name='**Profile**',value =f"{cmdPrefix}acprofile\n{cmdPrefix}acprofilecolor\n{cmdPrefix}acprofilecharacter\n{cmdPrefix}acprofilefavorite\n{cmdPrefix}acprofilemal\n{cmdPrefix}acprofileanilist\n{cmdPrefix}acprofilebio\n{cmdPrefix}acprofileremove")#\n{cmdPrefix}acleaderboard")
            em.add_field(name='**Economy**',value =f"/acshop\n{cmdPrefix}acresetshop",inline=True)
            #em.add_field(name='**Achievements and\nPrestige**',value =f"{cmdPrefix}acachievements (/acach)\n{cmdPrefix}acprestige\n{cmdPrefix}acprestigeprofile (/acpp)",inline=True)
            #em.add_field(name='**League**',value =f"{cmdPrefix}acleague\n{cmdPrefix}acwager",inline=True)
            em.add_field(name="\u200B",value='[[ACraffle Discord Server]](https://discord.gg/DjSCcaUpTg)',inline=False)
        if type.value == 2:
            em = discord.Embed(title = f"AChelp - {member.name}",description = f"To get started look at **/actutorial**\nTo see recent changes use **{cmdPrefix}acannouncements**\nTo see all included shows do **/ccshows**\nTo Invite the bot to your own server click **Add To Server** on its profile",color = discord.Color.teal())
            em.add_field(name = f"**Unlocking\nCharacters**", value = f"{cmdPrefix}ccraffle\n{cmdPrefix}ccrp\n{cmdPrefix}ccrv\n{cmdPrefix}cctrade\n{cmdPrefix}cchyperlegendary\n{cmdPrefix}ccloadingscreen")#add acupgrade back here when updated
            em.add_field(name="**Viewing\nCharacters**", value =f"{cmdPrefix}ccbs\n{cmdPrefix}ccbr\n/ccbank\n{cmdPrefix}acpreview")
            em.add_field(name='**Profile**',value =f"{cmdPrefix}acprofile\n{cmdPrefix}acprofilecolor\n{cmdPrefix}acprofilecharacter\n{cmdPrefix}acprofilefavorite\n{cmdPrefix}acprofilemal\n{cmdPrefix}acprofileanilist\n{cmdPrefix}acprofilebio\n{cmdPrefix}acprofileremove")#\n{cmdPrefix}acleaderboard")
            em.add_field(name='**Economy**',value =f"/ccshop\n{cmdPrefix}ccresetshop",inline=True)
            #em.add_field(name='**Achievements and\nPrestige**',value =f"{cmdPrefix}acachievements (/acach)\n{cmdPrefix}acprestige\n{cmdPrefix}acprestigeprofile (/acpp)",inline=True)
            #em.add_field(name='**League**',value =f"{cmdPrefix}acleague\n{cmdPrefix}acwager",inline=True)
            em.add_field(name="\u200B",value='[[ACraffle Discord Server]](https://discord.gg/DjSCcaUpTg)',inline=False)
        
        await interaction.response.send_message(embed=em)
        

        
        
        
async def setup(bot):
    await bot.add_cog(ACAN(bot))