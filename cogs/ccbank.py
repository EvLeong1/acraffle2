import discord 
from discord import app_commands
from discord.ext import commands
import pymongo
import config 
import math
import random

#ACshows and AC Hyper Legendary
# acshowsPages = []

class Buttons(discord.ui.View):
    showit = 0
    def __init__(self,author,showlist,userchars,i, *, timeout=30):
        self.author = author
        self.showlist = showlist
        self.userchars = userchars
        self.i = i
        super().__init__(timeout=timeout)
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    async def on_timeout(self) -> None:
        # Step 2
        for item in self.children:
            Buttons.remove_item(self,item)

        # Step 3
        await self.message.edit(view=self)
        
    @discord.ui.button(label="First", style=discord.ButtonStyle.green,row=1)
    async def first(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.i = 0
        userChars = self.userchars
        show = self.showlist[self.i]
        amountUnlocked = 0
        member = interaction.user
        amountCharsinShow = charDB.count_documents({"show":show["name"]})
        # amountUnlocked = userDB.find({"id":member.id,"characters":{"$elemMatch":{"show":show["name"]}}})
        for y in userChars:
            if show["name"] == y["show"]:
                amountUnlocked+=1


        userpres = presDB.find_one({'id':member.id})
        if userpres == None:
            level = 0
        else:
            level = 0
            preslist = userpres['shows']
            for shws in preslist:
                if shws['show'] == show['name']:
                    level = shws['tier']

        stars = ''
        for x in range(level):
            stars += '⭐'
        
        embedDef = discord.Embed (
        title = f"CCbank - {member.name.capitalize()}\n({self.i+1}/{showDB.estimated_document_count()})",
        description = f"**{show['title']} ({show['abv']})\nUnlocked: {amountUnlocked}/{amountCharsinShow}\nPrestige: {level}**\n{stars}",
        colour = getPresCol(level)
        )
        charlist = charDB.find({"show":show['name']}).sort("rarityrank")
        embedDef.set_thumbnail(url= show['thumbnail'])
        for y in charlist:
            # tempname = y["name"]
            # #charshow=y["show"]
            # rarity=y["rarity"]
            charFound=False
            #print(charshow,show)
            for t in userChars:
                if y['name'] == t["name"]:
                    #addfield(pages[it],tempname,rarity,"✅")
                    embedDef.add_field(name=f"{'✅'} {y['name'].capitalize()}",value=f"{y['rarity'].capitalize()}", inline=True)
                    charFound = True
                    break
            if charFound == False:
                #addfield(pages[it],tempname,rarity,"❌")
                embedDef.add_field(name=f"{'❌'} {y['name'].capitalize()}",value=f"{y['rarity'].capitalize()}", inline=True)
        embedDef.set_footer(text=f"Page ({self.i+1}/{showDB.estimated_document_count()}) - {show['title']} ({show['abv']})")
        
        view = Buttons(interaction.user,self.showlist,self.userchars,self.i)
        await interaction.response.edit_message(embed=embedDef,view=view)
        view.message = await interaction.original_response()
        
    @discord.ui.button(label="-5", style=discord.ButtonStyle.blurple,row=2)
    async def minusFive(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.i > 5:
            self.i -= 5
            userChars = self.userchars
            show = self.showlist[self.i]
            amountUnlocked = 0
            member = interaction.user
            numshows = showDB.estimated_document_count()
            amountCharsinShow = charDB.count_documents({"show":show["name"]})
            #amountUnlocked = userDB.find({"id":member.id,"characters":{"$elemMatch":{"show":show["name"]}}})
            for y in userChars:
                if show["name"] == y["show"]:
                    amountUnlocked+=1
            userpres = presDB.find_one({'id':member.id})
            if userpres == None:
                level = 0
            else:
                level = 0
                preslist = userpres['shows']
                for shws in preslist:
                    if shws['show'] == show['name']:
                        level = shws['tier']


            stars = ''
            for x in range(level):
                stars += '⭐'
            
            embedDef = discord.Embed (
            title = f"CCbank - {member.name.capitalize()}\n({self.i+1}/{numshows})",
            description = f"**{show['title']} ({show['abv']})\nUnlocked: {amountUnlocked}/{amountCharsinShow}\nPrestige: {level}**\n{stars}",
            colour = getPresCol(level)
            )
            charlist = charDB.find({"show":show['name']}).sort("rarityrank")
            embedDef.set_thumbnail(url= show['thumbnail'])
            for y in charlist:
                # tempname = y["name"]
                # #charshow=y["show"]
                # rarity=y["rarity"]
                charFound=False
                #print(charshow,show)
                for t in userChars:
                    if y['name'] == t["name"]:
                        #addfield(pages[it],tempname,rarity,"✅")
                        embedDef.add_field(name=f"{'✅'} {y['name'].capitalize()}",value=f"{y['rarity'].capitalize()}", inline=True)
                        charFound = True
                        break
                if charFound == False:
                    #addfield(pages[it],tempname,rarity,"❌")
                    embedDef.add_field(name=f"{'❌'} {y['name'].capitalize()}",value=f"{y['rarity'].capitalize()}", inline=True)
            embedDef.set_footer(text=f"Page ({self.i+1}/{numshows}) - {show['title']} ({show['abv']})")
        view = Buttons(interaction.user,self.showlist,self.userchars,self.i)
        await interaction.response.edit_message(embed=embedDef,view=view)
        view.message = await interaction.original_response()
    
        
    @discord.ui.button(label="Prev", style=discord.ButtonStyle.gray,row=2)
    async def prev(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.i > 0:
            self.i -= 1
            userChars = self.userchars
            show = self.showlist[self.i]
            amountUnlocked = 0
            member = interaction.user
            numshows = showDB.estimated_document_count()
            amountCharsinShow = charDB.count_documents({"show":show["name"]})
            #amountUnlocked = userDB.find({"id":member.id,"characters":{"$elemMatch":{"show":show["name"]}}})
            for y in userChars:
                if show["name"] == y["show"]:
                    amountUnlocked+=1
            userpres = presDB.find_one({'id':member.id})
            if userpres == None:
                level = 0
            else:
                level = 0
                preslist = userpres['shows']
                for shws in preslist:
                    if shws['show'] == show['name']:
                        level = shws['tier']


            stars = ''
            for x in range(level):
                stars += '⭐'
            
            embedDef = discord.Embed (
            title = f"CCbank - {member.name.capitalize()}\n({self.i+1}/{numshows})",
            description = f"**{show['title']} ({show['abv']})\nUnlocked: {amountUnlocked}/{amountCharsinShow}\nPrestige: {level}**\n{stars}",
            colour = getPresCol(level)
            )
            charlist = charDB.find({"show":show['name']}).sort("rarityrank")
            embedDef.set_thumbnail(url= show['thumbnail'])
            for y in charlist:
                # tempname = y["name"]
                # #charshow=y["show"]
                # rarity=y["rarity"]
                charFound=False
                #print(charshow,show)
                for t in userChars:
                    if y['name'] == t["name"]:
                        #addfield(pages[it],tempname,rarity,"✅")
                        embedDef.add_field(name=f"{'✅'} {y['name'].capitalize()}",value=f"{y['rarity'].capitalize()}", inline=True)
                        charFound = True
                        break
                if charFound == False:
                    #addfield(pages[it],tempname,rarity,"❌")
                    embedDef.add_field(name=f"{'❌'} {y['name'].capitalize()}",value=f"{y['rarity'].capitalize()}", inline=True)
            embedDef.set_footer(text=f"Page ({self.i+1}/{numshows}) - {show['title']} ({show['abv']})")
        view = Buttons(interaction.user,self.showlist,self.userchars,self.i)
        await interaction.response.edit_message(embed=embedDef,view=view)
        view.message = await interaction.original_response()
        
    @discord.ui.button(label="Next", style=discord.ButtonStyle.gray,row=2)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        numshows = showDB.estimated_document_count()
        if self.i < numshows - 1:
            self.i += 1
            userChars = self.userchars
            show = self.showlist[self.i]
            amountUnlocked = 0
            member = interaction.user
            amountCharsinShow = charDB.count_documents({"show":show["name"]})
            #amountUnlocked = userDB.find({"id":member.id,"characters":{"$elemMatch":{"show":show["name"]}}})
            for y in userChars:
                if show["name"] == y["show"]:
                    amountUnlocked+=1
            userpres = presDB.find_one({'id':member.id})
            if userpres == None:
                level = 0
            else:
                level = 0
                preslist = userpres['shows']
                for shws in preslist:
                    if shws['show'] == show['name']:
                        level = shws['tier']


            stars = ''
            for x in range(level):
                stars += '⭐'
            
            embedDef = discord.Embed (
            title = f"CCbank - {member.name.capitalize()}\n({self.i+1}/{numshows})",
            description = f"**{show['title']} ({show['abv']})\nUnlocked: {amountUnlocked}/{amountCharsinShow}\nPrestige: {level}**\n{stars}",
            colour = getPresCol(level)
            )
            charlist = charDB.find({"show":show['name']}).sort("rarityrank")
            embedDef.set_thumbnail(url= show['thumbnail'])
            for y in charlist:
                # tempname = y["name"]
                # #charshow=y["show"]
                # rarity=y["rarity"]
                charFound=False
                #print(charshow,show)
                for t in userChars:
                    if y['name'] == t["name"]:
                        #addfield(pages[it],tempname,rarity,"✅")
                        embedDef.add_field(name=f"{'✅'} {y['name'].capitalize()}",value=f"{y['rarity'].capitalize()}", inline=True)
                        charFound = True
                        break
                if charFound == False:
                    #addfield(pages[it],tempname,rarity,"❌")
                    embedDef.add_field(name=f"{'❌'} {y['name'].capitalize()}",value=f"{y['rarity'].capitalize()}", inline=True)
            embedDef.set_footer(text=f"Page ({self.i+1}/{numshows}) - {show['title']} ({show['abv']})")
        view = Buttons(interaction.user,self.showlist,self.userchars,self.i)
        await interaction.response.edit_message(embed=embedDef,view=view)
        view.message = await interaction.original_response()
    
    @discord.ui.button(label="+5", style=discord.ButtonStyle.blurple,row=2)
    async def plusFive(self, interaction: discord.Interaction, button: discord.ui.Button):
        numshows = showDB.estimated_document_count()
        if self.i < numshows - 5:
            self.i += 5
            userChars = self.userchars
            show = self.showlist[self.i]
            amountUnlocked = 0
            member = interaction.user
            amountCharsinShow = charDB.count_documents({"show":show["name"]})
            #amountUnlocked = userDB.find({"id":member.id,"characters":{"$elemMatch":{"show":show["name"]}}})
            for y in userChars:
                if show["name"] == y["show"]:
                    amountUnlocked+=1
            userpres = presDB.find_one({'id':member.id})
            if userpres == None:
                level = 0
            else:
                level = 0
                preslist = userpres['shows']
                for shws in preslist:
                    if shws['show'] == show['name']:
                        level = shws['tier']


            stars = ''
            for x in range(level):
                stars += '⭐'
            
            embedDef = discord.Embed (
            title = f"CCbank - {member.name.capitalize()}\n({self.i+1}/{numshows})",
            description = f"**{show['title']} ({show['abv']})\nUnlocked: {amountUnlocked}/{amountCharsinShow}\nPrestige: {level}**\n{stars}",
            colour = getPresCol(level)
            )
            charlist = charDB.find({"show":show['name']}).sort("rarityrank")
            embedDef.set_thumbnail(url= show['thumbnail'])
            for y in charlist:
                # tempname = y["name"]
                # #charshow=y["show"]
                # rarity=y["rarity"]
                charFound=False
                #print(charshow,show)
                for t in userChars:
                    if y['name'] == t["name"]:
                        #addfield(pages[it],tempname,rarity,"✅")
                        embedDef.add_field(name=f"{'✅'} {y['name'].capitalize()}",value=f"{y['rarity'].capitalize()}", inline=True)
                        charFound = True
                        break
                if charFound == False:
                    #addfield(pages[it],tempname,rarity,"❌")
                    embedDef.add_field(name=f"{'❌'} {y['name'].capitalize()}",value=f"{y['rarity'].capitalize()}", inline=True)
                    
            embedDef.set_footer(text=f"Page ({self.i+1}/{numshows}) - {show['title']} ({show['abv']})")
        view = Buttons(interaction.user,self.showlist,self.userchars,self.i)
        await interaction.response.edit_message(embed=embedDef,view=view)
        view.message = await interaction.original_response()
    
    @discord.ui.button(label="Last", style=discord.ButtonStyle.green,row=1)
    async def Last(self, interaction: discord.Interaction, button: discord.ui.Button):
        userChars = self.userchars
        numshows = showDB.estimated_document_count()
        amountUnlocked = 0
        member = interaction.user
        self.i = numshows-1
        show = self.showlist[self.i]
        amountUnlocked = 0
        amountCharsinShow = charDB.count_documents({"show":show["name"]})
        # amountUnlocked = userDB.find({"id":member.id,"characters":{"$elemMatch":{"show":show["name"]}}})
        for y in userChars:
            if show["name"] == y["show"]:
                amountUnlocked+=1
        userpres = presDB.find_one({'id':member.id})
        if userpres == None:
            level = 0
        else:
            level = 0
            preslist = userpres['shows']
            for shws in preslist:
                if shws['show'] == show['name']:
                    level = shws['tier']


        stars = ''
        for x in range(level):
            stars += '⭐'
        
        embedDef = discord.Embed (
        title = f"CCbank - {member.name.capitalize()}\n({self.i+1}/{numshows})",
        description = f"**{show['title']} ({show['abv']})\nUnlocked: {amountUnlocked}/{amountCharsinShow}\nPrestige: {level}**\n{stars}",
        colour = getPresCol(level)
        )
        charlist = charDB.find({"show":show['name']}).sort("rarityrank")
        embedDef.set_thumbnail(url= show['thumbnail'])
        for y in charlist:
            # tempname = y["name"]
            # #charshow=y["show"]
            # rarity=y["rarity"]
            charFound=False
            #print(charshow,show)
            for t in userChars:
                if y['name'] == t["name"]:
                    #addfield(pages[it],tempname,rarity,"✅")
                    embedDef.add_field(name=f"{'✅'} {y['name'].capitalize()}",value=f"{y['rarity'].capitalize()}", inline=True)
                    charFound = True
                    break
            if charFound == False:
                #addfield(pages[it],tempname,rarity,"❌")
                embedDef.add_field(name=f"{'❌'} {y['name'].capitalize()}",value=f"{y['rarity'].capitalize()}", inline=True)
        embedDef.set_footer(text=f"Page ({self.i+1}/{numshows}) - {show['title']} ({show['abv']})")
        
        view = Buttons(interaction.user,self.showlist,self.userchars,self.i)
        await interaction.response.edit_message(embed=embedDef,view=view)
        view.message = await interaction.original_response()
        
    @discord.ui.button(label="Close", style=discord.ButtonStyle.red,row=1)
    async def Close(self, interaction: discord.Interaction, child: discord.ui.Button):
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

# def createPages(member):   
#     numshows = showDB.count_documents({})
#     pagesNeeded = math.ceil(numshows/15)
#     #print(pagesNeeded)

#     showlist = showDB.find().sort('title')
#     newShowsList = []
#     numInList = 1
#     for t in showlist:
#         newShowsList.append(f'{numInList}. {t["title"]} ({t["abv"]})')
#         numInList+=1
#     joinVar = '\n'

#     #print(newShowsList)
    
#     startNum = 0
#     stopNum = 15

#     for pages in range(pagesNeeded):
#         embed = discord.Embed (
#         title = f"**ACshows - User: {member.name}\nTo see the characters in a show do /ccbs show\nExample: /ccbs aot**",
#         description = f'{joinVar.join(newShowsList[i] for i in range(startNum,stopNum))}',
#         colour = getColor('botColor')
#         )
#         embed.set_thumbnail(url=member.avatar)
#         embed.set_footer(text=f'Page: ({pages+1}/{pagesNeeded})')
#         acshowsPages.append(embed)
#         startNum+=15
#         stopNum+=15
#         if stopNum >= numshows:
#             stopNum = numshows
#     return acshowsPages


async def createuser(member,guild):
    data = userDB.find_one({"id":member.id})
    if data is None:
        # guildid = guild.id
        # guildname = guild.name
        newuser = {"id": member.id,"name":member.name,"currentchar":None}
        userDB.insert_one(newuser)
        userDB.update_one({"id":member.id}, {"$set":{"favorites": [] }})
    
        # await addUniqueUser()
        return
    else:
        if data["name"] == member.name:
            return
        else:
            userDB.update_one({"id":member.id}, {"$set":{"name":member.name}})
            return
        
def getPresCol(level):
    if level == 0:
        color = discord.Color.teal()
    else:
        color = discord.Color(random.randint(0,16777215))
    return color
       
class CCBANK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("CCBANK Cog loaded!")
        
    
    @app_commands.command(name="ccbank",description="Shows a list of all the shows included in ACRaffle (Cartoons)")
    async def ccbank(self,interaction: discord.Interaction, user: discord.User):
        member = user
        guild = interaction.guild
        await createuser(member,guild)
    
        user = userDB.find_one({"id":member.id})
        try:
            userChars = user["characters"]
        except:
            em = discord.Embed(title = f"{member.name.capitalize()} hasn't unlocked any characters!\nDo */ccraffle* to get started then come back to see a list of all the characters and shows!",color = discord.Color.teal())
            em.set_thumbnail(url=member.avatar)
            await interaction.response.send_message(embed=em) 
            return

        showlist = showDB.find().sort("title")

        showlist = showlist
        numshows = showDB.estimated_document_count()

        i = 0
        show = showlist[i]
        amountUnlocked = 0
        amountCharsinShow = charDB.count_documents({"show":show["name"]})
        for y in userChars:
            if show["name"] == y["show"]:
                amountUnlocked+=1


        userpres = presDB.find_one({'id':member.id})
        if userpres == None:
            level = 0
        else:
            level = 0
            preslist = userpres['shows']
            for shws in preslist:
                if shws['show'] == show['name']:
                    level = shws['tier']

        stars = ''
        for x in range(level):
            stars += '⭐'
        
        embedDef = discord.Embed (
        title = f"CCbank - {member.name.capitalize()}\n({i+1}/{numshows})",
        description = f"**{show['title']} ({show['abv']})\nUnlocked: {amountUnlocked}/{amountCharsinShow}\nPrestige: {level}**\n{stars}",
        colour = getPresCol(level)
        )

        user = userDB.find_one({"id":member.id})
        userChars = user["characters"]
        
        charlist = charDB.find({"show":show['name']}).sort("rarityrank")
        embedDef.set_thumbnail(url= show['thumbnail'])
        for y in charlist:
            charFound=False
            for t in userChars:
                if y['name'] == t["name"]:
                    
                    embedDef.add_field(name=f"{'✅'} {y['name'].capitalize()}",value=f"{y['rarity'].capitalize()}", inline=True)
                    charFound = True
                    break
            if charFound == False:
                embedDef.add_field(name=f"{'❌'} {y['name'].capitalize()}",value=f"{y['rarity'].capitalize()}", inline=True)
        
        embedDef.set_footer(text=f"Page ({i+1}/{numshows}) - {show['title']} ({show['abv']})")
        
        chl = self.bot.get_channel(config.BANK_LOG_ID)
        await chl.send(f"**/ccbank** - User: **{interaction.user}** - Viewed: **{member.name}** - Server: **{interaction.guild}**")
        
        view = Buttons(interaction.user,showlist,userChars,0)
        await interaction.response.send_message(embed=embedDef,view=view) 
        view.message = await interaction.original_response()

   
            
        
        
        
async def setup(bot):
    await bot.add_cog(CCBANK(bot))