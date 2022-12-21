import discord 
import config
from discord import app_commands
from discord.ext import commands
import random
import pymongo

cluster = pymongo.MongoClient(config.MONGOTOKEN)

charDB = cluster["acraffleCartoon"]["characters"]
userDB = cluster["acraffleCartoon"]["users"]
shopDB = cluster["acraffleCartoon"]["usershops"]
showDB = cluster["acraffleCartoon"]["shows"]
botstatsDB = cluster["acrafflebot"]["botstats"]
presDB = cluster["acraffleCartoon"]["userprestige"]


def getPresCol(level):
    if level == 0:
        color = discord.Color.teal()
    else:
        color = discord.Color(random.randint(0,16777215))
    return color
        
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


class CCBS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("CCBS Cog loaded!")
        
    #Test Command
    @app_commands.command(name="ccbs",description="ACbankshow shows your unlocked characters for the specified show")
    @app_commands.describe(show="Use the show name or abbriviation found in /ccshows",
                           user="Specify a user or @ yourself for your own bank")
    async def ccbs(self,interaction: discord.Interaction, show: str, user:discord.User):
        await interaction.response.defer()
        member = user
        guild = interaction.guild
        await createuser(member,guild)
        membername = member.name
        showInput = show
        user = userDB.find_one({"id":member.id})
        
        try:
            userChars = user["characters"]
        except:
            em = discord.Embed(title = f"{member.name.capitalize()} hasn't unlocked any characters!\nDo */ccraffle*  to get started!",color = discord.Color.teal())
            await interaction.edit_original_response(embed=em)
            
        
        try:
            showFound = showDB.find_one({'name':showInput})
        except:
            showFound = None

        if showFound == None:
            try:
                showFound = showDB.find_one({'abv':showInput})
            except:
                pass

        if showFound == None:
            em = discord.Embed(title = f"ACbankshow- Show not found.",description = f"Remember to use the *abbreviation* of the show found in **/ccshows**\nExample: **/ccbs atla**",color = discord.Color.teal())
            await interaction.edit_original_response(embed=em)
            

        showPrint = showFound["title"]
        showAbv = showFound["abv"]
        showInput = showFound['name']
        
        amtCharsInShow = charDB.count_documents({"show":showInput})
        amountUnlocked = 0

        for y in userChars:
            if showInput == y["show"]:
                amountUnlocked+=1
        
        userpres = presDB.find_one({'id':member.id})
        if userpres == None:
            level = 0
        else:
            level = 0
            preslist = userpres['shows']
            for shws in preslist:
                if shws['show'] == showInput:
                    level = shws['tier']

        stars = ''
        for x in range(level):
            stars += '⭐'
    
        singlePage = discord.Embed (
            title = f'ACbankshow - {membername.capitalize()}',
            description = f"**{showPrint} ({showAbv})\nUnlocked: {amountUnlocked}/{amtCharsInShow}\nPrestige: {level}**\n{stars}",
            colour = getPresCol(level)
        )
        singlePage.set_footer(text=f"{showPrint} ({showAbv}) - Unlocked: {amountUnlocked}/{amtCharsInShow}")

    
        def addfield(page,tempname,rarity,have):
            page.add_field(name=f"{have} {tempname.capitalize()}",value=f"{rarity.capitalize()}", inline=True)


        # hashyper = userDB.find_one({"id":member.id, "characters":{"$elemMatch": {"show":showInput,"rarity":'hyperlegendary'}}})
        # if hashyper == None:
        charlist = charDB.find({"show":showInput}).sort("rarityrank")
        for y in charlist:
            charshow=y["show"]
            if charshow == showInput: 
                charFound=False
                for t in userChars:
                    if y['name'] == t["name"]:
                        addfield(singlePage,y["name"],y["rarity"],"✅")
                        charFound = True
                if charFound == False:
                    addfield(singlePage,y["name"],y["rarity"],"❌")
        # else:
        #     charlist = charDB.find({"show":showInput}).sort("rarityrank")
        #     for y in charlist:
        #         addfield(singlePage,y['name'],y['rarity'],"✅")


        singlePage.set_thumbnail(url = showFound['thumbnail'])
    
        # await ctx.send(embed = singlePage)
        await interaction.edit_original_response(embed=singlePage)
        # commanduser = ctx.author
        # await send_logs_acbs(commanduser,member, guild, "acbankspecific",showInput)
        # return
        
        
        
        
        

        
async def setup(bot):
    await bot.add_cog(CCBS(bot))