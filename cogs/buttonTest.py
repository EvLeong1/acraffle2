import discord 
import config
from discord import app_commands
from discord.ext import commands

#intents = discord.Intents.default()
#bot = commands.Bot(command_prefix= '!', intents=intents, application_id = config.APP_ID)
#tree = app_commands.CommandTree(bot)

class Buttons(discord.ui.View):
    def __init__(self,author, *, timeout=15):
        self.author = author
        super().__init__(timeout=timeout)
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    async def on_timeout(self) -> None:
        # Step 2
        for item in self.children:
            Buttons.remove_item(self,item)

        # Step 3
        await self.message.edit(view=self)
        
    @discord.ui.button(label="Click Me!", style=discord.ButtonStyle.danger)
    async def click(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked me!")
        
        
class ADMIN(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin Cog loaded!")
        
    @commands.command()
    async def syncReg(self,ctx) -> None:
        fmt = await ctx.bot.tree.sync()
        await ctx.send(f'Synced {len(fmt)} commands.')
        
    @app_commands.command(name='sync', description='Owner only')
    async def sync(self,interaction: discord.Interaction):
        if interaction.user.id == config.MY_ID:
            await self.bot.tree.sync()
            print('Command Tree Synced.')
        else:
            await interaction.response.send_message('Only Lard can use this command!')
        
    #Test Command
    # @app_commands.command(name="test",description="A Test Command!")
    # async def test(self,interaction: discord.Interaction):
    #     await interaction.response.send_message(view=Buttons())    
        
        
        
async def setup(bot):
    await bot.add_cog(ADMIN(bot))