import discord 
import config
from discord import app_commands
from discord.ext import commands
import pymongo
import datetime
import random

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

rarities = ["common", "uncommon", "rare","epic","legendary"]
bs = botstatsDB.find_one({"id":573})
uncommonprice = bs["uncommonbaseprice"]
rareprice = bs["rarebaseprice"]
epicprice = bs["epicbaseprice"]
legendaryprice = bs["legendarybaseprice"]
loadingprice = bs['lsbaseprice']

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

async def createshopuser(member,guild):
    data = shopDB.find_one({"id":member.id})
    if data is None:
        newuser = {"id": member.id,"name":member.name,'money':0}
        shopDB.insert_one(newuser)
        shopDB.update_one({"id":member.id}, {"$set":{"characterShop": [] }})
        try:
            oldProf = userDB.find_one({'id':member.id})
            try:
                shopDB.update_one({"id":member.id}, {"$set":{"money": oldProf['money']}})
                userDB.update_one({"id":member.id}, {"$unset":{"money":""}})
            except:
                pass
            try:
                userDB.update_one({"id":member.id}, {"$unset":{"characterShop":""}})
            except:
                pass
            try:
                userDB.update_one({"id":member.id}, {"$unset":{"boughtuncommon":""}})
                userDB.update_one({"id":member.id}, {"$unset":{"boughtrare":""}})
                userDB.update_one({"id":member.id}, {"$unset":{"boughtepic":""}})
                userDB.update_one({"id":member.id}, {"$unset":{"boughtlegendary":""}})
                userDB.update_one({"id":member.id}, {"$unset":{"boughtloading":""}})
            except:
                pass
            try:
                userDB.update_one({"id":member.id}, {"$unset":{"month":""}})
                userDB.update_one({"id":member.id}, {"$unset":{"tomorrow":""}})
            except:
                pass
                
        except:
            pass

        return
    else:
        if data["name"] == member.name:
            return
        else:
            shopDB.update_one({"id":member.id}, {"$set":{"name":member.name}})
            return

def updateLegendaryandEpic(member):
        user = userDB.find_one({"id":member.id})
        Leg=0
        Ep=0
        for x in user["characters"]:
            if x["rarity"] == "legendary":
                Leg+=1
            if x["rarity"] == "epic":
                Ep+=1
                
        userDB.update_one({"id":member.id}, {"$set":{"legendsunlocked":Leg}})
        userDB.update_one({"id":member.id}, {"$set":{"legunlocked":Ep}})


def updateCharsAmount(member):
        user = userDB.find_one({"id":member.id})
        userchars = len(user["characters"])
        userDB.update_one({"id":user["id"]}, {"$set":{"charsunlocked":userchars}})



#####################################################


class Select(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label= 'Home',value='option1',emoji='🏠'),
            discord.SelectOption(label= 'Uncommon',value='option2',emoji='🟩'),
            discord.SelectOption(label= 'Rare',value='option3',emoji='🟦'),
            discord.SelectOption(label= 'Epic',value='option4',emoji='🟪'),
            discord.SelectOption(label= 'Legendary 1',value='option5',emoji='🟨'),
            discord.SelectOption(label= 'Legendary 2',value='option6',emoji='🟨'),
            discord.SelectOption(label= 'Loading Screen',value='option7',emoji='🖼️')
        ]
        super().__init__(placeholder="Choose an Option",max_values=1, min_values=1, options=options)
        
    async def callback(self, interaction:discord.Interaction):
        member = interaction.user
        guild = interaction.guild
        if self.values[0] == 'option1':
            #print('home')
            user = shopDB.find_one({"id":member.id})
            usermoney = user["money"]
            gethour = datetime.datetime.utcnow()
            currenthour = gethour.hour
            currentminute = gethour.minute
            homeem = discord.Embed(title = f"ACraffle Character Shop - {member.name}",description = f"\n**Time Until Next Reset: {23 - currenthour} hours {60-currentminute} minutes**\nTo reset your shop manually: **/acresetshop**\n\n**User Balance: ${usermoney}**", color = discord.Color.teal())
            homeem.set_thumbnail(url = member.avatar)
            homeem.set_image(url="https://media1.tenor.com/images/52950888781d0f27f61df71442f176cd/tenor.gif?itemid=5078001")
            await interaction.response.edit_message(embed=homeem,view=homeComp(interaction.user))

        if self.values[0] == 'option2':
            # print('uncommon')
            user = shopDB.find_one({"id":member.id})
            usermoney = user["money"]
            gethour = datetime.datetime.utcnow()
            currenthour = gethour.hour
            currentminute = gethour.minute
            userShop = user["characterShop"]
            charShoplist = []
            for x in userShop:
                try:
                    charShoplist.append(x["name"])
                except:
                    charShoplist.append(x["number"])
            
            uncommonChar = charDB.find_one({"name":charShoplist[0]})
            showOut = showDB.find_one({'name':uncommonChar['show']})
            uncommonem = discord.Embed(title = f"ACraffle Character Shop - {member.name}",color = getColor(uncommonChar['rarity']))
            uncommonem.add_field(name=f"{uncommonChar['name'].capitalize()}",value=f"**Show:** {showOut['title']} ({showOut['abv']})\n**Rarity:** {uncommonChar['rarity'].capitalize()}",inline=True)
            uncommonem.add_field(name="Price",value=f"${uncommonprice}",inline=True)
            uncommonem.add_field(name="User Balance",value=f"${usermoney}",inline=True)
            uprof = userDB.find_one({"id":member.id})
            
            uchars = uprof['characters']
            owned = False
            for char in uchars:
                if char['name'] == uncommonChar['name']:
                    owned = True
                    break
            if owned == True:
                uncommonem.add_field(name="**Owned**",value=f"✅",inline=True)
            else:
                uncommonem.add_field(name="**Owned**",value=f"❌",inline=True)
            uncommonem.set_image(url = uncommonChar['gif'])
            uncommonem.set_thumbnail(url = member.avatar)
            
            if(user['money'] < uncommonprice and user["boughtuncommon"] == False ):
                await interaction.response.edit_message(embed=uncommonem,view=NotEnoughMoneyComp(interaction.user))
            elif (user["boughtuncommon"] == False):
                await interaction.response.edit_message(embed=uncommonem,view=buyCompUn(interaction.user))
            else:
                await interaction.response.edit_message(embed=uncommonem,view=boughtComp(interaction.user))
                
        if self.values[0] == 'option3':
            # print('rare')
            user = shopDB.find_one({"id":member.id})
            usermoney = user["money"]
            gethour = datetime.datetime.utcnow()
            currenthour = gethour.hour
            currentminute = gethour.minute
            userShop = user["characterShop"]
            charShoplist = []
            for x in userShop:
                try:
                    charShoplist.append(x["name"])
                except:
                    charShoplist.append(x["number"])
            
            rareChar = charDB.find_one({"name":charShoplist[1]})
            showOutrare = showDB.find_one({'name':rareChar['show']})
            rareem = discord.Embed(title = f"ACraffle Character Shop - {member.name}",color = getColor(rareChar['rarity']))
            rareem.add_field(name=f"**{rareChar['name'].capitalize()}**",value=f"Show: {showOutrare['title']} ({showOutrare['abv']})\nRarity: {rareChar['rarity'].capitalize()}",inline=True)
            rareem.add_field(name="**Price**",value=f"${rareprice}",inline=True)
            rareem.add_field(name="User Balance",value=f"${usermoney}",inline=True)
            uprof = userDB.find_one({"id":member.id})
            uchars = uprof['characters']
            owned = False
            for char in uchars:
                if char['name'] == rareChar['name']:
                    owned = True
                    break
            if owned == True:
                rareem.add_field(name="**Owned**",value=f"✅",inline=True)
            else:
                rareem.add_field(name="**Owned**",value=f"❌",inline=True)
            rareem.set_image(url = rareChar['gif'])
            rareem.set_thumbnail(url = member.avatar)
            
            if(user['money'] < rareprice and user["boughtrare"] == False ):
                await interaction.response.edit_message(embed=rareem,view=NotEnoughMoneyComp(interaction.user))
            elif (user["boughtrare"] == False):
                await interaction.response.edit_message(embed=rareem,view=buyCompRare(interaction.user))
            else:
                await interaction.response.edit_message(embed=rareem,view=boughtComp(interaction.user))
                
        if self.values[0] == 'option4':
            # print('epic')
            user = shopDB.find_one({"id":member.id})
            usermoney = user["money"]
            gethour = datetime.datetime.utcnow()
            currenthour = gethour.hour
            currentminute = gethour.minute
            userShop = user["characterShop"]
            charShoplist = []
            for x in userShop:
                try:
                    charShoplist.append(x["name"])
                except:
                    charShoplist.append(x["number"])
            
            epicChar = charDB.find_one({"name":charShoplist[2]})
            showOutepic = showDB.find_one({'name':epicChar['show']})
            epicem = discord.Embed(title = f"ACraffle Character Shop - {member.name}",color = getColor(epicChar['rarity']))
            epicem.add_field(name=f"{epicChar['name'].capitalize()}",value=f"**Show:** {showOutepic['title']} ({showOutepic['abv']})\n**Rarity:** {epicChar['rarity'].capitalize()}",inline=True)
            epicem.add_field(name="Price",value=f"${epicprice}",inline=True)
            epicem.add_field(name="User Balance",value=f"${usermoney}",inline=True)
            uprof = userDB.find_one({"id":member.id})
            uchars = uprof['characters']
            owned = False
            for char in uchars:
                if char['name'] == epicChar['name']:
                    owned = True
                    break
            if owned == True:
                epicem.add_field(name="**Owned**",value=f"✅",inline=True)
            else:
                epicem.add_field(name="**Owned**",value=f"❌",inline=True)
            epicem.set_image(url = epicChar['gif'])
            epicem.set_thumbnail(url = member.avatar)
            
            if(user['money'] < epicprice and user["boughtepic"] == False ):
                await interaction.response.edit_message(embed=epicem,view=NotEnoughMoneyComp(interaction.user))
            elif (user["boughtepic"] == False):
                await interaction.response.edit_message(embed=epicem,view=buyCompEpic(interaction.user))
            else:
                await interaction.response.edit_message(embed=epicem,view=boughtComp(interaction.user))
                
        if self.values[0] == 'option5':
            # print('leg 1')
            user = shopDB.find_one({"id":member.id})
            usermoney = user["money"]
            gethour = datetime.datetime.utcnow()
            currenthour = gethour.hour
            currentminute = gethour.minute
            userShop = user["characterShop"]
            charShoplist = []
            for x in userShop:
                try:
                    charShoplist.append(x["name"])
                except:
                    charShoplist.append(x["number"])
            
            legendaryChar1 = charDB.find_one({"name":charShoplist[3]})
            showOutleg = showDB.find_one({'name':legendaryChar1['show']})
            legem = discord.Embed(title = f"ACraffle Character Shop - {member.name}",color = getColor(legendaryChar1['rarity']))
            legem.add_field(name=f"{legendaryChar1['name'].capitalize()}",value=f"**Show:** {showOutleg['title']} ({showOutleg['abv']})\n**Rarity:** {legendaryChar1['rarity'].capitalize()}",inline=True)
            legem.add_field(name="Price",value=f"${legendaryprice}",inline=True)
            legem.add_field(name="User Balance",value=f"${usermoney}",inline=True)
            uprof = userDB.find_one({"id":member.id})
            uchars = uprof['characters']
            owned = False
            for char in uchars:
                if char['name'] == legendaryChar1['name']:
                    owned = True
                    break
            if owned == True:
                legem.add_field(name="**Owned**",value=f"✅",inline=True)
            else:
                legem.add_field(name="**Owned**",value=f"❌",inline=True)
            legem.set_image(url = legendaryChar1['gif'])
            legem.set_thumbnail(url = member.avatar)
            
            if(user['money'] < legendaryprice and user["boughtlegendary1"] == False ):
                await interaction.response.edit_message(embed=legem,view=NotEnoughMoneyComp(interaction.user))
            elif (user["boughtlegendary1"] == False):
                await interaction.response.edit_message(embed=legem,view=buyCompLeg1(interaction.user))
            else:
                await interaction.response.edit_message(embed=legem,view=boughtComp(interaction.user))
                
        if self.values[0] == 'option6':
            # print('leg2')
            user = shopDB.find_one({"id":member.id})
            usermoney = user["money"]
            # gethour = datetime.datetime.utcnow()
            # currenthour = gethour.hour
            # currentminute = gethour.minute
            userShop = user["characterShop"]
            charShoplist = []
            for x in userShop:
                try:
                    charShoplist.append(x["name"])
                except:
                    charShoplist.append(x["number"])
            
            legendaryChar2 = charDB.find_one({"name":charShoplist[4]})
            showOutleg2 = showDB.find_one({'name':legendaryChar2['show']})
            legem2 = discord.Embed(title = f"ACraffle Character Shop - {member.name}",color = getColor(legendaryChar2['rarity']))
            legem2.add_field(name=f"{legendaryChar2['name'].capitalize()}",value=f"**Show:** {showOutleg2['title']} ({showOutleg2['abv']})\n**Rarity:** {legendaryChar2['rarity'].capitalize()}",inline=True)
            legem2.add_field(name="Price",value=f"${legendaryprice}",inline=True)
            legem2.add_field(name="User Balance",value=f"${usermoney}")
            uprof = userDB.find_one({"id":member.id})
            uchars = uprof['characters']
            owned = False
            
            for char in uchars:
                if char['name'] == legendaryChar2['name']:
                    owned = True
                    break
            if owned == True:
                legem2.add_field(name="**Owned**",value=f"✅",inline=True)
            else:
                legem2.add_field(name="**Owned**",value=f"❌",inline=True)
            legem2.set_image(url = legendaryChar2['gif'])
            legem2.set_thumbnail(url = member.avatar)
            
            
            if(user['money'] < legendaryprice and user["boughtlegendary2"] == False ):
                await interaction.response.edit_message(embed=legem2,view=NotEnoughMoneyComp(interaction.user))
            elif (user["boughtlegendary2"] == False):
                await interaction.response.edit_message(embed=legem2,view=buyCompLeg2(interaction.user))
            else:
                await interaction.response.edit_message(embed=legem2,view=boughtComp(interaction.user))
                
        if self.values[0] == 'option7':
            # print('LS')
            user = shopDB.find_one({"id":member.id})
            usermoney = user["money"]
            gethour = datetime.datetime.utcnow()
            currenthour = gethour.hour
            currentminute = gethour.minute
            userShop = user["characterShop"]
            charShoplist = []
            for x in userShop:
                try:
                    charShoplist.append(x["name"])
                except:
                    charShoplist.append(x["number"])
                    
            loadingScreen = loadingScreenDB.find_one({"number":charShoplist[5]})
            Ls = loadingScreenDB.find_one({'number':loadingScreen['number']})
            loadingEm = discord.Embed(title = f"ACraffle Character Shop - {member.name}\nLoading Screen",color = getColor('loadingscreen'))
            loadingEm.add_field(name="Price",value=f"${loadingprice}",inline=True)
            loadingEm.add_field(name="User Balance",value=f"${usermoney}",inline=True)
            loadingEm.set_image(url = Ls['gif'])
            loadingEm.set_thumbnail(url = member.avatar)
            
            if(user['money'] < loadingprice and user["boughtloading"] == False ):
                await interaction.response.edit_message(embed=loadingEm,view=NotEnoughMoneyComp(interaction.user))
            elif (user["boughtloading"] == False):
                await interaction.response.edit_message(embed=loadingEm,view=buyCompLS(interaction.user))
            else:
                await interaction.response.edit_message(embed=loadingEm,view=boughtComp(interaction.user))









####################### TenLoadingSelectMenu ###########################


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
            findFirstLoadingEm = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**You can only have 10 loading screens! Please choose one to replace with the new one you are purchasing**",color = getColor('loadingscreen'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            view = replaceAndBuyLS1(interaction.user)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load2':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[1])})
            findFirstLoadingEm = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**You can only have 10 loading screens! Please choose one to replace with the new one you are purchasing**",color = getColor('loadingscreen'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            view = replaceAndBuyLS2(interaction.user)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load3':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[2])})
            findFirstLoadingEm = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**You can only have 10 loading screens! Please choose one to replace with the new one you are purchasing**",color = getColor('loadingscreen'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            view = replaceAndBuyLS3(interaction.user)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load4':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[3])})
            findFirstLoadingEm = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**You can only have 10 loading screens! Please choose one to replace with the new one you are purchasing**",color = getColor('loadingscreen'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            view = replaceAndBuyLS4(interaction.user)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load5':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[4])})
            findFirstLoadingEm = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**You can only have 10 loading screens! Please choose one to replace with the new one you are purchasing**",color = getColor('loadingscreen'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            view = replaceAndBuyLS5(interaction.user)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load6':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[5])})
            findFirstLoadingEm = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**You can only have 10 loading screens! Please choose one to replace with the new one you are purchasing**",color = getColor('loadingscreen'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            view = replaceAndBuyLS6(interaction.user)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load7':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[6])})
            findFirstLoadingEm = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**You can only have 10 loading screens! Please choose one to replace with the new one you are purchasing**",color = getColor('loadingscreen'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            view = replaceAndBuyLS7(interaction.user)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load8':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[7])})
            findFirstLoadingEm = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**You can only have 10 loading screens! Please choose one to replace with the new one you are purchasing**",color = getColor('loadingscreen'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            view = replaceAndBuyLS8(interaction.user)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load9':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[8])})
            findFirstLoadingEm = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**You can only have 10 loading screens! Please choose one to replace with the new one you are purchasing**",color = getColor('loadingscreen'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            view = replaceAndBuyLS9(interaction.user)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
        if self.values[0] == 'load10':
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[9])})
            findFirstLoadingEm = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**You can only have 10 loading screens! Please choose one to replace with the new one you are purchasing**",color = getColor('loadingscreen'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            
            view = replaceAndBuyLS10(interaction.user)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()
            
#################### BUTTONS ########################


class homeComp(discord.ui.View):
    def __init__(self,author, *, timeout=30):
        self.author = author
        super().__init__(timeout=timeout)
        self.add_item(Select())
        
    async def on_timeout(self) -> None:
        # Step 2
        for item in self.children:
            homeComp.remove_item(self,item)

        # Step 3
        await self.message.edit(view=self)
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    
    @discord.ui.button(label="Buy", style=discord.ButtonStyle.green,disabled=True)
    async def buyDis(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked me!")
        
    @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            homeComp.remove_item(self,child)
    
        view = homeComp(interaction.user)
        await interaction.response.edit_message(view=self)
        view.message = await interaction.original_response()

class buyCompUn(discord.ui.View):
    def __init__(self,author, *, timeout=30):
        self.author = author
        super().__init__(timeout=timeout)
        self.add_item(Select())
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    # async def on_timeout(self) -> None:
    #     # Step 2
    #     for item in self.children:
    #         buyCompUn.remove_item(self,item)

    #     # Step 3
    #     await self.message.edit(view=self)
        
    @discord.ui.button(label="Buy Uncommon", style=discord.ButtonStyle.green)
    async def buyUn(self, interaction: discord.Interaction, button: discord.ui.Button):
        priceUn = uncommonprice
        member= interaction.user
        
        user = shopDB.find_one({"id":member.id})
        userShop = user["characterShop"]
        charShoplist = []
        for x in userShop:
            try:
                charShoplist.append(x["name"])
            except:
                charShoplist.append(x["number"])
            
        uncommonChar = charDB.find_one({"name":charShoplist[0]})
        
        uncem = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**{member.name} bought {uncommonChar['name'].capitalize()}!**",color = getColor('uncommon'))
        uncem.set_image(url=uncommonChar["gif"])
        uncem.set_thumbnail(url = member.avatar_url)
            
        userDB.update_one({"id":member.id}, {"$addToSet":{"characters":{"name":uncommonChar["name"],"show":uncommonChar["show"],"rarity":uncommonChar["rarity"]}}})
        shopDB.update_one({"id":member.id}, {"$set":{"money":user["money"] - priceUn}})
        shopDB.update_one({"id":member.id}, {"$set":{"boughtuncommon":True}})

        updateLegendaryandEpic(member)
        updateCharsAmount(member)
        
        view = purchaseSuccess(interaction.user)
        await interaction.response.edit_message(embed=uncem, view=view)
        view.message = await interaction.original_response()
        
        
    @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
    async def closeUn(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            buyCompUn.remove_item(self,child)
    
        view = buyCompUn(interaction.user)
        await interaction.response.edit_message(view=self)
        view.message = await interaction.original_response()
        
class buyCompRare(discord.ui.View):
    def __init__(self,author, *, timeout=30):
        self.author = author
        super().__init__(timeout=timeout)
        self.add_item(Select())
        
    # async def on_timeout(self) -> None:
    #     # Step 2
    #     for item in self.children:
    #         buyCompRare.remove_item(self,item)

    #     # Step 3
    #     await self.message.edit(view=self)
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    @discord.ui.button(label="Buy Rare", style=discord.ButtonStyle.green)
    async def buyRare(self, interaction: discord.Interaction, button: discord.ui.Button):
        priceRare = rareprice
        member = interaction.user
        
        user = shopDB.find_one({"id":member.id})
        userShop = user["characterShop"]
        charShoplist = []
        for x in userShop:
            try:
                charShoplist.append(x["name"])
            except:
                charShoplist.append(x["number"])
            
        rareChar = charDB.find_one({"name":charShoplist[1]})
        
        rareem = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**{member.name} bought {rareChar['name'].capitalize()}!**",color = getColor('rare'))
        rareem.set_image(url=rareChar["gif"])
        rareem.set_thumbnail(url = member.avatar)
            
        userDB.update_one({"id":member.id}, {"$addToSet":{"characters":{"name":rareChar["name"],"show":rareChar["show"],"rarity":rareChar["rarity"]}}})
        shopDB.update_one({"id":member.id}, {"$set":{"money":user["money"] - priceRare}})
        shopDB.update_one({"id":member.id}, {"$set":{"boughtrare":True}})

        updateLegendaryandEpic(member)
        updateCharsAmount(member)
        
        view = purchaseSuccess(interaction.user)
        await interaction.response.edit_message(embed=rareem, view=view)
        view.message = await interaction.original_response()
        
    @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
    async def closeRare(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            buyCompRare.remove_item(self,child)
    
        view = buyCompRare(interaction.user)
        await interaction.response.edit_message(view=self)
        view.message = await interaction.original_response()
        
class buyCompEpic(discord.ui.View):
    def __init__(self,author, *, timeout=30):
        self.author = author
        super().__init__(timeout=timeout)
        self.add_item(Select())
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    # async def on_timeout(self) -> None:
    #     # Step 2
    #     for item in self.children:
    #         buyCompEpic.remove_item(self,item)

    #     # Step 3
    #     await self.message.edit(view=self)
        
    @discord.ui.button(label="Buy Epic", style=discord.ButtonStyle.green)
    async def buyEpic(self, interaction: discord.Interaction, button: discord.ui.Button):
        priceEpic = epicprice
        member = interaction.user
        
        user = shopDB.find_one({"id":member.id})
        userShop = user["characterShop"]
        charShoplist = []
        for x in userShop:
            try:
                charShoplist.append(x["name"])
            except:
                charShoplist.append(x["number"])
            
        epipChar = charDB.find_one({"name":charShoplist[2]})
        
        epicem = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**{member.name} bought {epipChar['name'].capitalize()}!**",color = getColor('epic'))
        epicem.set_image(url=epipChar["gif"])
        epicem.set_thumbnail(url = member.avatar)
            
        userDB.update_one({"id":member.id}, {"$addToSet":{"characters":{"name":epipChar["name"],"show":epipChar["show"],"rarity":epipChar["rarity"]}}})
        shopDB.update_one({"id":member.id}, {"$set":{"money":user["money"] - priceEpic}})
        shopDB.update_one({"id":member.id}, {"$set":{"boughtepic":True}})

        updateLegendaryandEpic(member)
        updateCharsAmount(member)
        
        view = purchaseSuccess(interaction.user)
        await interaction.response.edit_message(embed=epicem, view=view)
        view.message = await interaction.original_response()
        
    @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
    async def closeEpic(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            buyCompEpic.remove_item(self,child)
    
        view = buyCompEpic(interaction.user)
        await interaction.response.edit_message(view=self)
        view.message = await interaction.original_response()
        
class buyCompLeg1(discord.ui.View):
    def __init__(self,author, *, timeout=30):
        self.author = author
        super().__init__(timeout=timeout)
        self.add_item(Select())
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    # async def on_timeout(self) -> None:
    #     # Step 2
    #     for item in self.children:
    #         buyCompLeg1.remove_item(self,item)

    #     # Step 3
    #     await self.message.edit(view=self)
        
    @discord.ui.button(label="Buy Legendary 1", style=discord.ButtonStyle.green)
    async def buyLeg1(self, interaction: discord.Interaction, button: discord.ui.Button):
        priceLeg = legendaryprice
        member = interaction.user
        
        user = shopDB.find_one({"id":member.id})
        userShop = user["characterShop"]
        charShoplist = []
        for x in userShop:
            try:
                charShoplist.append(x["name"])
            except:
                charShoplist.append(x["number"])
            
        legChar = charDB.find_one({"name":charShoplist[3]})
        
        legembed1 = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**{member.name} bought {legChar['name'].capitalize()}!**",color = getColor('legendary'))
        legembed1.set_image(url=legChar["gif"])
        legembed1.set_thumbnail(url = member.avatar)
            
        userDB.update_one({"id":member.id}, {"$addToSet":{"characters":{"name":legChar["name"],"show":legChar["show"],"rarity":legChar["rarity"]}}})
        shopDB.update_one({"id":member.id}, {"$set":{"money":user["money"] - priceLeg}})
        shopDB.update_one({"id":member.id}, {"$set":{"boughtlegendary1":True}})

        updateLegendaryandEpic(member)
        updateCharsAmount(member)
        
        view = purchaseSuccess(interaction.user)
        await interaction.response.edit_message(embed=legembed1, view=view)
        view.message = await interaction.original_response()
        
    @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
    async def closeLeg1(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            buyCompLeg1.remove_item(self,child)
    
        view = buyCompLeg1(interaction.user)
        await interaction.response.edit_message(view=self)
        view.message = await interaction.original_response()
        
class buyCompLeg2(discord.ui.View):
    def __init__(self,author, *, timeout=30):
        self.author = author
        super().__init__(timeout=timeout)
        self.add_item(Select())
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
    # async def on_timeout(self) -> None:
    #     # Step 2
    #     for item in self.children:
    #         buyCompLeg2.remove_item(self,item)

    #     # Step 3
    #     await self.message.edit(view=self)
        
    @discord.ui.button(label="Buy Legendary 2", style=discord.ButtonStyle.green)
    async def buyLeg2(self, interaction: discord.Interaction, button: discord.ui.Button):
        priceLeg = legendaryprice
        member = interaction.user
        
        user = shopDB.find_one({"id":member.id})
        userShop = user["characterShop"]
        charShoplist = []
        for x in userShop:
            try:
                charShoplist.append(x["name"])
            except:
                charShoplist.append(x["number"])
            
        legChar2 = charDB.find_one({"name":charShoplist[4]})
        
        legembed2 = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**{member.name} bought {legChar2['name'].capitalize()}!**",color = getColor('legendary'))
        legembed2.set_image(url=legChar2["gif"])
        legembed2.set_thumbnail(url = member.avatar)
            
        userDB.update_one({"id":member.id}, {"$addToSet":{"characters":{"name":legChar2["name"],"show":legChar2["show"],"rarity":legChar2["rarity"]}}})
        shopDB.update_one({"id":member.id}, {"$set":{"money":user["money"] - priceLeg}})
        shopDB.update_one({"id":member.id}, {"$set":{"boughtlegendary2":True}})

        updateLegendaryandEpic(member)
        updateCharsAmount(member)
        
        view = purchaseSuccess(interaction.user)
        await interaction.response.edit_message(embed=legembed2, view=view)
        view.message = await interaction.original_response()
        
    @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
    async def closeLeg2(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            buyCompLeg2.remove_item(self,child)
    
        view = buyCompLeg2(interaction.user)
        await interaction.response.edit_message(view=self)
        view.message = await interaction.original_response()
        
class buyCompLS(discord.ui.View):
    def __init__(self,author, *, timeout=30):
        self.author = author
        super().__init__(timeout=timeout)
        self.add_item(Select())
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    # async def on_timeout(self) -> None:
    #     # Step 2
    #     for item in self.children:
    #         buyCompLS.remove_item(self,item)

    #     # Step 3
    #     await self.message.edit(view=self)
        
    @discord.ui.button(label="Buy Loading Screen", style=discord.ButtonStyle.green)
    async def buyLS(self, interaction: discord.Interaction, button: discord.ui.Button):
        i=0
        member = interaction.user
        
        user = shopDB.find_one({"id":member.id})
        userShop = user["characterShop"]
        charShoplist = []
        for x in userShop:
            try:
                charShoplist.append(x["name"])
            except:
                charShoplist.append(x["number"])
        
        loadingScreen = loadingScreenDB.find_one({"number":charShoplist[5]})
        try:
            userData = userDB.find_one({'id':member.id})
            loadingScreenBank = userData['loadingscreens']
            screenlist = []
            for screens in loadingScreenBank:
                screenlist.append(int(screens['number']))
            
            for screens in screenlist:
                i+=1
        except:
            pass
        #print(i)
        if i >= 10:
            findFirstLoading = loadingScreenDB.find_one({'number':int(screenlist[0])})
            findFirstLoadingEm = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**You can only have 10 loading screens! Please choose one to replace with the new one you are purchasing**",color = getColor('loadingscreen'))
            findFirstLoadingEm.set_image(url=findFirstLoading["gif"])
            findFirstLoadingEm.set_thumbnail(url = member.avatar)
            #print('ham')
            view = replaceAndBuyLS1(interaction.user)
            await interaction.response.edit_message(embed=findFirstLoadingEm, view=view)
            view.message = await interaction.original_response()

                    
        else:
            priceLoad = loadingprice
            loadingScreen = loadingScreenDB.find_one({"number":charShoplist[5]})
            loadEm = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**{member.name} bought the Loading Screen!**\nIt has been added to your Loading Screen collection **(/acloadingscreen)**",color = getColor('loadingscreen'))
            loadEm.set_image(url=loadingScreen["gif"])
            loadEm.set_thumbnail(url = member.avatar)

            userDB.update_one({"id":member.id}, {"$addToSet":{"loadingscreens":{"number":int(loadingScreen["number"])}}})
            shopDB.update_one({"id":member.id}, {"$set":{"money":user["money"] - priceLoad}})
            shopDB.update_one({"id":member.id}, {"$set":{"boughtloading":True}})

            updateLegendaryandEpic(member)
            updateCharsAmount(member)
            
            userDat = userDB.find_one({"id":member.id})
            try:
                currentLS = userDat['currentloadingscreen']
            except:
                try:
                    findLS = loadingScreenDB.find_one({'number':int(loadingScreen["number"])})
                    userDB.update_one({"id":member.id}, {"$set":{"currentloadingscreen":findLS['gif']}})
                    userDB.update_one({"id":member.id}, {"$set":{"lstype":'Select'}})
                except:
                    pass

            #await send_logs_shopbuy(member,guild,'loadingscreen',loadingScreen['description'])
        
            view = purchaseSuccess(interaction.user)
            await interaction.response.edit_message(embed=loadEm, view=view)
            view.message = await interaction.original_response()
        
    @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
    async def closeLS(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            buyCompLS.remove_item(self,child)
    
        view = buyCompLS(interaction.user)
        await interaction.response.edit_message(view=self)
        view.message = await interaction.original_response()

        
class boughtComp(discord.ui.View):
    def __init__(self,author, *, timeout=30):
        self.author = author
        super().__init__(timeout=timeout)
        self.add_item(Select())
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    # async def on_timeout(self) -> None:
    #     # Step 2
    #     for item in self.children:
    #         boughtComp.remove_item(self,item)

    #     # Step 3
    #     await self.message.edit(view=self)
        
    @discord.ui.button(label="Already Purchased", style=discord.ButtonStyle.danger,disabled=True)
    async def alreadyPurchased(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked me!")
        
    @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
    async def closeBoughtComp(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            boughtComp.remove_item(self,child)
    
        view = boughtComp(interaction.user)
        await interaction.response.edit_message(view=self)
        view.message = await interaction.original_response()
        
class NotEnoughMoneyComp(discord.ui.View):
    def __init__(self,author, *, timeout=30):
        self.author = author
        super().__init__(timeout=timeout)
        self.add_item(Select())
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    # async def on_timeout(self) -> None:
    #     # Step 2
    #     for item in self.children:
    #         NotEnoughMoneyComp.remove_item(self,item)

    #     # Step 3
    #     await self.message.edit(view=self)
        
    @discord.ui.button(label="Not Enough Money", style=discord.ButtonStyle.danger,disabled=True)
    async def notenoughbread(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked me!")
        
    @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
    async def closeNotEnough(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            NotEnoughMoneyComp.remove_item(self,child)
    
        view = NotEnoughMoneyComp(interaction.user)
        await interaction.response.edit_message(view=self)
        view.message = await interaction.original_response()
        
class purchaseSuccess(discord.ui.View):
    def __init__(self,author, *, timeout=30):
        self.author = author
        super().__init__(timeout=timeout)
        self.add_item(Select())
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    # async def on_timeout(self) -> None:
    #     # Step 2
    #     for item in self.children:
    #         purchaseSuccess.remove_item(self,item)

    #     # Step 3
    #     await self.message.edit(view=self)
        
    @discord.ui.button(label="Purchase Successful!", style=discord.ButtonStyle.green,disabled=True)
    async def purchSuc(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked me!")
        
    @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
    async def closePurchaseSuccess(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            purchaseSuccess.remove_item(self,child)
    
        view = purchaseSuccess(interaction.user)
        await interaction.response.edit_message(view=self)
        view.message = await interaction.original_response()
        
class replaceAndBuyLS1(discord.ui.View):
    def __init__(self,author, *, timeout=30):
        self.author = author
        super().__init__(timeout=timeout)
        self.add_item(TenLoading())
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    @discord.ui.button(label="Replace Loading Screen 1", style=discord.ButtonStyle.green)
    async def replace(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        priceLoad = loadingprice
        userData = userDB.find_one({'id':member.id})
        loadingScreenBank = userData['loadingscreens']
        screenlist = []
        for screens in loadingScreenBank:
            screenlist.append(int(screens['number']))
         
        user = shopDB.find_one({"id":member.id})
        userShop = user["characterShop"]
        charShoplist = []
        for x in userShop:
            try:
                charShoplist.append(x["name"])
            except:
                charShoplist.append(x["number"])

        loadingScreen = loadingScreenDB.find_one({"number":charShoplist[5]})
        
        loadEm = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**{member.name} bought the Loading Screen!**\nIt has been added to your Loading Screen collection **(!acls)**",color = getColor('loadingscreen'))
        loadEm.set_image(url=loadingScreen["gif"])
        loadEm.set_thumbnail(url = member.avatar)

        userProf = shopDB.find_one({"id":member.id})
        findLS = loadingScreenDB.find_one({'number':int(screenlist[0])})
        newLS = loadingScreenDB.find_one({'number':int(loadingScreen["number"])})
        userUserDB = userDB.find_one({'id':member.id})
        if userUserDB['currentloadingscreen'] == findLS['gif']:
            userDB.update_one({"id":member.id}, {"$set":{"currentloadingscreen":newLS['gif']}})

        userDB.update_one({"id":member.id}, {"$pull":{"loadingscreens":{"number":int(screenlist[0])}}})
        userDB.update_one({"id":member.id}, {"$addToSet":{"loadingscreens":{"number":int(loadingScreen["number"])}}})
        shopDB.update_one({"id":member.id}, {"$set":{"money":userProf["money"] - priceLoad}})
        shopDB.update_one({"id":member.id}, {"$set":{"boughtloading":True}})
        
        view = purchaseSuccess(interaction.user)
        await interaction.response.edit_message(embed=loadEm, view=view)
        view.message = await interaction.original_response()
        
    @discord.ui.button(label="Home", style=discord.ButtonStyle.blurple)
    async def homefromls(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = shopDB.find_one({"id":member.id})
        usermoney = user["money"]
        gethour = datetime.datetime.utcnow()
        currenthour = gethour.hour
        currentminute = gethour.minute
        homeem = discord.Embed(title = f"ACraffle Character Shop - {member.name}",description = f"\n**Time Until Next Reset: {23 - currenthour} hours {60-currentminute} minutes**\nTo reset your shop manually **/acresetshop**\n\n**User Balance: ${usermoney}**", color = discord.Color.teal())
        homeem.set_thumbnail(url = member.avatar)
        homeem.set_image(url="https://media1.tenor.com/images/52950888781d0f27f61df71442f176cd/tenor.gif?itemid=5078001")
        await interaction.response.edit_message(embed=homeem,view=homeComp(interaction.user))
    
        view = homeComp(interaction.user)
        await interaction.response.edit_message(view=view)
        view.message = await interaction.original_response()
        
class replaceAndBuyLS2(discord.ui.View):
    def __init__(self,author, *, timeout=30):
        self.author = author
        super().__init__(timeout=timeout)
        self.add_item(TenLoading())
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    @discord.ui.button(label="Replace Loading Screen 2", style=discord.ButtonStyle.green)
    async def replace(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        priceLoad = loadingprice
        userData = userDB.find_one({'id':member.id})
        loadingScreenBank = userData['loadingscreens']
        screenlist = []
        for screens in loadingScreenBank:
            screenlist.append(int(screens['number']))
         
        user = shopDB.find_one({"id":member.id})
        userShop = user["characterShop"]
        charShoplist = []
        for x in userShop:
            try:
                charShoplist.append(x["name"])
            except:
                charShoplist.append(x["number"])

        loadingScreen = loadingScreenDB.find_one({"number":charShoplist[5]})
        
        loadEm = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**{member.name} bought the Loading Screen!**\nIt has been added to your Loading Screen collection **(!acls)**",color = getColor('loadingscreen'))
        loadEm.set_image(url=loadingScreen["gif"])
        loadEm.set_thumbnail(url = member.avatar)

        userProf = shopDB.find_one({"id":member.id})
        findLS = loadingScreenDB.find_one({'number':int(screenlist[1])})
        newLS = loadingScreenDB.find_one({'number':int(loadingScreen["number"])})
        userUserDB = userDB.find_one({'id':member.id})
        if userUserDB['currentloadingscreen'] == findLS['gif']:
            userDB.update_one({"id":member.id}, {"$set":{"currentloadingscreen":newLS['gif']}})

        userDB.update_one({"id":member.id}, {"$pull":{"loadingscreens":{"number":int(screenlist[1])}}})
        userDB.update_one({"id":member.id}, {"$addToSet":{"loadingscreens":{"number":int(loadingScreen["number"])}}})
        shopDB.update_one({"id":member.id}, {"$set":{"money":userProf["money"] - priceLoad}})
        shopDB.update_one({"id":member.id}, {"$set":{"boughtloading":True}})
        
        view = purchaseSuccess(interaction.user)
        await interaction.response.edit_message(embed=loadEm, view=view)
        view.message = await interaction.original_response()
        
    @discord.ui.button(label="Home", style=discord.ButtonStyle.blurple)
    async def homefromls(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = shopDB.find_one({"id":member.id})
        usermoney = user["money"]
        gethour = datetime.datetime.utcnow()
        currenthour = gethour.hour
        currentminute = gethour.minute
        homeem = discord.Embed(title = f"ACraffle Character Shop - {member.name}",description = f"\n**Time Until Next Reset: {23 - currenthour} hours {60-currentminute} minutes**\nTo reset your shop manually **/acresetshop**\n\n**User Balance: ${usermoney}**", color = discord.Color.teal())
        homeem.set_thumbnail(url = member.avatar)
        homeem.set_image(url="https://media1.tenor.com/images/52950888781d0f27f61df71442f176cd/tenor.gif?itemid=5078001")
        await interaction.response.edit_message(embed=homeem,view=homeComp(interaction.user))
    
        view = homeComp(interaction.user)
        await interaction.response.edit_message(view=view)
        view.message = await interaction.original_response()
        
class replaceAndBuyLS3(discord.ui.View):
    def __init__(self,author, *, timeout=30):
        self.author = author
        super().__init__(timeout=timeout)
        self.add_item(TenLoading())
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    @discord.ui.button(label="Replace Loading Screen 3", style=discord.ButtonStyle.green)
    async def replace(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        priceLoad = loadingprice
        userData = userDB.find_one({'id':member.id})
        loadingScreenBank = userData['loadingscreens']
        screenlist = []
        for screens in loadingScreenBank:
            screenlist.append(int(screens['number']))
         
        user = shopDB.find_one({"id":member.id})
        userShop = user["characterShop"]
        charShoplist = []
        for x in userShop:
            try:
                charShoplist.append(x["name"])
            except:
                charShoplist.append(x["number"])

        loadingScreen = loadingScreenDB.find_one({"number":charShoplist[5]})
        
        loadEm = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**{member.name} bought the Loading Screen!**\nIt has been added to your Loading Screen collection **(!acls)**",color = getColor('loadingscreen'))
        loadEm.set_image(url=loadingScreen["gif"])
        loadEm.set_thumbnail(url = member.avatar)

        userProf = shopDB.find_one({"id":member.id})
        findLS = loadingScreenDB.find_one({'number':int(screenlist[2])})
        newLS = loadingScreenDB.find_one({'number':int(loadingScreen["number"])})
        userUserDB = userDB.find_one({'id':member.id})
        if userUserDB['currentloadingscreen'] == findLS['gif']:
            userDB.update_one({"id":member.id}, {"$set":{"currentloadingscreen":newLS['gif']}})

        userDB.update_one({"id":member.id}, {"$pull":{"loadingscreens":{"number":int(screenlist[2])}}})
        userDB.update_one({"id":member.id}, {"$addToSet":{"loadingscreens":{"number":int(loadingScreen["number"])}}})
        shopDB.update_one({"id":member.id}, {"$set":{"money":userProf["money"] - priceLoad}})
        shopDB.update_one({"id":member.id}, {"$set":{"boughtloading":True}})
        
        view = purchaseSuccess(interaction.user)
        await interaction.response.edit_message(embed=loadEm, view=view)
        view.message = await interaction.original_response()
        
    @discord.ui.button(label="Home", style=discord.ButtonStyle.blurple)
    async def homefromls(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = shopDB.find_one({"id":member.id})
        usermoney = user["money"]
        gethour = datetime.datetime.utcnow()
        currenthour = gethour.hour
        currentminute = gethour.minute
        homeem = discord.Embed(title = f"ACraffle Character Shop - {member.name}",description = f"\n**Time Until Next Reset: {23 - currenthour} hours {60-currentminute} minutes**\nTo reset your shop manually **/acresetshop**\n\n**User Balance: ${usermoney}**", color = discord.Color.teal())
        homeem.set_thumbnail(url = member.avatar)
        homeem.set_image(url="https://media1.tenor.com/images/52950888781d0f27f61df71442f176cd/tenor.gif?itemid=5078001")
        await interaction.response.edit_message(embed=homeem,view=homeComp(interaction.user))
    
        view = homeComp(interaction.user)
        await interaction.response.edit_message(view=view)
        view.message = await interaction.original_response()
        
class replaceAndBuyLS4(discord.ui.View):
    def __init__(self,author, *, timeout=30):
        self.author = author
        super().__init__(timeout=timeout)
        self.add_item(TenLoading())
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    @discord.ui.button(label="Replace Loading Screen 4", style=discord.ButtonStyle.green)
    async def replace(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        priceLoad = loadingprice
        userData = userDB.find_one({'id':member.id})
        loadingScreenBank = userData['loadingscreens']
        screenlist = []
        for screens in loadingScreenBank:
            screenlist.append(int(screens['number']))
         
        user = shopDB.find_one({"id":member.id})
        userShop = user["characterShop"]
        charShoplist = []
        for x in userShop:
            try:
                charShoplist.append(x["name"])
            except:
                charShoplist.append(x["number"])

        loadingScreen = loadingScreenDB.find_one({"number":charShoplist[5]})
        
        loadEm = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**{member.name} bought the Loading Screen!**\nIt has been added to your Loading Screen collection **(!acls)**",color = getColor('loadingscreen'))
        loadEm.set_image(url=loadingScreen["gif"])
        loadEm.set_thumbnail(url = member.avatar)

        userProf = shopDB.find_one({"id":member.id})
        findLS = loadingScreenDB.find_one({'number':int(screenlist[3])})
        newLS = loadingScreenDB.find_one({'number':int(loadingScreen["number"])})
        userUserDB = userDB.find_one({'id':member.id})
        if userUserDB['currentloadingscreen'] == findLS['gif']:
            userDB.update_one({"id":member.id}, {"$set":{"currentloadingscreen":newLS['gif']}})

        userDB.update_one({"id":member.id}, {"$pull":{"loadingscreens":{"number":int(screenlist[3])}}})
        userDB.update_one({"id":member.id}, {"$addToSet":{"loadingscreens":{"number":int(loadingScreen["number"])}}})
        shopDB.update_one({"id":member.id}, {"$set":{"money":userProf["money"] - priceLoad}})
        shopDB.update_one({"id":member.id}, {"$set":{"boughtloading":True}})
        
        view = purchaseSuccess(interaction.user)
        await interaction.response.edit_message(embed=loadEm, view=view)
        view.message = await interaction.original_response()
        
    @discord.ui.button(label="Home", style=discord.ButtonStyle.blurple)
    async def homefromls(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = shopDB.find_one({"id":member.id})
        usermoney = user["money"]
        gethour = datetime.datetime.utcnow()
        currenthour = gethour.hour
        currentminute = gethour.minute
        homeem = discord.Embed(title = f"ACraffle Character Shop - {member.name}",description = f"\n**Time Until Next Reset: {23 - currenthour} hours {60-currentminute} minutes**\nTo reset your shop manually **/acresetshop**\n\n**User Balance: ${usermoney}**", color = discord.Color.teal())
        homeem.set_thumbnail(url = member.avatar)
        homeem.set_image(url="https://media1.tenor.com/images/52950888781d0f27f61df71442f176cd/tenor.gif?itemid=5078001")
        await interaction.response.edit_message(embed=homeem,view=homeComp(interaction.user))
    
        view = homeComp(interaction.user)
        await interaction.response.edit_message(view=view)
        view.message = await interaction.original_response()
        
class replaceAndBuyLS5(discord.ui.View):
    def __init__(self,author, *, timeout=30):
        self.author = author
        super().__init__(timeout=timeout)
        self.add_item(TenLoading())
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    @discord.ui.button(label="Replace Loading Screen 5", style=discord.ButtonStyle.green)
    async def replace(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        priceLoad = loadingprice
        userData = userDB.find_one({'id':member.id})
        loadingScreenBank = userData['loadingscreens']
        screenlist = []
        for screens in loadingScreenBank:
            screenlist.append(int(screens['number']))
         
        user = shopDB.find_one({"id":member.id})
        userShop = user["characterShop"]
        charShoplist = []
        for x in userShop:
            try:
                charShoplist.append(x["name"])
            except:
                charShoplist.append(x["number"])

        loadingScreen = loadingScreenDB.find_one({"number":charShoplist[5]})
        
        loadEm = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**{member.name} bought the Loading Screen!**\nIt has been added to your Loading Screen collection **(!acls)**",color = getColor('loadingscreen'))
        loadEm.set_image(url=loadingScreen["gif"])
        loadEm.set_thumbnail(url = member.avatar)

        userProf = shopDB.find_one({"id":member.id})
        findLS = loadingScreenDB.find_one({'number':int(screenlist[4])})
        newLS = loadingScreenDB.find_one({'number':int(loadingScreen["number"])})
        userUserDB = userDB.find_one({'id':member.id})
        if userUserDB['currentloadingscreen'] == findLS['gif']:
            userDB.update_one({"id":member.id}, {"$set":{"currentloadingscreen":newLS['gif']}})

        userDB.update_one({"id":member.id}, {"$pull":{"loadingscreens":{"number":int(screenlist[4])}}})
        userDB.update_one({"id":member.id}, {"$addToSet":{"loadingscreens":{"number":int(loadingScreen["number"])}}})
        shopDB.update_one({"id":member.id}, {"$set":{"money":userProf["money"] - priceLoad}})
        shopDB.update_one({"id":member.id}, {"$set":{"boughtloading":True}})
        
        view = purchaseSuccess(interaction.user)
        await interaction.response.edit_message(embed=loadEm, view=view)
        view.message = await interaction.original_response()
    
    @discord.ui.button(label="Home", style=discord.ButtonStyle.blurple)
    async def homefromls(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = shopDB.find_one({"id":member.id})
        usermoney = user["money"]
        gethour = datetime.datetime.utcnow()
        currenthour = gethour.hour
        currentminute = gethour.minute
        homeem = discord.Embed(title = f"ACraffle Character Shop - {member.name}",description = f"\n**Time Until Next Reset: {23 - currenthour} hours {60-currentminute} minutes**\nTo reset your shop manually **/acresetshop**\n\n**User Balance: ${usermoney}**", color = discord.Color.teal())
        homeem.set_thumbnail(url = member.avatar)
        homeem.set_image(url="https://media1.tenor.com/images/52950888781d0f27f61df71442f176cd/tenor.gif?itemid=5078001")
        await interaction.response.edit_message(embed=homeem,view=homeComp(interaction.user))
    
        view = homeComp(interaction.user)
        await interaction.response.edit_message(view=view)
        view.message = await interaction.original_response()
        
class replaceAndBuyLS6(discord.ui.View):
    def __init__(self,author, *, timeout=30):
        self.author = author
        super().__init__(timeout=timeout)
        self.add_item(TenLoading())
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    @discord.ui.button(label="Replace Loading Screen 6", style=discord.ButtonStyle.green)
    async def replace(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        priceLoad = loadingprice
        userData = userDB.find_one({'id':member.id})
        loadingScreenBank = userData['loadingscreens']
        screenlist = []
        for screens in loadingScreenBank:
            screenlist.append(int(screens['number']))
         
        user = shopDB.find_one({"id":member.id})
        userShop = user["characterShop"]
        charShoplist = []
        for x in userShop:
            try:
                charShoplist.append(x["name"])
            except:
                charShoplist.append(x["number"])

        loadingScreen = loadingScreenDB.find_one({"number":charShoplist[5]})
        
        loadEm = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**{member.name} bought the Loading Screen!**\nIt has been added to your Loading Screen collection **(!acls)**",color = getColor('loadingscreen'))
        loadEm.set_image(url=loadingScreen["gif"])
        loadEm.set_thumbnail(url = member.avatar)

        userProf = shopDB.find_one({"id":member.id})
        findLS = loadingScreenDB.find_one({'number':int(screenlist[5])})
        newLS = loadingScreenDB.find_one({'number':int(loadingScreen["number"])})
        userUserDB = userDB.find_one({'id':member.id})
        if userUserDB['currentloadingscreen'] == findLS['gif']:
            userDB.update_one({"id":member.id}, {"$set":{"currentloadingscreen":newLS['gif']}})

        userDB.update_one({"id":member.id}, {"$pull":{"loadingscreens":{"number":int(screenlist[5])}}})
        userDB.update_one({"id":member.id}, {"$addToSet":{"loadingscreens":{"number":int(loadingScreen["number"])}}})
        shopDB.update_one({"id":member.id}, {"$set":{"money":userProf["money"] - priceLoad}})
        shopDB.update_one({"id":member.id}, {"$set":{"boughtloading":True}})
        
        view = purchaseSuccess(interaction.user)
        await interaction.response.edit_message(embed=loadEm, view=view)
        view.message = await interaction.original_response()
    
    @discord.ui.button(label="Home", style=discord.ButtonStyle.blurple)
    async def homefromls(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = shopDB.find_one({"id":member.id})
        usermoney = user["money"]
        gethour = datetime.datetime.utcnow()
        currenthour = gethour.hour
        currentminute = gethour.minute
        homeem = discord.Embed(title = f"ACraffle Character Shop - {member.name}",description = f"\n**Time Until Next Reset: {23 - currenthour} hours {60-currentminute} minutes**\nTo reset your shop manually **/acresetshop**\n\n**User Balance: ${usermoney}**", color = discord.Color.teal())
        homeem.set_thumbnail(url = member.avatar)
        homeem.set_image(url="https://media1.tenor.com/images/52950888781d0f27f61df71442f176cd/tenor.gif?itemid=5078001")
        await interaction.response.edit_message(embed=homeem,view=homeComp(interaction.user))
    
        view = homeComp(interaction.user)
        await interaction.response.edit_message(view=view)
        view.message = await interaction.original_response()
        
class replaceAndBuyLS7(discord.ui.View):
    def __init__(self,author, *, timeout=30):
        self.author = author
        super().__init__(timeout=timeout)
        self.add_item(TenLoading())
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    @discord.ui.button(label="Replace Loading Screen 7", style=discord.ButtonStyle.green)
    async def replace(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        priceLoad = loadingprice
        userData = userDB.find_one({'id':member.id})
        loadingScreenBank = userData['loadingscreens']
        screenlist = []
        for screens in loadingScreenBank:
            screenlist.append(int(screens['number']))
         
        user = shopDB.find_one({"id":member.id})
        userShop = user["characterShop"]
        charShoplist = []
        for x in userShop:
            try:
                charShoplist.append(x["name"])
            except:
                charShoplist.append(x["number"])

        loadingScreen = loadingScreenDB.find_one({"number":charShoplist[5]})
        
        loadEm = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**{member.name} bought the Loading Screen!**\nIt has been added to your Loading Screen collection **(!acls)**",color = getColor('loadingscreen'))
        loadEm.set_image(url=loadingScreen["gif"])
        loadEm.set_thumbnail(url = member.avatar)

        userProf = shopDB.find_one({"id":member.id})
        findLS = loadingScreenDB.find_one({'number':int(screenlist[6])})
        newLS = loadingScreenDB.find_one({'number':int(loadingScreen["number"])})
        userUserDB = userDB.find_one({'id':member.id})
        if userUserDB['currentloadingscreen'] == findLS['gif']:
            userDB.update_one({"id":member.id}, {"$set":{"currentloadingscreen":newLS['gif']}})

        userDB.update_one({"id":member.id}, {"$pull":{"loadingscreens":{"number":int(screenlist[6])}}})
        userDB.update_one({"id":member.id}, {"$addToSet":{"loadingscreens":{"number":int(loadingScreen["number"])}}})
        shopDB.update_one({"id":member.id}, {"$set":{"money":userProf["money"] - priceLoad}})
        shopDB.update_one({"id":member.id}, {"$set":{"boughtloading":True}})
        
        view = purchaseSuccess(interaction.user)
        await interaction.response.edit_message(embed=loadEm, view=view)
        view.message = await interaction.original_response()
    
    @discord.ui.button(label="Home", style=discord.ButtonStyle.blurple)
    async def homefromls(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = shopDB.find_one({"id":member.id})
        usermoney = user["money"]
        gethour = datetime.datetime.utcnow()
        currenthour = gethour.hour
        currentminute = gethour.minute
        homeem = discord.Embed(title = f"ACraffle Character Shop - {member.name}",description = f"\n**Time Until Next Reset: {23 - currenthour} hours {60-currentminute} minutes**\nTo reset your shop manually **/acresetshop**\n\n**User Balance: ${usermoney}**", color = discord.Color.teal())
        homeem.set_thumbnail(url = member.avatar)
        homeem.set_image(url="https://media1.tenor.com/images/52950888781d0f27f61df71442f176cd/tenor.gif?itemid=5078001")
        await interaction.response.edit_message(embed=homeem,view=homeComp(interaction.user))
    
        view = homeComp(interaction.user)
        await interaction.response.edit_message(view=view)
        view.message = await interaction.original_response()

class replaceAndBuyLS8(discord.ui.View):
    def __init__(self,author, *, timeout=30):
        self.author = author
        super().__init__(timeout=timeout)
        self.add_item(TenLoading())
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    @discord.ui.button(label="Replace Loading Screen 8", style=discord.ButtonStyle.green)
    async def replace(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        priceLoad = loadingprice
        userData = userDB.find_one({'id':member.id})
        loadingScreenBank = userData['loadingscreens']
        screenlist = []
        for screens in loadingScreenBank:
            screenlist.append(int(screens['number']))
         
        user = shopDB.find_one({"id":member.id})
        userShop = user["characterShop"]
        charShoplist = []
        for x in userShop:
            try:
                charShoplist.append(x["name"])
            except:
                charShoplist.append(x["number"])

        loadingScreen = loadingScreenDB.find_one({"number":charShoplist[5]})
        
        loadEm = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**{member.name} bought the Loading Screen!**\nIt has been added to your Loading Screen collection **(!acls)**",color = getColor('loadingscreen'))
        loadEm.set_image(url=loadingScreen["gif"])
        loadEm.set_thumbnail(url = member.avatar)

        userProf = shopDB.find_one({"id":member.id})
        findLS = loadingScreenDB.find_one({'number':int(screenlist[7])})
        newLS = loadingScreenDB.find_one({'number':int(loadingScreen["number"])})
        userUserDB = userDB.find_one({'id':member.id})
        if userUserDB['currentloadingscreen'] == findLS['gif']:
            userDB.update_one({"id":member.id}, {"$set":{"currentloadingscreen":newLS['gif']}})

        userDB.update_one({"id":member.id}, {"$pull":{"loadingscreens":{"number":int(screenlist[7])}}})
        userDB.update_one({"id":member.id}, {"$addToSet":{"loadingscreens":{"number":int(loadingScreen["number"])}}})
        shopDB.update_one({"id":member.id}, {"$set":{"money":userProf["money"] - priceLoad}})
        shopDB.update_one({"id":member.id}, {"$set":{"boughtloading":True}})
        
        view = purchaseSuccess(interaction.user)
        await interaction.response.edit_message(embed=loadEm, view=view)
        view.message = await interaction.original_response()
    
    @discord.ui.button(label="Home", style=discord.ButtonStyle.blurple)
    async def homefromls(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = shopDB.find_one({"id":member.id})
        usermoney = user["money"]
        gethour = datetime.datetime.utcnow()
        currenthour = gethour.hour
        currentminute = gethour.minute
        homeem = discord.Embed(title = f"ACraffle Character Shop - {member.name}",description = f"\n**Time Until Next Reset: {23 - currenthour} hours {60-currentminute} minutes**\nTo reset your shop manually **/acresetshop**\n\n**User Balance: ${usermoney}**", color = discord.Color.teal())
        homeem.set_thumbnail(url = member.avatar)
        homeem.set_image(url="https://media1.tenor.com/images/52950888781d0f27f61df71442f176cd/tenor.gif?itemid=5078001")
        await interaction.response.edit_message(embed=homeem,view=homeComp(interaction.user))
    
        view = homeComp(interaction.user)
        await interaction.response.edit_message(view=view)
        view.message = await interaction.original_response()

class replaceAndBuyLS9(discord.ui.View):
    def __init__(self,author, *, timeout=30):
        self.author = author
        super().__init__(timeout=timeout)
        self.add_item(TenLoading())
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    @discord.ui.button(label="Replace Loading Screen 9", style=discord.ButtonStyle.green)
    async def replace(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        priceLoad = loadingprice
        userData = userDB.find_one({'id':member.id})
        loadingScreenBank = userData['loadingscreens']
        screenlist = []
        for screens in loadingScreenBank:
            screenlist.append(int(screens['number']))
         
        user = shopDB.find_one({"id":member.id})
        userShop = user["characterShop"]
        charShoplist = []
        for x in userShop:
            try:
                charShoplist.append(x["name"])
            except:
                charShoplist.append(x["number"])

        loadingScreen = loadingScreenDB.find_one({"number":charShoplist[5]})
        
        loadEm = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**{member.name} bought the Loading Screen!**\nIt has been added to your Loading Screen collection **(!acls)**",color = getColor('loadingscreen'))
        loadEm.set_image(url=loadingScreen["gif"])
        loadEm.set_thumbnail(url = member.avatar)

        userProf = shopDB.find_one({"id":member.id})
        findLS = loadingScreenDB.find_one({'number':int(screenlist[8])})
        newLS = loadingScreenDB.find_one({'number':int(loadingScreen["number"])})
        userUserDB = userDB.find_one({'id':member.id})
        if userUserDB['currentloadingscreen'] == findLS['gif']:
            userDB.update_one({"id":member.id}, {"$set":{"currentloadingscreen":newLS['gif']}})

        userDB.update_one({"id":member.id}, {"$pull":{"loadingscreens":{"number":int(screenlist[8])}}})
        userDB.update_one({"id":member.id}, {"$addToSet":{"loadingscreens":{"number":int(loadingScreen["number"])}}})
        shopDB.update_one({"id":member.id}, {"$set":{"money":userProf["money"] - priceLoad}})
        shopDB.update_one({"id":member.id}, {"$set":{"boughtloading":True}})
        
        view = purchaseSuccess(interaction.user)
        await interaction.response.edit_message(embed=loadEm, view=view)
        view.message = await interaction.original_response()
        
    @discord.ui.button(label="Home", style=discord.ButtonStyle.blurple)
    async def homefromls(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = shopDB.find_one({"id":member.id})
        usermoney = user["money"]
        gethour = datetime.datetime.utcnow()
        currenthour = gethour.hour
        currentminute = gethour.minute
        homeem = discord.Embed(title = f"ACraffle Character Shop - {member.name}",description = f"\n**Time Until Next Reset: {23 - currenthour} hours {60-currentminute} minutes**\nTo reset your shop manually **/acresetshop**\n\n**User Balance: ${usermoney}**", color = discord.Color.teal())
        homeem.set_thumbnail(url = member.avatar)
        homeem.set_image(url="https://media1.tenor.com/images/52950888781d0f27f61df71442f176cd/tenor.gif?itemid=5078001")
        await interaction.response.edit_message(embed=homeem,view=homeComp(interaction.user))
    
        view = homeComp(interaction.user)
        await interaction.response.edit_message(view=view)
        view.message = await interaction.original_response()
        
class replaceAndBuyLS10(discord.ui.View):
    def __init__(self,author, *, timeout=30):
        self.author = author
        super().__init__(timeout=timeout)
        self.add_item(TenLoading())
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    @discord.ui.button(label="Replace Loading Screen 10", style=discord.ButtonStyle.green)
    async def replace(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        priceLoad = loadingprice
        userData = userDB.find_one({'id':member.id})
        loadingScreenBank = userData['loadingscreens']
        screenlist = []
        for screens in loadingScreenBank:
            screenlist.append(int(screens['number']))
         
        user = shopDB.find_one({"id":member.id})
        userShop = user["characterShop"]
        charShoplist = []
        for x in userShop:
            try:
                charShoplist.append(x["name"])
            except:
                charShoplist.append(x["number"])

        loadingScreen = loadingScreenDB.find_one({"number":charShoplist[5]})
        
        loadEm = discord.Embed(title = f"ACcharactershop - {member.name}",description=f"**{member.name} bought the Loading Screen!**\nIt has been added to your Loading Screen collection **(!acls)**",color = getColor('loadingscreen'))
        loadEm.set_image(url=loadingScreen["gif"])
        loadEm.set_thumbnail(url = member.avatar)

        userProf = shopDB.find_one({"id":member.id})
        findLS = loadingScreenDB.find_one({'number':int(screenlist[9])})
        newLS = loadingScreenDB.find_one({'number':int(loadingScreen["number"])})
        userUserDB = userDB.find_one({'id':member.id})
        if userUserDB['currentloadingscreen'] == findLS['gif']:
            userDB.update_one({"id":member.id}, {"$set":{"currentloadingscreen":newLS['gif']}})

        userDB.update_one({"id":member.id}, {"$pull":{"loadingscreens":{"number":int(screenlist[9])}}})
        userDB.update_one({"id":member.id}, {"$addToSet":{"loadingscreens":{"number":int(loadingScreen["number"])}}})
        shopDB.update_one({"id":member.id}, {"$set":{"money":userProf["money"] - priceLoad}})
        shopDB.update_one({"id":member.id}, {"$set":{"boughtloading":True}})
        
        view = purchaseSuccess(interaction.user)
        await interaction.response.edit_message(embed=loadEm, view=view)
        view.message = await interaction.original_response()
    
    @discord.ui.button(label="Home", style=discord.ButtonStyle.blurple)
    async def homefromls(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        user = shopDB.find_one({"id":member.id})
        usermoney = user["money"]
        gethour = datetime.datetime.utcnow()
        currenthour = gethour.hour
        currentminute = gethour.minute
        homeem = discord.Embed(title = f"ACraffle Character Shop - {member.name}",description = f"\n**Time Until Next Reset: {23 - currenthour} hours {60-currentminute} minutes**\nTo reset your shop manually **/acresetshop**\n\n**User Balance: ${usermoney}**", color = discord.Color.teal())
        homeem.set_thumbnail(url = member.avatar)
        homeem.set_image(url="https://media1.tenor.com/images/52950888781d0f27f61df71442f176cd/tenor.gif?itemid=5078001")
        await interaction.response.edit_message(embed=homeem,view=homeComp(interaction.user))
    
        view = homeComp(interaction.user)
        await interaction.response.edit_message(view=view)
        view.message = await interaction.original_response()
        
        
        
        
class ResetShop(discord.ui.View):
    def __init__(self,author,resetItem, *, timeout=15):
        self.author = author
        self.resetItem = resetItem
        super().__init__(timeout=timeout)
        
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id
        
    async def on_timeout(self) -> None:
        # Step 2
        for item in self.children:
            ResetShop.remove_item(self,item)

        # Step 3
        await self.message.edit(view=self)
        
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def Confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        userProf = shopDB.find_one({"id":member.id})
        
        userShop = userProf["characterShop"]
        charShoplist = []
        for x in userShop:
            try:
                charShoplist.append(x["name"])
            except:
                charShoplist.append(x["number"])
        uncommonChar = charDB.find_one({"name":charShoplist[0]})
        rareChar = charDB.find_one({"name":charShoplist[1]})
        epicChar = charDB.find_one({"name":charShoplist[2]})
        legendaryChar1 = charDB.find_one({"name":charShoplist[3]})
        legendaryChar2 = charDB.find_one({"name":charShoplist[4]})
        LoadScreener = loadingScreenDB.find_one({"number":charShoplist[5]})
        
        if self.resetItem == 1:
            def resetShop():
                shopDB.update_one({"id":member.id}, {"$set":{"boughtuncommon":False,}})

                for x in range(2):
                    # print(x)
                    randNum = random.randint(1,100000000000)
                    # randseed = int(member.id + randNum)
                    random.seed(randNum)
                    try:
                        ublocks = blockDB.find_one({'id':member.id})
                        blist = ublocks['blocklist']
                        newblist = []
                        for itm in blist:
                            newblist.append(itm['show'])
                    except:
                        newblist=[]
                    if x == 1:
                        max = charDB.count_documents({"rarity":rarities[x]})
                        randomInt = random.randint(1,max) 
                        uncChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                        while uncChar['show'] in newblist:
                            randomInt = random.randint(1,max) 
                            uncChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                        #userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":favs[0]}}})
                        #shopDB.update_one({"id":member.id}, {"$pull":{"characterShop":{"rarity":"uncommon"}}})
                        shopDB.update_one({"id":member.id,"characterShop":{"name":uncommonChar["name"],"show":uncommonChar["show"],"rarity":uncommonChar["rarity"]}}, {"$set":{"characterShop.$":{"name":uncChar["name"],"show":uncChar["show"],"rarity":uncChar["rarity"]}}})

                        
            resetShop()
            shopDB.update_one({"id":member.id}, {"$set":{"money":userProf["money"]-round(uncommonprice/2)}})
                
            em = discord.Embed(title = f"ACresetshop - {member.name}",description=f"**Shop Reset Successfully!**\nDo /acshop to check what you got",color = getColor('botColor'))
            em.set_thumbnail(url = member.avatar)
        
            for child in self.children:
                ResetShop.remove_item(self,child)
        
            view = ResetShop(interaction.user,1)
            await interaction.response.edit_message(embed=em,view=self)
            view.message = await interaction.original_response()   
            
        if self.resetItem == 2:
            def resetShop():
                shopDB.update_one({"id":member.id}, {"$set":{"boughtrare":False,}})

                for x in range(3):
                    # print(x)
                    randNum = random.randint(1,100000000000)
                    # randseed = int(member.id + randNum)
                    random.seed(randNum)
                    try:
                        ublocks = blockDB.find_one({'id':member.id})
                        blist = ublocks['blocklist']
                        newblist = []
                        for itm in blist:
                            newblist.append(itm['show'])
                    except:
                        newblist=[]
                    if x == 2:
                        max = charDB.count_documents({"rarity":rarities[x]})
                        randomInt = random.randint(1,max) 
                        uncChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                        while uncChar['show'] in newblist:
                            randomInt = random.randint(1,max) 
                            uncChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                        #userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":favs[0]}}})
                        #shopDB.update_one({"id":member.id}, {"$pull":{"characterShop":{"rarity":"uncommon"}}})
                        shopDB.update_one({"id":member.id,"characterShop":{"name":rareChar["name"],"show":rareChar["show"],"rarity":rareChar["rarity"]}}, {"$set":{"characterShop.$":{"name":uncChar["name"],"show":uncChar["show"],"rarity":uncChar["rarity"]}}})
            
                        
            resetShop()
            shopDB.update_one({"id":member.id}, {"$set":{"money":userProf["money"]-round(rareprice/2)}})
                
            em = discord.Embed(title = f"ACresetshop - {member.name}",description=f"**Shop Reset Successfully!**\nDo /acshop to check what you got",color = getColor('botColor'))
            em.set_thumbnail(url = member.avatar)
        
            for child in self.children:
                ResetShop.remove_item(self,child)
        
            view = ResetShop(interaction.user,1)
            await interaction.response.edit_message(embed=em,view=self)
            view.message = await interaction.original_response()  
        
        if self.resetItem == 3:
            def resetShop():
                shopDB.update_one({"id":member.id}, {"$set":{"boughtepic":False,}})

                for x in range(4):
                    # print(x)
                    randNum = random.randint(1,100000000000)
                    # randseed = int(member.id + randNum)
                    random.seed(randNum)
                    try:
                        ublocks = blockDB.find_one({'id':member.id})
                        blist = ublocks['blocklist']
                        newblist = []
                        for itm in blist:
                            newblist.append(itm['show'])
                    except:
                        newblist=[]
                    if x == 3:
                        max = charDB.count_documents({"rarity":rarities[x]})
                        randomInt = random.randint(1,max) 
                        uncChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                        while uncChar['show'] in newblist:
                            randomInt = random.randint(1,max) 
                            uncChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                        #userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":favs[0]}}})
                        #shopDB.update_one({"id":member.id}, {"$pull":{"characterShop":{"rarity":"uncommon"}}})
                        shopDB.update_one({"id":member.id,"characterShop":{"name":epicChar["name"],"show":epicChar["show"],"rarity":epicChar["rarity"]}}, {"$set":{"characterShop.$":{"name":uncChar["name"],"show":uncChar["show"],"rarity":uncChar["rarity"]}}})
            
                        
            resetShop()
            shopDB.update_one({"id":member.id}, {"$set":{"money":userProf["money"]-round(epicprice/2)}})
                
            em = discord.Embed(title = f"ACresetshop - {member.name}",description=f"**Shop Reset Successfully!**\nDo /acshop to check what you got",color = getColor('botColor'))
            em.set_thumbnail(url = member.avatar)
        
            for child in self.children:
                ResetShop.remove_item(self,child)
        
            view = ResetShop(interaction.user,1)
            await interaction.response.edit_message(embed=em,view=self)
            view.message = await interaction.original_response()
            
        if self.resetItem == 4:
            def resetShop():
                shopDB.update_one({"id":member.id}, {"$set":{"boughtlegendary1":False,}})

                for x in range(4):
                    # print(x)
                    randNum = random.randint(1,100000000000)
                    # randseed = int(member.id + randNum)
                    random.seed(randNum)
                    try:
                        ublocks = blockDB.find_one({'id':member.id})
                        blist = ublocks['blocklist']
                        newblist = []
                        for itm in blist:
                            newblist.append(itm['show'])
                    except:
                        newblist=[]
                    if x == 3:
                        max = charDB.count_documents({"rarity":rarities[x]})
                        randomInt = random.randint(1,max) 
                        uncChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                        while uncChar['show'] in newblist:
                            randomInt = random.randint(1,max) 
                            uncChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                        #userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":favs[0]}}})
                        #shopDB.update_one({"id":member.id}, {"$pull":{"characterShop":{"rarity":"uncommon"}}})
                        shopDB.update_one({"id":member.id,"characterShop":{"name":legendaryChar1["name"],"show":legendaryChar1["show"],"rarity":legendaryChar1["rarity"]}}, {"$set":{"characterShop.$":{"name":uncChar["name"],"show":uncChar["show"],"rarity":uncChar["rarity"]}}})
            
                        
            resetShop()
            shopDB.update_one({"id":member.id}, {"$set":{"money":userProf["money"]-round(legendaryprice/2)}})
                
            em = discord.Embed(title = f"ACresetshop - {member.name}",description=f"**Shop Reset Successfully!**\nDo /acshop to check what you got",color = getColor('botColor'))
            em.set_thumbnail(url = member.avatar)
        
            for child in self.children:
                ResetShop.remove_item(self,child)
        
            view = ResetShop(interaction.user,1)
            await interaction.response.edit_message(embed=em,view=self)
            view.message = await interaction.original_response()
            
        if self.resetItem == 5:
            def resetShop():
                shopDB.update_one({"id":member.id}, {"$set":{"boughtlegendary2":False,}})

                for x in range(5):
                    # print(x)
                    randNum = random.randint(1,100000000000)
                    # randseed = int(member.id + randNum)
                    random.seed(randNum)
                    try:
                        ublocks = blockDB.find_one({'id':member.id})
                        blist = ublocks['blocklist']
                        newblist = []
                        for itm in blist:
                            newblist.append(itm['show'])
                    except:
                        newblist=[]
                    if x == 4:
                        max = charDB.count_documents({"rarity":rarities[x]})
                        randomInt = random.randint(1,max) 
                        uncChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                        while uncChar['show'] in newblist:
                            randomInt = random.randint(1,max) 
                            uncChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                        #userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":favs[0]}}})
                        #shopDB.update_one({"id":member.id}, {"$pull":{"characterShop":{"rarity":"uncommon"}}})
                        shopDB.update_one({"id":member.id,"characterShop":{"name":legendaryChar2["name"],"show":legendaryChar2["show"],"rarity":legendaryChar2["rarity"]}}, {"$set":{"characterShop.$":{"name":uncChar["name"],"show":uncChar["show"],"rarity":uncChar["rarity"]}}})
            
                        
            resetShop()
            shopDB.update_one({"id":member.id}, {"$set":{"money":userProf["money"]-round(legendaryprice/2)}})
                
            em = discord.Embed(title = f"ACresetshop - {member.name}",description=f"**Shop Reset Successfully!**\nDo /acshop to check what you got",color = getColor('botColor'))
            em.set_thumbnail(url = member.avatar)
        
            for child in self.children:
                ResetShop.remove_item(self,child)
        
            view = ResetShop(interaction.user,1)
            await interaction.response.edit_message(embed=em,view=self)
            view.message = await interaction.original_response()
            
        if self.resetItem == 6:
            def resetShop():
                shopDB.update_one({"id":member.id}, {"$set":{"boughtloading":False,}})

                for x in range(6):
                    # print(x)
                    randNum = random.randint(1,100000000000)
                    # randseed = int(member.id + randNum)
                    random.seed(randNum)
                    try:
                        ublocks = blockDB.find_one({'id':member.id})
                        blist = ublocks['blocklist']
                        newblist = []
                        for itm in blist:
                            newblist.append(itm['show'])
                    except:
                        newblist=[]
                    if x == 5:
                        max = loadingScreenDB.count_documents({})
                        randomInt = random.randint(1,max) 
                        loadSC = loadingScreenDB.find_one({'number':randomInt})
                        #userDB.update_one({"id":member.id}, {"$pull":{"favorites":{"name":favs[0]}}})
                        #shopDB.update_one({"id":member.id}, {"$pull":{"characterShop":{"rarity":"uncommon"}}})
                        shopDB.update_one({"id":member.id,"characterShop":{"number":LoadScreener["number"]}}, {"$set":{"characterShop.$":{"number":loadSC["number"]}}})
            
                        
            resetShop()
            shopDB.update_one({"id":member.id}, {"$set":{"money":userProf["money"]-round(loadingprice/2)}})
                
            em = discord.Embed(title = f"ACresetshop - {member.name}",description=f"**Shop Reset Successfully!**\nDo /acshop to check what you got",color = getColor('botColor'))
            em.set_thumbnail(url = member.avatar)
        
            for child in self.children:
                ResetShop.remove_item(self,child)
        
            view = ResetShop(interaction.user,1)
            await interaction.response.edit_message(embed=em,view=self)
            view.message = await interaction.original_response()
            
            
            
        if self.resetItem == 7:
            def resetShop():
                shopDB.update_one({"id":member.id}, {"$set":{"boughtuncommon":False,"boughtrare":False,"boughtepic":False,"boughtlegendary1":False,"boughtlegendary2":False,"boughtloading":False}})

                for x in range(7):
                    randNum = random.randint(1,100000000000)
                    # randseed = int(member.id + randNum)
                    random.seed(randNum)
                    try:
                        ublocks = blockDB.find_one({'id':member.id})
                        blist = ublocks['blocklist']
                        newblist = []
                        for itm in blist:
                            newblist.append(itm['show'])
                    except:
                        newblist=[]
                    if x == 1:
                        max = charDB.count_documents({"rarity":rarities[x]})
                        randomInt = random.randint(1,max) 
                        uncChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                        while uncChar['show'] in newblist:
                            randomInt = random.randint(1,max) 
                            uncChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                        shopDB.update_one({"id":member.id}, {"$addToSet":{"characterShop":{"name":uncChar["name"],"show":uncChar["show"],"rarity":uncChar["rarity"]}}})
                    if x == 2:
                        max = charDB.count_documents({"rarity":rarities[x]})
                        randomInt = random.randint(1,max) 
                        rareChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                        while rareChar['show'] in newblist:
                            randomInt = random.randint(1,max) 
                            rareChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                        shopDB.update_one({"id":member.id}, {"$addToSet":{"characterShop":{"name":rareChar["name"],"show":rareChar["show"],"rarity":rareChar["rarity"]}}})
                    if x == 3:
                        max = charDB.count_documents({"rarity":rarities[x]})
                        randomInt = random.randint(1,max) 
                        epicChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                        while epicChar['show'] in newblist:
                            randomInt = random.randint(1,max) 
                            epicChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                        shopDB.update_one({"id":member.id}, {"$addToSet":{"characterShop":{"name":epicChar["name"],"show":epicChar["show"],"rarity":epicChar["rarity"]}}})
                    if x == 4:
                        max = charDB.count_documents({"rarity":rarities[x]})
                        randomInt = random.randint(1,max) 
                        legendaryChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                        while legendaryChar['show'] in newblist:
                            randomInt = random.randint(1,max) 
                            legendaryChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                        shopDB.update_one({"id":member.id}, {"$addToSet":{"characterShop":{"name":legendaryChar["name"],"show":legendaryChar["show"],"rarity":legendaryChar["rarity"]}}})
                    if x == 5:
                        max = charDB.count_documents({"rarity":rarities[4]})
                        randomInt = random.randint(1,max) 
                        legChar2 = charDB.find_one({"rarity":rarities[4], "raritynumber": randomInt})
                        while legChar2['show'] in newblist:
                            randomInt = random.randint(1,max) 
                            legChar2 = charDB.find_one({"rarity":rarities[4], "raritynumber": randomInt})
                        shopDB.update_one({"id":member.id}, {"$addToSet":{"characterShop":{"name":legChar2["name"],"show":legChar2["show"],"rarity":legChar2["rarity"]}}})
                    if x == 6:
                        max = loadingScreenDB.count_documents({})
                        randomInt = random.randint(1,max) 
                        loadingScreen = loadingScreenDB.find_one({'number':randomInt})
                        shopDB.update_one({"id":member.id}, {"$addToSet":{"characterShop":{"number":loadingScreen["number"]}}})
                        
            resetShop()
            shopDB.update_one({"id":member.id}, {"$set":{"money":userProf["money"]-3000}})
                
            em = discord.Embed(title = f"ACresetshop - {member.name}",description=f"**Shop Reset Successfully!**\nDo /acshop to check what you got",color = getColor('botColor'))
            em.set_thumbnail(url = member.avatar)
        
            for child in self.children:
                ResetShop.remove_item(self,child)
        
            view = ResetShop(interaction.user,7)
            await interaction.response.edit_message(embed=em,view=self)
            view.message = await interaction.original_response()   
        
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        em = discord.Embed(title = f"ACresetshop - {member.name}\n**Reset Canceled!**",color = getColor('botColor'))
        em.set_thumbnail(url = member.avatar)
        
        for child in self.children:
            ResetShop.remove_item(self,child)
    
        view = ResetShop(interaction.user)
        await interaction.response.edit_message(embed=em,view=self)
        view.message = await interaction.original_response()        
        
        


        
        
        
################## ACTUAL COMMAND UNDER THIS ######################
        
class ACSHOP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("ACSHOP Cog loaded!")
        
    @app_commands.command(name='acshop', description='Shop for characters! Resets Daily!')
    async def acshop(self,interaction: discord.Interaction):
        member=interaction.user
        guild = interaction.guild
        botStats = botstatsDB.find_one({"id":573})
        if botStats['botOffline']==True:
            em = discord.Embed(title = f"ACcharactershop - {member.name}\nThe bot is rebooting...\nTry again in a few minutes.",color = getColor('botColor'))
            em.set_thumbnail(url = member.avatar)
            await interaction.response.send_message(embed=em)
            return
        
        
        await createshopuser(member,guild)
        
        # em = discord.Embed(title = f"ACcharactershop - {member.name}\nLoading...",color = getColor("botColor"))
        # em.set_thumbnail(url = member.avatar)
        # message = await interaction.response.send_message(embed=em)

        todayDisplay = datetime.datetime.utcnow()
        def resetShop():
            shopDB.update_one({"id":member.id}, {"$set":{"boughtuncommon":False,"boughtrare":False,"boughtepic":False,"boughtlegendary1":False,"boughtlegendary2":False,"boughtloading":False}})

            for x in range(7):
                randNum = random.randint(1,100000000000)
                # randseed = int(member.id + randNum)
                random.seed(randNum)
                try:
                    ublocks = blockDB.find_one({'id':member.id})
                    blist = ublocks['blocklist']
                    newblist = []
                    for itm in blist:
                        newblist.append(itm['show'])
                except:
                    newblist=[]
                if x == 1:
                    max = charDB.count_documents({"rarity":rarities[x]})
                    randomInt = random.randint(1,max) 
                    uncChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                    while uncChar['show'] in newblist:
                        randomInt = random.randint(1,max) 
                        uncChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                    shopDB.update_one({"id":member.id}, {"$addToSet":{"characterShop":{"name":uncChar["name"],"show":uncChar["show"],"rarity":uncChar["rarity"]}}})
                if x == 2:
                    max = charDB.count_documents({"rarity":rarities[x]})
                    randomInt = random.randint(1,max) 
                    rareChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                    while rareChar['show'] in newblist:
                        randomInt = random.randint(1,max) 
                        rareChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                    shopDB.update_one({"id":member.id}, {"$addToSet":{"characterShop":{"name":rareChar["name"],"show":rareChar["show"],"rarity":rareChar["rarity"]}}})
                if x == 3:
                    max = charDB.count_documents({"rarity":rarities[x]})
                    randomInt = random.randint(1,max) 
                    epicChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                    while epicChar['show'] in newblist:
                        randomInt = random.randint(1,max) 
                        epicChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                    shopDB.update_one({"id":member.id}, {"$addToSet":{"characterShop":{"name":epicChar["name"],"show":epicChar["show"],"rarity":epicChar["rarity"]}}})
                if x == 4:
                    max = charDB.count_documents({"rarity":rarities[x]})
                    randomInt = random.randint(1,max) 
                    legendaryChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                    while legendaryChar['show'] in newblist:
                        randomInt = random.randint(1,max) 
                        legendaryChar = charDB.find_one({"rarity":rarities[x], "raritynumber": randomInt})
                    shopDB.update_one({"id":member.id}, {"$addToSet":{"characterShop":{"name":legendaryChar["name"],"show":legendaryChar["show"],"rarity":legendaryChar["rarity"]}}})
                if x == 5:
                    max = charDB.count_documents({"rarity":rarities[4]})
                    randomInt = random.randint(1,max) 
                    legChar2 = charDB.find_one({"rarity":rarities[4], "raritynumber": randomInt})
                    while legChar2['show'] in newblist:
                        randomInt = random.randint(1,max) 
                        legChar2 = charDB.find_one({"rarity":rarities[4], "raritynumber": randomInt})
                    shopDB.update_one({"id":member.id}, {"$addToSet":{"characterShop":{"name":legChar2["name"],"show":legChar2["show"],"rarity":legChar2["rarity"]}}})
                if x == 6:
                    max = loadingScreenDB.count_documents({})
                    randomInt = random.randint(1,max) 
                    loadingScreen = loadingScreenDB.find_one({'number':randomInt})
                    shopDB.update_one({"id":member.id}, {"$addToSet":{"characterShop":{"number":loadingScreen["number"]}}})


        user = shopDB.find_one({"id":member.id})

        todaysDay = todayDisplay.day
        todaysMonth = todayDisplay.month 
        
        
        try:
            indvMonth = user["month"]
        except:
            shopDB.update_one({"id":member.id}, {"$set":{"month":todaysMonth}})
            #userDB.update_one({"id":member.id}, {"$set":{"nextmonth":todayDisplay.month+1}})
            user = shopDB.find_one({"id":member.id})
            indvMonth = user["month"]
        
    
        if todaysMonth != indvMonth:
            #userDB.update_one({"id":member.id}, {"$set":{"today":1}})
            tomorow = datetime.datetime.utcnow() + datetime.timedelta(days = 1)
            shopDB.update_one({"id":member.id}, {"$set":{"tomorrow":tomorow.day}})
            shopDB.update_one({"id":member.id}, {"$set":{"month":todaysMonth}})
            try:
                userShop = user["characterShop"]
                shopDB.update_one({"id":member.id}, {"$set":{"characterShop":[]}})
            except:
                pass
            resetShop()
            em = discord.Embed(title = f"ACcharactershop - {member.name}\nYour shop has been reset since you last checked, please do /acshop again to see what you got!",color = getColor('botColor'))
            em.set_thumbnail(url = member.avatar)
            await interaction.response.send_message(embed=em)
            return

        # if todaysMonth == 1:
        #     shopDB.update_one({"id":member.id}, {"$set":{"month":todaysMonth}})

        #print(todaysMonth)

        gethour = datetime.datetime.utcnow()
        currenthour = gethour.hour
        currentminute = gethour.minute
        # currentsecond = gethour.second

        user = shopDB.find_one({"id":member.id})
        charShoplist = []
        try:
            indvTomorrow = user["tomorrow"]
        except:
            #userDB.update_one({"id":member.id}, {"$set":{"today":todayDisplay.day}})
            tomorow = datetime.datetime.utcnow() + datetime.timedelta(days = 1)
            
            shopDB.update_one({"id":member.id}, {"$set":{"tomorrow":tomorow.day}})
            user = shopDB.find_one({"id":member.id})
            indvTomorrow = user["tomorrow"]
            try:
                userShop = user["characterShop"]
                shopDB.update_one({"id":member.id}, {"$set":{"characterShop":[]}})
            except:
                pass
            resetShop()
            em = discord.Embed(title = f"ACcharactershop - {member.name}\nYour shop has been reset since you last checked, please do /acshop again to see what you got!",color = getColor('botColor'))
            em.set_thumbnail(url = member.avatar)
            await interaction.response.send_message(embed=em)
            return

        if indvTomorrow >= todaysDay + 2:
            tomorow = datetime.datetime.utcnow() + datetime.timedelta(days = 1)
            shopDB.update_one({"id":member.id}, {"$set":{"tomorrow":tomorow.day}})
            user = shopDB.find_one({"id":member.id})
            indvTomorrow = user["tomorrow"]
            try:
                userShop = user["characterShop"]
                shopDB.update_one({"id":member.id}, {"$set":{"characterShop":[]}})
            except:
                pass
            resetShop()
            em = discord.Embed(title = f"ACcharactershop - {member.name}\nYour shop has been reset since you last checked, please do /acshop again to see what you got!",color = getColor('botColor'))
            em.set_thumbnail(url = member.avatar)
            await interaction.response.send_message(embed=em)
            return

        if ((indvTomorrow == 1 and todaysDay == 1) or (indvTomorrow == 1 and todaysDay == 31) or (indvTomorrow == 1 and todaysDay == 28) or (indvTomorrow == 1 and todaysDay == 29) or (indvTomorrow == 1 and todaysDay == 30)):
            user = shopDB.find_one({"id":member.id})
            userShop = user["characterShop"]
            for x in userShop:
                try:
                    charShoplist.append(x["name"])
                except:
                    charShoplist.append(x["number"])
        elif todaysDay >= indvTomorrow:
            d2 = datetime.datetime.utcnow() + datetime.timedelta(days = 1)
            shopDB.update_one({"id":member.id}, {"$set":{"tomorrow":d2.day}})
            try:
                shopDB.update_one({"id":member.id}, {"$set":{"characterShop":[]}})
                resetShop()
                user = shopDB.find_one({"id":member.id})
                userShop = user["characterShop"]
                for x in userShop:
                    try:
                        charShoplist.append(x["name"])
                    except:
                        charShoplist.append(x["number"])
            except:
                resetShop()
                userShop = user["characterShop"]
                for x in userShop:
                    try:
                        charShoplist.append(x["name"])
                    except:
                        charShoplist.append(x["number"])
            em = discord.Embed(title = f"ACcharactershop - {member.name}\nYour shop has been reset since you last checked, please do /acshop again to see what you got!",color = getColor('botColor'))
            em.set_thumbnail(url = member.avatar)
            await interaction.response.send_message(embed=em)
            return
        
        else:
            user = shopDB.find_one({"id":member.id})
            userShop = user["characterShop"]
            if len(userShop) != 6:
                shopDB.update_one({"id":member.id}, {"$set":{"characterShop":[]}})
                resetShop()
                user = shopDB.find_one({"id":member.id})
                userShop = user["characterShop"]
            for x in userShop:
                try:
                    charShoplist.append(x["name"])
                except:
                    charShoplist.append(x["number"])
        
    
        
        # uncommonChar = charDB.find_one({"name":charShoplist[0]})
        # rareChar = charDB.find_one({"name":charShoplist[1]})
        # epicChar = charDB.find_one({"name":charShoplist[2]})
        # legendaryChar1 = charDB.find_one({"name":charShoplist[3]})
        # legendaryChar2 = charDB.find_one({"name":charShoplist[4]})
        # loadingScreen = loadingScreenDB.find_one({"number":charShoplist[5]})

        # #commonprice = botStats["commonbaseprice"]
        # uncommonprice = botStats["uncommonbaseprice"]
        # rareprice = botStats["rarebaseprice"]
        # epicprice = botStats["epicbaseprice"]
        # legendaryprice = botStats["legendarybaseprice"]
        # loadingprice = botStats['lsbaseprice']


        usermoney = user["money"]

        homeem = discord.Embed(title = f"ACraffle Character Shop - {member.name}",description = f"\n**Time Until Next Reset: {23 - currenthour} hours {60-currentminute} minutes**\nTo reset your shop manually **/acresetshop**\n\n**User Balance: ${usermoney}**", color = discord.Color.teal())
        homeem.set_thumbnail(url = member.avatar)
        homeem.set_image(url="https://media1.tenor.com/images/52950888781d0f27f61df71442f176cd/tenor.gif?itemid=5078001")
        

        userProf = shopDB.find_one({"id":member.id})
        # try:
        #     boughtun = userProf["boughtuncommon"]
        # except:
        #     shopDB.update_one({"id":member.id}, {"$set":{"boughtuncommon":False}})
        #     userProf = shopDB.find_one({"id":member.id})
        #     boughtun = userProf["boughtuncommon"]
        # try:
        #     boughtrare = userProf["boughtrare"]
        # except:
        #     shopDB.update_one({"id":member.id}, {"$set":{"boughtrare":False}})
        #     userProf = shopDB.find_one({"id":member.id})
        #     boughtrare = userProf["boughtrare"]
        # try:
        #     boughtepic = userProf["boughtepic"]
        # except:
        #     shopDB.update_one({"id":member.id}, {"$set":{"boughtepic":False}})
        #     userProf = shopDB.find_one({"id":member.id})
        #     boughtepic = userProf["boughtepic"]
        # try:
        #     boughtleg1 = userProf["boughtlegendary1"]
        # except:
        #     shopDB.update_one({"id":member.id}, {"$set":{"boughtlegendary1":False}})
        #     userProf = shopDB.find_one({"id":member.id})
        #     boughtleg1 = userProf["boughtlegendary1"]
        # try:
        #     boughtleg2 = userProf["boughtlegendary2"]
        # except:
        #     shopDB.update_one({"id":member.id}, {"$set":{"boughtlegendary2":False}})
        #     userProf = shopDB.find_one({"id":member.id})
        #     boughtleg2 = userProf["boughtlegendary2"]
        # try:
        #     boughtloading = userProf["boughtloading"]
        # except:
        #     shopDB.update_one({"id":member.id}, {"$set":{"boughtloading":False}})
        #     userProf = shopDB.find_one({"id":member.id})
        #     boughtloading = userProf["boughtloading"]
            
        view=homeComp(interaction.user)
        await interaction.response.send_message(embed=homeem,view=view)
        view.message = await interaction.original_response()
        
    @app_commands.command(name='acresetshop', description='Reset your /acshop by choose one of the options')
    @app_commands.choices(reset=[
        discord.app_commands.Choice(name='Uncommon',value=1),
        discord.app_commands.Choice(name='Rare',value=2),
        discord.app_commands.Choice(name='Epic',value=3),
        discord.app_commands.Choice(name='Legendary 1',value=4),
        discord.app_commands.Choice(name='Legendary 2',value=5),
        discord.app_commands.Choice(name='Loading Screen',value=6),
        discord.app_commands.Choice(name='All',value = 7)
    ])
    async def acresetshop(self, interaction: discord.Interaction, reset: discord.app_commands.Choice[int]):
        member = interaction.user
        user = shopDB.find_one({'id':member.id})
        usermoney = user['money']
        hasEnough = False
        if reset.value == 1:
            if (usermoney >= round(uncommonprice/2)):
                em = discord.Embed(title = f"ACresetshop - {member.name}",description=f"Would you like to reset the **Uncommon Character** in your shop for **${round(uncommonprice/2)}**?",color = getColor('botColor'))
                em.set_thumbnail(url = member.avatar)
                hasEnough = True
            else:
                em = discord.Embed(title = f"ACresetshop - {member.name}",description=f"You do not have enough money!!\n**Cost: ${round(uncommonprice/2)}**",color = getColor('botColor'))
                em.set_thumbnail(url = member.avatar)
    
        if reset.value == 2:
            if (usermoney >= round(rareprice/2)):
                em = discord.Embed(title = f"ACresetshop - {member.name}",description=f"Would you like to reset the **Rare Character** in your shop for **${round(rareprice/2)}**?",color = getColor('botColor'))
                em.set_thumbnail(url = member.avatar)
                hasEnough = True
            else:
                em = discord.Embed(title = f"ACresetshop - {member.name}",description=f"You do not have enough money!!\n**Cost: ${round(rareprice/2)}**",color = getColor('botColor'))
                em.set_thumbnail(url = member.avatar)
        if reset.value == 3:
            if (usermoney >= round(epicprice/2)):
                em = discord.Embed(title = f"ACresetshop - {member.name}",description=f"Would you like to reset the **Epic Character** in your shop for **${round(epicprice/2)}**?",color = getColor('botColor'))
                em.set_thumbnail(url = member.avatar)
                hasEnough = True
            else:
                em = discord.Embed(title = f"ACresetshop - {member.name}",description=f"You do not have enough money!!\n**Cost: ${round(epicprice/2)}**",color = getColor('botColor'))
                em.set_thumbnail(url = member.avatar)
        if reset.value == 4:
            if (usermoney >= round(legendaryprice/2)):
                em = discord.Embed(title = f"ACresetshop - {member.name}",description=f"Would you like to reset the **Legendary (1) Character** in your shop for **${round(legendaryprice/2)}**?",color = getColor('botColor'))
                em.set_thumbnail(url = member.avatar)
                hasEnough = True
            else:
                em = discord.Embed(title = f"ACresetshop - {member.name}",description=f"You do not have enough money!!\n**Cost: ${round(legendaryprice/2)}**",color = getColor('botColor'))
                em.set_thumbnail(url = member.avatar)
                
        if reset.value == 5:
            if (usermoney >= round(legendaryprice/2)):
                em = discord.Embed(title = f"ACresetshop - {member.name}",description=f"Would you like to reset the **Legendary (2) Character** in your shop for **${round(legendaryprice/2)}**?",color = getColor('botColor'))
                em.set_thumbnail(url = member.avatar)
                hasEnough = True
            else:
                em = discord.Embed(title = f"ACresetshop - {member.name}",description=f"You do not have enough money!!\n**Cost: ${round(legendaryprice/2)}**",color = getColor('botColor'))
                em.set_thumbnail(url = member.avatar)
        if reset.value == 6:
            if (usermoney >= round(loadingprice/2)):
                em = discord.Embed(title = f"ACresetshop - {member.name}",description=f"Would you like to reset the **Loading Screen** in your shop for **${round(loadingprice/2)}**?",color = getColor('botColor'))
                em.set_thumbnail(url = member.avatar)
                hasEnough = True
            else:
                em = discord.Embed(title = f"ACresetshop - {member.name}",description=f"You do not have enough money!!\n**Cost: ${round(loadingprice/2)}**",color = getColor('botColor'))
                em.set_thumbnail(url = member.avatar)
        if reset.value == 7:
            if (usermoney >= 3000):
                em = discord.Embed(title = f"ACresetshop - {member.name}",description=f"Would you like to reset your **entire** shop for **$3000**?",color = getColor('botColor'))
                em.set_thumbnail(url = member.avatar)
                hasEnough = True
            else:
                em = discord.Embed(title = f"ACresetshop - {member.name}",description=f"You do not have enough money!!\n**Cost: $3000**",color = getColor('botColor'))
                em.set_thumbnail(url = member.avatar)
        
        
        if hasEnough:
            view=ResetShop(interaction.user,reset.value)
            await interaction.response.send_message(embed=em,view=view)
            view.message = await interaction.original_response()
        else:
            await interaction.response.send_message(embed=em)
            
    
        
        
async def setup(bot):
    await bot.add_cog(ACSHOP(bot))