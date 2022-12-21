import discord 
import config
from discord import app_commands
from discord.ext import commands
import pymongo
import datetime
import random

cluster = pymongo.MongoClient(config.MONGOTOKEN)

botstatsDB = cluster["acrafflebot"]["botstats"]

charDB = cluster["acraffleCartoon"]["characters"]
userDB = cluster["acraffleCartoon"]["users"]
shopDB = cluster["acraffleCartoon"]["usershops"]
showDB = cluster["acraffleCartoon"]["shows"]
presDB = cluster["acraffleCartoon"]["userprestige"]
loadingScreenDB = cluster["acraffleCartoon"]["loadingscreens"]
voteDB = cluster["acrafflebot"]["uservotes"]
moneyDB = cluster["acrafflebot"]["usershops"]

#intents = discord.Intents.default()
#bot = commands.Bot(command_prefix= '!', intents=intents, application_id = config.APP_ID)
#tree = app_commands.CommandTree(bot)
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


class TenLoading(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label= 'Loading Screen 1',value='load1'),
            discord.SelectOption(label= 'Loading Screen 2',value='load2'),
            discord.SelectOption(label= 'Loading Screen 3',value='load3'),
            discord.SelectOption(label= 'Loading Screen 4',value='load4'),
            discord.SelectOption(label= 'Loading Screen 5',value='load5'),
            discord.SelectOption(label= 'Loading Screen 6',value='load6'),
            discord.SelectOption(label= 'Loading Screen 7',value='load7'),
            discord.SelectOption(label= 'Loading Screen 8',value='load8'),
            discord.SelectOption(label= 'Loading Screen 9',value='load9'),
            discord.SelectOption(label= 'Loading Screen 10',value='load10')
        ]
        super().__init__(placeholder="Choose a Loading Screen",max_values=1, min_values=1, options=options)
        
    async def callback(self, interaction:discord.Interaction):
        member = interaction.user
        guild = interaction.guild
        if self.values[0] == 'load1':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[0])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,1,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
            
        if self.values[0] == 'load2':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[1])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,2,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load3':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[2])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,3,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load4':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[3])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,4,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load5':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[4])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,5,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load6':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[5])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,6,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load7':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[6])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,7,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load8':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[7])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,8,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load9':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[8])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,9,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load10':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[9])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,10,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
            
class NineLoading(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label= 'Loading Screen 1',value='load1'),
            discord.SelectOption(label= 'Loading Screen 2',value='load2'),
            discord.SelectOption(label= 'Loading Screen 3',value='load3'),
            discord.SelectOption(label= 'Loading Screen 4',value='load4'),
            discord.SelectOption(label= 'Loading Screen 5',value='load5'),
            discord.SelectOption(label= 'Loading Screen 6',value='load6'),
            discord.SelectOption(label= 'Loading Screen 7',value='load7'),
            discord.SelectOption(label= 'Loading Screen 8',value='load8'),
            discord.SelectOption(label= 'Loading Screen 9',value='load9')
        ]
        super().__init__(placeholder="Choose a Loading Screen",max_values=1, min_values=1, options=options)
        
    async def callback(self, interaction:discord.Interaction):
        member = interaction.user
        guild = interaction.guild
        if self.values[0] == 'load1':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[0])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,1,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
            
        if self.values[0] == 'load2':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[1])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,2,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load3':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[2])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,3,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load4':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[3])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,4,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load5':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[4])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,5,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load6':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[5])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,6,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load7':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[6])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,7,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load8':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[7])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,8,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load9':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[8])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,9,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
            
class EightLoading(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label= 'Loading Screen 1',value='load1'),
            discord.SelectOption(label= 'Loading Screen 2',value='load2'),
            discord.SelectOption(label= 'Loading Screen 3',value='load3'),
            discord.SelectOption(label= 'Loading Screen 4',value='load4'),
            discord.SelectOption(label= 'Loading Screen 5',value='load5'),
            discord.SelectOption(label= 'Loading Screen 6',value='load6'),
            discord.SelectOption(label= 'Loading Screen 7',value='load7'),
            discord.SelectOption(label= 'Loading Screen 8',value='load8')
        ]
        super().__init__(placeholder="Choose a Loading Screen",max_values=1, min_values=1, options=options)
        
    async def callback(self, interaction:discord.Interaction):
        member = interaction.user
        guild = interaction.guild
        if self.values[0] == 'load1':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[0])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,1,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
            
        if self.values[0] == 'load2':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[1])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,2,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load3':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[2])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,3,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load4':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[3])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,4,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load5':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[4])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,5,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load6':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[5])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,6,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load7':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[6])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,7,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load8':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[7])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,8,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        
class SevenLoading(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label= 'Loading Screen 1',value='load1'),
            discord.SelectOption(label= 'Loading Screen 2',value='load2'),
            discord.SelectOption(label= 'Loading Screen 3',value='load3'),
            discord.SelectOption(label= 'Loading Screen 4',value='load4'),
            discord.SelectOption(label= 'Loading Screen 5',value='load5'),
            discord.SelectOption(label= 'Loading Screen 6',value='load6'),
            discord.SelectOption(label= 'Loading Screen 7',value='load7')
        ]
        super().__init__(placeholder="Choose a Loading Screen",max_values=1, min_values=1, options=options)
        
    async def callback(self, interaction:discord.Interaction):
        member = interaction.user
        guild = interaction.guild
        if self.values[0] == 'load1':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[0])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,1,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
            
        if self.values[0] == 'load2':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[1])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,2,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load3':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[2])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,3,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load4':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[3])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,4,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load5':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[4])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,5,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load6':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[5])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,6,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load7':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[6])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,7,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
            
class SixLoading(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label= 'Loading Screen 1',value='load1'),
            discord.SelectOption(label= 'Loading Screen 2',value='load2'),
            discord.SelectOption(label= 'Loading Screen 3',value='load3'),
            discord.SelectOption(label= 'Loading Screen 4',value='load4'),
            discord.SelectOption(label= 'Loading Screen 5',value='load5'),
            discord.SelectOption(label= 'Loading Screen 6',value='load6')
        ]
        super().__init__(placeholder="Choose a Loading Screen",max_values=1, min_values=1, options=options)
        
    async def callback(self, interaction:discord.Interaction):
        member = interaction.user
        guild = interaction.guild
        if self.values[0] == 'load1':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[0])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,1,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
            
        if self.values[0] == 'load2':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[1])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,2,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load3':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[2])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,3,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load4':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[3])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,4,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load5':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[4])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,5,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load6':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[5])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,6,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
            
class FiveLoading(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label= 'Loading Screen 1',value='load1'),
            discord.SelectOption(label= 'Loading Screen 2',value='load2'),
            discord.SelectOption(label= 'Loading Screen 3',value='load3'),
            discord.SelectOption(label= 'Loading Screen 4',value='load4'),
            discord.SelectOption(label= 'Loading Screen 5',value='load5')
        ]
        super().__init__(placeholder="Choose a Loading Screen",max_values=1, min_values=1, options=options)
        
    async def callback(self, interaction:discord.Interaction):
        member = interaction.user
        guild = interaction.guild
        if self.values[0] == 'load1':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[0])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,1,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
            
        if self.values[0] == 'load2':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[1])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,2,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load3':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[2])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,3,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load4':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[3])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,4,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load5':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[4])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,5,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
            
class FourLoading(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label= 'Loading Screen 1',value='load1'),
            discord.SelectOption(label= 'Loading Screen 2',value='load2'),
            discord.SelectOption(label= 'Loading Screen 3',value='load3'),
            discord.SelectOption(label= 'Loading Screen 4',value='load4')
        ]
        super().__init__(placeholder="Choose a Loading Screen",max_values=1, min_values=1, options=options)
        
    async def callback(self, interaction:discord.Interaction):
        member = interaction.user
        guild = interaction.guild
        if self.values[0] == 'load1':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[0])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,1,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
            
        if self.values[0] == 'load2':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[1])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,2,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load3':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[2])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,3,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load4':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[3])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,4,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
            
class ThreeLoading(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label= 'Loading Screen 1',value='load1'),
            discord.SelectOption(label= 'Loading Screen 2',value='load2'),
            discord.SelectOption(label= 'Loading Screen 3',value='load3')
        ]
        super().__init__(placeholder="Choose a Loading Screen",max_values=1, min_values=1, options=options)
        
    async def callback(self, interaction:discord.Interaction):
        member = interaction.user
        guild = interaction.guild
        if self.values[0] == 'load1':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[0])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,1,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
            
        if self.values[0] == 'load2':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[1])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,2,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load3':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[2])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,3,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
            
class TwoLoading(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label= 'Loading Screen 1',value='load1'),
            discord.SelectOption(label= 'Loading Screen 2',value='load2')
        ]
        super().__init__(placeholder="Choose a Loading Screen",max_values=1, min_values=1, options=options)
        
    async def callback(self, interaction:discord.Interaction):
        member = interaction.user
        guild = interaction.guild
        if self.values[0] == 'load1':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[0])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,1,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
            
        if self.values[0] == 'load2':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[1])})
            findFirstLoadingEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Press Select** to Only use this loading screen or **Press Random** to use all of them!",color = getColor('botColor'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            currentLS = userData['currentloadingscreen']
            view = Buttons(interaction.user,2,findFirstLoading,currentLS)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        
          
          
          
   #########################BUTTONS CLASSES######################################        
          
          
class Buttons(discord.ui.View):
    def __init__(self,author,pageOn,loadScreen,currentLS, *, timeout=20):
        self.author = author
        self.pageOn = pageOn
        self.loadScreen = loadScreen 
        self.currentLs = currentLS
        super().__init__(timeout=timeout)
        userData = userDB.find_one({'id':self.author.id})
        loadingScreenBank = userData['loadingscreens']
        # print(len(loadingScreenBank))
        if(len(loadingScreenBank) == 10):
            self.add_item(TenLoading())
        if(len(loadingScreenBank) == 9):
            self.add_item(NineLoading())
        if(len(loadingScreenBank) == 8):
            self.add_item(EightLoading())
        if(len(loadingScreenBank) == 7):
            self.add_item(SevenLoading())
        if(len(loadingScreenBank) == 6):
            self.add_item(SixLoading())
        if(len(loadingScreenBank) == 5):
            self.add_item(FiveLoading())
        if(len(loadingScreenBank) == 4):
            self.add_item(FourLoading())
        if(len(loadingScreenBank) == 3):
            self.add_item(ThreeLoading())
        if(len(loadingScreenBank) == 2):
            self.add_item(TwoLoading())
        
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    # async def on_timeout(self) -> None:
    #     # Step 2
    #     for item in self.children:
    #         Buttons.remove_item(self,item)

    #     # Step 3
    #     await self.message.edit(view=self)
    
        
    @discord.ui.button(label="Select", style=discord.ButtonStyle.blurple)
    async def select(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        userData = userDB.find_one({'id':member.id})
        loadingScreenBank = userData['loadingscreens']
        screenlist = []
        for screens in loadingScreenBank:
            screenlist.append(int(screens['number']))
        if self.pageOn == 1:
            findLSnew = loadingScreenDB.find_one({'number':screenlist[0]})
            userDB.update_one({"id":member.id}, {"$set":{"currentloadingscreen":findLSnew['gif']}})
         
        elif self.pageOn == 2:
            findLSnew = loadingScreenDB.find_one({'number':screenlist[1]})
            userDB.update_one({"id":member.id}, {"$set":{"currentloadingscreen":findLSnew['gif']}})
         
        elif self.pageOn == 3:
            findLSnew = loadingScreenDB.find_one({'number':screenlist[2]})
            userDB.update_one({"id":member.id}, {"$set":{"currentloadingscreen":findLSnew['gif']}})
          
        elif self.pageOn == 4:
            findLSnew = loadingScreenDB.find_one({'number':screenlist[3]})
            userDB.update_one({"id":member.id}, {"$set":{"currentloadingscreen":findLSnew['gif']}})
        elif self.pageOn == 5:
            findLSnew = loadingScreenDB.find_one({'number':screenlist[4]})
            userDB.update_one({"id":member.id}, {"$set":{"currentloadingscreen":findLSnew['gif']}})
        elif self.pageOn == 6:
            findLSnew = loadingScreenDB.find_one({'number':screenlist[5]})
            userDB.update_one({"id":member.id}, {"$set":{"currentloadingscreen":findLSnew['gif']}})
        elif self.pageOn == 7:
            findLSnew = loadingScreenDB.find_one({'number':screenlist[6]})
            userDB.update_one({"id":member.id}, {"$set":{"currentloadingscreen":findLSnew['gif']}})
        elif self.pageOn == 8:
            findLSnew = loadingScreenDB.find_one({'number':screenlist[7]})
            userDB.update_one({"id":member.id}, {"$set":{"currentloadingscreen":findLSnew['gif']}})
            
        elif self.pageOn == 9:
            findLSnew = loadingScreenDB.find_one({'number':screenlist[8]})
            userDB.update_one({"id":member.id}, {"$set":{"currentloadingscreen":findLSnew['gif']}})
           
        elif self.pageOn == 10:
            findLSnew = loadingScreenDB.find_one({'number':screenlist[9]})
            userDB.update_one({"id":member.id}, {"$set":{"currentloadingscreen":findLSnew['gif']}})
            

        
        userDB.update_one({"id":member.id}, {"$set":{"lstype":'Select'}})
        selectEm = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Loading Screen Selected**",color = discord.Color.teal())
        selectEm.set_thumbnail(url=member.avatar)
        selectEm.set_image(url=findLSnew['gif'])

        view = settoSel(interaction.user)
        await interaction.response.edit_message(embed=selectEm,view=view)
        view.message = await interaction.original_response()
        
    @discord.ui.button(label="Random", style=discord.ButtonStyle.green)
    async def random(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        newem = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"You will now get a **random** Loading Screen from your collection!",color = discord.Color.teal())
        newem.set_thumbnail(url=member.avatar)
        newem.set_image(url=self.currentLs)

        userDB.update_one({"id":member.id}, {"$set":{"lstype":'Random'}})
        #await (member,ctx.message.guild,"random","random")
        view = settoRand(interaction.user)
        await interaction.response.edit_message(embed=newem,view=view)
        view.message = await interaction.original_response()
        
        
    @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            Buttons.remove_item(self,child)
    
        view = Buttons(interaction.user,self.pageOn,self.loadScreen,self.currentLs)
        await interaction.response.edit_message(view=self)
        view.message = await interaction.original_response()
        
class ButtonsDis(discord.ui.View):
    def __init__(self,author,pageOn,loadScreen,currentLS, *, timeout=20):
        self.author = author
        self.pageOn = pageOn
        self.loadScreen = loadScreen 
        self.currentLs = currentLS
        super().__init__(timeout=timeout)
        userData = userDB.find_one({'id':self.author.id})
        loadingScreenBank = userData['loadingscreens']
        # print(len(loadingScreenBank))
        if(len(loadingScreenBank) == 10):
            self.add_item(TenLoading())
        if(len(loadingScreenBank) == 9):
            self.add_item(NineLoading())
        if(len(loadingScreenBank) == 8):
            self.add_item(EightLoading())
        if(len(loadingScreenBank) == 7):
            self.add_item(SevenLoading())
        if(len(loadingScreenBank) == 6):
            self.add_item(SixLoading())
        if(len(loadingScreenBank) == 5):
            self.add_item(FiveLoading())
        if(len(loadingScreenBank) == 4):
            self.add_item(FourLoading())
        if(len(loadingScreenBank) == 3):
            self.add_item(ThreeLoading())
        if(len(loadingScreenBank) == 2):
            self.add_item(TwoLoading())
        
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    async def on_timeout(self) -> None:
        # Step 2
        for item in self.children:
            ButtonsDis.remove_item(self,item)

        # Step 3
        await self.message.edit(view=self)
    
        
    @discord.ui.button(label="Select", style=discord.ButtonStyle.blurple,disabled=True)
    async def select(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message('priont ham')
        
        
    @discord.ui.button(label="Random", style=discord.ButtonStyle.green)
    async def random(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        newem = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"You will now get a **random** Loading Screen from your collection!",color = discord.Color.teal())
        newem.set_thumbnail(url=member.avatar)
        
        newem.set_image(url=self.currentLs)
        
        userDB.update_one({"id":member.id}, {"$set":{"lstype":'Random'}})
        print('feet')
        #await (member,ctx.message.guild,"random","random")
        view = settoRand(interaction.user)
        await interaction.response.edit_message(embed=newem,view=view)
        view.message = await interaction.original_response()
        
        
    @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            Buttons.remove_item(self,child)
    
        view = Buttons(interaction.user,self.pageOn,self.loadScreen,self.currentLs)
        await interaction.response.edit_message(view=self)
        view.message = await interaction.original_response()
        
class settoRand(discord.ui.View):
    def __init__(self,author, *, timeout=20):
        self.author = author
        super().__init__(timeout=timeout)
        userData = userDB.find_one({'id':self.author.id})
        loadingScreenBank = userData['loadingscreens']
        # print(len(loadingScreenBank))
        if(len(loadingScreenBank) == 10):
            self.add_item(TenLoading())
        if(len(loadingScreenBank) == 9):
            self.add_item(NineLoading())
        if(len(loadingScreenBank) == 8):
            self.add_item(EightLoading())
        if(len(loadingScreenBank) == 7):
            self.add_item(SevenLoading())
        if(len(loadingScreenBank) == 6):
            self.add_item(SixLoading())
        if(len(loadingScreenBank) == 5):
            self.add_item(FiveLoading())
        if(len(loadingScreenBank) == 4):
            self.add_item(FourLoading())
        if(len(loadingScreenBank) == 3):
            self.add_item(ThreeLoading())
        if(len(loadingScreenBank) == 2):
            self.add_item(TwoLoading())
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id

        
    @discord.ui.button(label="Set To Random", style=discord.ButtonStyle.green, disabled=True)
    async def random(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked me!")
        

class settoSel(discord.ui.View):
    def __init__(self,author, *, timeout=20):
        self.author = author
        super().__init__(timeout=timeout)
        userData = userDB.find_one({'id':self.author.id})
        loadingScreenBank = userData['loadingscreens']
        # print(len(loadingScreenBank))
        if(len(loadingScreenBank) == 10):
            self.add_item(TenLoading())
        if(len(loadingScreenBank) == 9):
            self.add_item(NineLoading())
        if(len(loadingScreenBank) == 8):
            self.add_item(EightLoading())
        if(len(loadingScreenBank) == 7):
            self.add_item(SevenLoading())
        if(len(loadingScreenBank) == 6):
            self.add_item(SixLoading())
        if(len(loadingScreenBank) == 5):
            self.add_item(FiveLoading())
        if(len(loadingScreenBank) == 4):
            self.add_item(FourLoading())
        if(len(loadingScreenBank) == 3):
            self.add_item(ThreeLoading())
        if(len(loadingScreenBank) == 2):
            self.add_item(TwoLoading())
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id

    @discord.ui.button(label="Selected Loading Screen", style=discord.ButtonStyle.green, disabled=True)
    async def setSel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked me!")
              
        
class CCLS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("CCLS Cog loaded!")
        
        
    @app_commands.command(name='ccloadingscreen', description='View all of your owned loading screens (Max 10)')
    async def ccloadingscreen(self,interaction: discord.Interaction):
        member = interaction.user
        botstat = botstatsDB.find_one({'id':573})
        if botstat['botOffline']==True :
            em = discord.Embed(title = f"CCloadingscreen - {member.name}\nThe bot is rebooting...\nTry again in a few minutes.",color = getColor('botColor'))
            em.set_thumbnail(url = member.avatar)
            await interaction.response.send_message(embed=em)
            return
        userProfile = userDB.find_one({'id':member.id})
        
        screenList = []
        amntScreens=0
        try:
            userScreens = userProfile['loadingscreens']
            for x in userScreens:
                amntScreens+=1
                screenList.append(int(x['number']))
        except:
            pass

        try:
            currentLS = userProfile['currentloadingscreen']
        except:
            try:
                findLS = loadingScreenDB.find_one({'number':screenList[0]})
                userDB.update_one({"id":member.id}, {"$set":{"currentloadingscreen":findLS['gif']}})
                currentLS = findLS['gif']
                userProfile = userDB.find_one({'id':member.id})
            except:
                em = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"You don't have any unlocked Loading Screens!\nYou can buy loading screens in the shop (/acshop) for ${botstat['lsbaseprice']}",color = discord.Color.teal())
                em.set_thumbnail(url=member.avatar)
                await interaction.response.send_message(embed=em)
                return


        try:
            lstype = userProfile['lstype']
        except:
            userDB.update_one({"id":member.id}, {"$set":{"lstype":'Select'}})
            lstype = 'Select'
            userProfile = userDB.find_one({'id':member.id})


        if amntScreens==0:
            em = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"You don't have any unlocked Loading Screens!\nYou can buy loading screens in the shop (/acshop) for ${botstat['lsbaseprice']}",color = discord.Color.teal())
            em.set_thumbnail(url=member.avatar)
            await interaction.response.send_message(embed=em)
            return

        elif amntScreens == 1:
            em = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Current Loading Screen**",color = discord.Color.teal())
            em.set_thumbnail(url=member.avatar)
            em.set_image(url=currentLS)
            
            await interaction.response.send_message(embed=em)
            return
        else:
            em = discord.Embed(title = f"CCloadingscreen - {member.name}",description=f"**Current Loading Screen**\n**Type: {userProfile['lstype']}**",color = discord.Color.teal())
            em.set_thumbnail(url=member.avatar)
            em.set_image(url=currentLS)
            
        
            view = ButtonsDis(interaction.user,1,screenList[1],currentLS)
            await interaction.response.send_message(embed=em,view=view)
            view.message = await interaction.original_response()
            
            
        
async def setup(bot):
    await bot.add_cog(CCLS(bot))



