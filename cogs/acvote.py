import discord 
from discord import app_commands
from discord.ext import commands

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=10):
        super().__init__(timeout=timeout)
        
        
class ACVOTE(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("ACvote Cog loaded!")
        
    #Test Command
    @app_commands.command(name="acvote",description="Vote for ACRaffle and get a free raffle!")
    async def acvote(self,interaction: discord.Interaction):
        member = interaction.user
        guild= interaction.guild
        view = Buttons()
        em = discord.Embed(title = f"ACvote - {member.name}",description = f"Click the link below to vote for ACraffle!\nVoting gives you **One Vote Credit** which is the equivalent to an **/acrp**.\n\nYou can access your vote credits by doing **/acrvote**",color = discord.Color.teal())
        em.set_thumbnail(url = member.avatar)
        em.set_image(url='https://pa1.narvii.com/6809/ab0f90cc948019786f61395656e31cdc924e8394_hq.gif')
        view.add_item(discord.ui.Button(label="Vote Here!",style=discord.ButtonStyle.link,url="https://top.gg/bot/864733251166797835/vote"))
        await interaction.response.send_message(embed=em,view=view) 
        
        
        
async def setup(bot):
    await bot.add_cog(ACVOTE(bot))