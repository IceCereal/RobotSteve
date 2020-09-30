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
		
		user = ctx.message.author

		rand_nos = []

		for i in range(4):
			
			random_number = randint(0, 100)
			
			if i == 0:

				if random_number < 30:
					rand_nos.append('Not')
				
				elif random_number > 30 and random_number < 70:
					rand_nos.append('Mildly')

				else:
					rand_nos.append('Very')

			elif i == 1:

				if random_number < 30:
					rand_nos.append('Not feeling')
				
				elif random_number > 30 and random_number < 70:
					rand_nos.append('Mildly')

				else:
					rand_nos.append('Really')

			elif i == 2:
				rand_nos.append(random_number / 5)

			elif i == 3:
				rand_nos.append(round(random_number / 10))

		rgb_values = [255, 173, 51]

		title = "{}: Stats".format(user)

		embed = discord.Embed(title=title, colour=discord.Colour.from_rgb(*rgb_values))

		embed.add_field(name="Fatness", value='{} fat'.format(rand_nos[0]), inline=True)
		embed.add_field(name="Lonliness", value='{} lonely'.format(rand_nos[1]), inline=True)
		embed.add_field(name="Consumption of Food", value='{}kg'.format(rand_nos[2]), inline=True)
		embed.add_field(name="Crappiness at Minecraft", value='{}/10 bad at the game'.format(rand_nos[3]), inline=True)

		await ctx.channel.send(embed = embed)


def setup(bot):
	bot.add_cog(Fats(bot))