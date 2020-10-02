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
    async def blade(self,ctx,arg):

        user = ctx.message.author

        #quotes file
        quotes = open("txt/quote.txt","r")
        quotes = quotes.read().split('\n')
        length = len(quotes)

        try:
            i = int(arg)

            if i!=length-1:
                await ctx.channel.send("```"+quotes[i]+"\n~Technoblade"+"```")
            else if i == length:
                #second randomizer for number of years of 'training'
                time = datetime.datetime.now()
                mic = time.microsecond
                seed(mic)

                j = randint(1,10)
                await ctx.channel.send(f"```\"If you wish to defeat me, train for another {(j*100)} years\n~Technoblade```")
        
        except Exception as e:
            await ctx.channel.send(f"Something went wrong:{e}")

        
def setup(bot):
    bot.add_cog(Blade(bot))