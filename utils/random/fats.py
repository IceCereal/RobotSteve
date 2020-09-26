import discord
from discord.ext import commands
from random import randint

class Fats(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(
	name = "fats",
	brief = "generate a random profile on yourself",
	description = " get a random profile about yourself. Don't take this seriously.",
	enabled = True
	)
	async def fats(self, ctx):
		
		message = ''
		user = ctx.message.author

		fatness = randint(0, 100)
		loneliness = randint(0, 100)
		food_amount = (randint(0, 100)) / 5
		crappiness = randint(0, 100)

		message += "username is {}% fat.\n".format(fatness)
		message += "username is really feeling {}% lonely right now.\n".format(loneliness)
		message += "username eats {}kg of food every day.\n".format(food_amount)
		message += "username is indeed, {}% crap at Minecraft.".format(crappiness)

		message.replace('username', user.mention)

		await ctx.channel.send(message)


def setup(bot):
	bot.add_cog(Fats(bot))