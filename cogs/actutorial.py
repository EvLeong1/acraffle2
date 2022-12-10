import discord 
from discord import app_commands
from discord.ext import commands

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=10):
        super().__init__(timeout=timeout)
        
        
class ACTUT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("ACtut Cog loaded!")
        
    #Test Command
    @app_commands.command(name="actutorial",description="Vote for ACRaffle and get a free raffle!")
    async def actutorial(self,interaction: discord.Interaction):
        # member = interaction.user
        # guild= interaction.guild
        # view = Buttons()
        # em = discord.Embed(title = f"ACvote - {member.name}",description = f"Click the link below to watch a YouTube tutorial for ACraffle!",color = discord.Color.teal())
        # em.set_thumbnail(url = member.avatar)
        # em.set_image(url='https://pa1.narvii.com/6809/ab0f90cc948019786f61395656e31cdc924e8394_hq.gif')
        # view.add_item(discord.ui.Button(label="YouTube Link",style=discord.ButtonStyle.link,url="https://top.gg/bot/864733251166797835/vote"))
        await interaction.response.send_message('https://www.youtube.com/watch?v=hTzOGHAkqMg') 
        
        
        
async def setup(bot):
    await bot.add_cog(ACTUT(bot))