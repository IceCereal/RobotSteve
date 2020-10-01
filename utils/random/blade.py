import discord
from discord.ext import commands

from random import seed
from random import randint

import datetime

class Blade(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(
        name = "blade",
        brief = "get enlightened by the almighty lord Technoblade",
        description = "chooses a random Sun Tzu art of war quote from a predefined text file",
        enabled = True
    )
    async def blade(self,ctx):

        user = ctx.message.author

        #quotes file
        quotes = open("txt/quote.txt","r")
        quotes = quotes.read().split('\n')
        length = len(quotes)

        #randomizer
        time = datetime.datetime.now()
        mic = time.microsecond
        seed(mic)

        i = randint(0,length-1)

        try:
            if i!=27:
                await ctx.channel.send("```"+quotes[i]+"\n~Technoblade"+"```")
            else:
                #second randomizer for number of years of 'training'
                time = datetime.datetime.now()
                mic = time.microsecond
                seed(mic)

                j = randint(1,10)
                await ctx.channel.send(f"```\"If you wish to defeat me, traing for another {(j*100)} years\n~Technoblade```")
        
        except Exception as e:
            await ctx.channel.send(f"Something went wrong:{e}")

        
def setup(bot):
    bot.add_cog(Blade(bot))