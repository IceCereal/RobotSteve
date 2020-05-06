import discord
from discord.ext import commands

import io
import sys
import aiohttp
import argparse
from pathlib import Path
from urllib import request

class ArgumentParser(argparse.ArgumentParser):
	def error(self, message):
		return (sys.stderr)


class Nuts(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.url = "https://source.unsplash.com/random"


	@commands.cooldown(1, 1, commands.cooldowns.BucketType.channel)
	@commands.command(
		name = "coco",
		brief = "get a random image. Optional-Arguments: Search Parameters",
		usage = "[--search, -s]",
		description = "get a random image from unsplash. [1 invoke per 10 seconds per channel]",
		enabled = True
	)
	async def coco(self, ctx):
		parser = ArgumentParser()
		parser.add_argument("--search", '-s', required=False)

		try:
			args = parser.parse_args(ctx.message.content.split()[1:])
		except:
			# I can't catch this exception for whatever reason...? Anyway, it continues as per normal
			# Even if there are arguments that don't match, for example: `--raww` is ignored
			pass

		url = self.url
		if args.search:
			url += "/?" + args.search

		random_msg = "Random Image"
		if args.search:
			random_msg += " of: " + args.search

		async with aiohttp.ClientSession() as session:
			async with session.get(url) as resp:
				if resp.status != 200:
					return await ctx.channel.send('Could not download file...')
				data = io.BytesIO(await resp.read())
				await ctx.channel.send(random_msg)
				await ctx.channel.send(file=discord.File(data, 'coco.jpeg'))

		return


def setup(bot):
	bot.add_cog(Nuts(bot))