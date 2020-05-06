"""
	Name: RobotSteve
	Objective: A discord bot for MECCraft, MEC's Minecraft Server
	Date: 2020-Apr-25

	Author: IceCereal
"""

import discord
from discord.ext import commands

from pathlib import Path

BOT_PREFIX = ('++')
bot = commands.Bot(command_prefix=BOT_PREFIX)


@bot.command(
	name="source",
	aliases=["src"],
	brief="source code link",
	description="The Source Code that can be found at Github"
)
async def source(ctx):
	await ctx.channel.send("https://github.com/IceCereal/RobotSteve")


@bot.event
async def on_ready():
	print ("\nLogged in as:\t" + str(bot.user))
	print ("-----------------")

	await bot.change_presence(activity=discord.Game(name="MECCraft"))


if __name__ == '__main__':
	res = Path("res")

	with open(res / "TOKEN", 'r') as TokenObj:
		TOKEN = TokenObj.read()

	cogs = ['utils.random.nuts',
		'utils.stats.mcstats',
		'utils.controls.backup',
		'utils.controls.control',
		'utils.error_handler.handler']

	for cog in cogs:
		print ("Loading Cog:\t", cog, "...")

		bot.load_extension(cog)


	bot.run(TOKEN)