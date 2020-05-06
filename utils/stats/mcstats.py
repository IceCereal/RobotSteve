from json import load
from pathlib import Path
from datetime import datetime
from argparse import ArgumentParser
from mcipc.query import Client

import discord
from discord.ext import commands

res = Path("res")

class MinecraftStats(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.cooldown(1, 5, commands.cooldowns.BucketType.channel)
	@commands.command(
		name = "stat",
		aliases = ["stats"],
		brief = "get server statistics",
		usage = "[--raw, -r]",
		enabled = True,
		description = "Get Realtime MECCraft Server Statistics"
	)
	async def stat(self, ctx):
		await ctx.trigger_typing()

		parser = ArgumentParser()
		parser.add_argument("--raw", '-r', action='store_true')

		try:
			args = parser.parse_args(ctx.message.content.split()[1:])
			raw = args.raw
		except:
			raw = False

		with open(res / "config.json", 'r') as F:
			config = load(F)

		online = True
		try:
			with Client(config["ip"], int(config["query-port"])) as client:
				full_stats = client.full_stats

		except ConnectionRefusedError:
			online = False

		title = "MECCraft - Status: "
		if online:
			title += "Online"
		else:
			title += "Offline"

		if online:
			values = [127, 255, 0]
		else:
			values = [208, 2, 7]

		embed = discord.Embed(title=title, colour=discord.Colour.from_rgb(*values))

		embed.set_footer(text="Time: " + str(datetime.now()))

		if online:
			if not raw:
				embed.add_field(name="IP", value=config['ip'], inline=True)
				embed.add_field(name="Port", value=config['port'], inline=True)
				embed.add_field(name="MOTD", value=full_stats.host_name, inline=True)
				embed.add_field(name="Players Online", value=str(full_stats.num_players) + " / " + str(full_stats.max_players), inline=True)
				embed.add_field(name="Players", value=", ".join(full_stats.players), inline=False)
				embed.add_field(name="Version", value=full_stats.version, inline=True)
			else:
				for key, value in zip(full_stats._fields, full_stats):
					embed.add_field(name=str(key), value=str(value), inline=True)

		embed.set_thumbnail(url="https://raw.githubusercontent.com/IceCereal/RobotSteve/master/res/robotsteve.png")

		await ctx.channel.send(embed=embed)

		return 1


def setup(bot):
	bot.add_cog(MinecraftStats(bot))