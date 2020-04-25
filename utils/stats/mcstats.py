import grequests
from json import load
from pathlib import Path
from datetime import datetime
from argparse import ArgumentParser

import discord
from discord.ext import commands

res = Path("res")

class MinecraftStats(commands.Cog):
	def __init__(self, bot):
		self.url = "https://api.mcsrvstat.us/2/"
		self.bot = bot

	@commands.cooldown(1, 60, commands.cooldowns.BucketType.channel)
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

		rs = [grequests.get(self.url + config["ip"] + ":" + config["port"])]
		r = grequests.map(rs)[0]

		stats = r.json()
		online = stats['online']

		title = "MECCraft - Status: "
		if online:
			title += "Online"
		else:
			title += "Offline"

		if stats['online']:
			values = [127, 255, 0]
		else:
			values = [208, 2, 7]

		embed = discord.Embed(title=title, colour=discord.Colour.from_rgb(*values))

		embed.set_footer(text="Time: " + str(datetime.now()))

		if online:
			if not raw:
				embed.add_field(name="IP", value=stats['ip'], inline=False)
				embed.add_field(name="Port", value=stats['port'], inline=False)
				embed.add_field(name="MOTD", value=stats['motd']['clean'][0], inline=False)
				embed.add_field(name="Players Online", value=str(stats['players']['online']) + " / " + str(stats['players']['max']), inline=False)
				embed.add_field(name="Players", value=", ".join(stats['players']['list']), inline=False)
				embed.add_field(name="Version", value=stats['version'], inline=False)
				embed.add_field(name="Software", value=stats['software'], inline=False)
			else:
				for field in stats:
					if type(stats[field]) == dict:
						embed.add_field(name="**"+field+"**", value="-----------", inline=False)
						for innerField in stats[field]:
							embed.add_field(name=innerField, value=str(stats[field][innerField]))
					else:
						embed.add_field(name=field, value=str(stats[field]), inline=False)

		embed.set_thumbnail(url="https://raw.githubusercontent.com/IceCereal/RobotSteve/master/res/robotsteve.png")

		await ctx.channel.send(embed=embed)

		return 1


def setup(bot):
	bot.add_cog(MinecraftStats(bot))