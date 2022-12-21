import discord 
from discord import app_commands
from discord.ext import commands
import pymongo
import config 
import math

#ACshows and AC Hyper Legendary
acshowsPages = []

class Buttons(discord.ui.View):
    showit = 0
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
        
    @discord.ui.button(label="Prev", style=discord.ButtonStyle.gray)
    async def prev(self, interaction: discord.Interaction, button: discord.ui.Button):
        if  Buttons.showit > 0:
            Buttons.showit -= 1
        #print(Buttons.showit)
        view = Buttons(interaction.user)
        await interaction.response.edit_message(embed=acshowsPages[Buttons.showit],view=view)
        view.message = await interaction.original_response()
        
    @discord.ui.button(label="Next", style=discord.ButtonStyle.gray)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        numshows = showDB.count_documents({})
        pagesNeeded = math.ceil(numshows/15)
        if Buttons.showit < pagesNeeded-1:
            Buttons.showit += 1
        #print((Buttons.showit))
        view = Buttons(interaction.user)
        await interaction.response.edit_message(embed=acshowsPages[Buttons.showit],view=view)
        view.message = await interaction.original_response()
        
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, child: discord.ui.Button):
        for child in self.children:
            Buttons.remove_item(self,child)
    
        await interaction.response.edit_message(view=self)
        
        
        
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

def updateHyperLeg(member):
    user = userDB.find_one({"id":member.id})
    HypLeg = 0
    for x in user["characters"]:
        if x["rarity"] == "hyperlegendary":
            HypLeg+=1
            
    userDB.update_one({"id":member.id}, {"$set":{"hypersunlocked":HypLeg}})
        
        
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

def createPages(member):   
    numshows = showDB.count_documents({})
    pagesNeeded = math.ceil(numshows/15)
    #print(pagesNeeded)

    showlist = showDB.find().sort('title')
    newShowsList = []
    numInList = 1
    for t in showlist:
        newShowsList.append(f'{numInList}. {t["title"]} ({t["abv"]})')
        numInList+=1
    joinVar = '\n'

    #print(newShowsList)
    
    startNum = 0
    if showDB.estimated_document_count() < 15:
        stopNum = showDB.estimated_document_count()
    else:
        stopNum = 15

    for pages in range(pagesNeeded):
        embed = discord.Embed (
        title = f"**CCShows - User: {member.name}\nTo see the characters in a show do /ccbs show\nExample: /ccbs atla**",
        description = f'{joinVar.join(newShowsList[i] for i in range(startNum,stopNum))}',
        colour = getColor('botColor')
        )
        embed.set_thumbnail(url=member.avatar)
        embed.set_footer(text=f'Page: ({pages+1}/{pagesNeeded})')
        acshowsPages.append(embed)
        startNum+=15
        stopNum+=15
        if stopNum >= numshows:
            stopNum = numshows
    return acshowsPages
       
class CCSHOWS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("CCShows Cog loaded!")
        
    
    @app_commands.command(name="ccshows",description="Shows a list of all the shows included in ACRaffle")
    async def ccshows(self,interaction: discord.Interaction):
        member = interaction.user
        botStats = botstatsDB.find_one({"id":573})
       
        if botStats['botOffline']==True:
            em = discord.Embed(title = f"ACsetfavorite - {member.name}\nThe bot is rebooting...\nTry again in a few minutes.",color = getColor('botColor'))
            em.set_thumbnail(url = member.avatar_url)
            await interaction.response.send_message(embed=em) 
            return
    
        acshowsPages = createPages(member=member)
        
        view = Buttons(interaction.user)
        await interaction.response.send_message(embed=acshowsPages[0],view=view) 
        view.message = await interaction.original_response()

    @app_commands.command(name="cchyperlegendary",description="Claim the Hyper Legendary once you collect all the chacracters in a show!")
    async def cchyperlegendary(self,interaction: discord.Interaction, show: str):   
        member = interaction.user
        guild = interaction.guild
        
        #botstat = botstatsDB.find_one({"id":573})
        inshowlist = False 
        showlist = showDB.find().sort("name")
        for p in showlist:
            if show == p["name"]:
                showfound = showDB.find_one({"name":show})
                inshowlist = True
                break
            elif show == p["abv"]:
                show = p["name"]
                showfound = showDB.find_one({"name":show})
                inshowlist = True
                break
        if inshowlist==False:
            em = discord.Embed(title = "CChyperlegendary",description=f"Show: **{show}** not found.\nTo see all shows do **/acshows**",color = discord.Color.teal())
            em.set_thumbnail(url = member.avatar)
            await interaction.response.send_message(embed=em) 
        
        
        amountCharsinShow = charDB.count_documents({"show":show})
        # print(amountCharsinShow)
        i = 0
        user = userDB.find_one({"id":member.id})
        userchars = user["characters"]
        hashypleg = False
        for p in userchars:
            if p["show"] == show:
                i+=1
            if p["show"] == show and p["rarity"] == "hyperlegendary":
                hashypleg = True


        if (amountCharsinShow-1) == i and hashypleg == False:
            charhypleg = charDB.find_one({"show":show,"rarity":"hyperlegendary"})
            charhyplegname = charhypleg["name"]
            charhyplegshow = charhypleg["show"]
            charhyplegrarity = charhypleg["rarity"]
            charhypleggif = charhypleg["gif"]
            userDB.update_one({"id":member.id}, {"$addToSet":{"characters":{"name":charhyplegname,"show":charhyplegshow,"rarity":charhyplegrarity}}})

            em = discord.Embed(title = f"CChyperlegendary",description= f"**{member.name} claimed a Hyper Legendary!**\n**Name: {charhyplegname.capitalize()}**\nShow: {showfound['title']}\nRarity: {charhyplegrarity.capitalize()}",color = getColor("hyperlegendary"))
            em.set_thumbnail(url = member.avatar)
            em.set_image(url=charhypleggif)
            await interaction.response.send_message(embed=em)
            #await send_logs_acraffle(member, guild, "CChyperlegendary",charhyplegname)
            updateHyperLeg(member)
            

        elif hashypleg == True:
            em = discord.Embed(title = "CChyperlegendary",description=f"{member.name} already claimed the Hyper Legendary for **{showfound['title']}**.",color = getColor("hyperlegendary"))
            em.set_thumbnail(url = member.avatar)
            await interaction.response.send_message(embed=em)
            
        else:
            em = discord.Embed(title = "CChyperlegendary",description=f"{member.name} doesn't have all available characters unlocked for **{showfound['title']}**\nCheck with **/ccbs {showfound['abv']}**",color = discord.Color.teal())
            em.set_thumbnail(url = member.avatar)
            await interaction.response.send_message(embed=em)
            
        
        
        
async def setup(bot):
    await bot.add_cog(CCSHOWS(bot))