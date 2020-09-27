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

		rand_nos = []

		for i in range(4):
			rand_nos.append(randint(0, 100))

		message += "username is {}% fat.\n".format(rand_nos[0])
		message += "username is really feeling {}% lonely right now.\n".format(rand_nos[1])
		message += "username eats {}kg of food every day.\n".format(rand_nos[2] / 5)
		message += "username is indeed, {}% crap at Minecraft.".format(rand_nos[3])

		message.replace('username', user.mention)

		await ctx.channel.send(message)


def setup(bot):
	bot.add_cog(Fats(bot))