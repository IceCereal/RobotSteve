from json import load
from pathlib import Path
from datetime import datetime
from argparse import ArgumentParser
from mcipc.query import Client

import discord
from discord.ext import commands

from utils.stats.log_manager import get_individual_stats, get_all_stats

res = Path("res")

class MinecraftStats(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.cooldown(1, 5, commands.cooldowns.BucketType.channel)
	@commands.command(
		name = "online",
		brief = "get server statistics",
		usage = "[--raw, -r]",
		enabled = True,
		description = "Get Realtime MECCraft Server Statistics"
	)
	async def online(self, ctx):
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
				try:
					embed.add_field(name="Players", value=", ".join(full_stats.players), inline=False)
				except:
					embed.add_field(name="Players", value="No one's online", inline=False)
				embed.add_field(name="Version", value=full_stats.version, inline=True)
			else:
				for key, value in zip(full_stats._fields, full_stats):
					embed.add_field(name=str(key), value=str(value), inline=True)

		embed.set_thumbnail(url="https://raw.githubusercontent.com/IceCereal/RobotSteve/master/res/robotsteve.png")

		await ctx.channel.send(embed=embed)

		return 1


	@commands.cooldown(1, 5, commands.cooldowns.BucketType.channel)
	@commands.command(
		name = "stat",
		aliases = ["stats"],
		brief = "get player statistics",
		enabled = True,
		description = "Get all game player statistics"
	)
	async def stat(self, ctx, *args):
		if len(args) != 1:
			await ctx.channel.send('Invalid format!')

		username = args[0]
		
		if username == 'all':
			all_stats = get_all_stats()

			# TODO: change the below to a single loop

			rgb_values = [255, 173, 51]

			title = "All players' game Stats"

			embed_gametime = discord.Embed(title=title, colour=discord.Colour.from_rgb(*rgb_values))

			embed_gametime.add_field(name="Rank", value=all_stats['gametime']['ranks'], inline=True)
			embed_gametime.add_field(name="Username", value=all_stats['gametime']['usernames'], inline=True)
			embed_gametime.add_field(name="Total time played", value=all_stats['gametime']['total_time_played'], inline=True)

			await ctx.channel.send(embed = embed_gametime)


			embed_session_stat = discord.Embed(title=title, colour=discord.Colour.from_rgb(*rgb_values))

			embed_session_stat.add_field(name="Rank", value=all_stats['session_ranks']['ranks'], inline=True)
			embed_session_stat.add_field(name="Username", value=all_stats['session_ranks']['usernames'], inline=True)
			embed_session_stat.add_field(name="Longest session played", value=all_stats['session_ranks']['longest_session'], inline=True)
			
			await ctx.channel.send(embed = embed_session_stat)


			embed_log_in_off = discord.Embed(title=title, colour=discord.Colour.from_rgb(*rgb_values))

			embed_log_in_off.add_field(name="Rank", value=all_stats['logged_in_off']['ranks'], inline=True)
			embed_log_in_off.add_field(name="Username", value=all_stats['logged_in_off']['usernames'], inline=True)
			embed_log_in_off.add_field(name="Number of log in/out", value=all_stats['logged_in_off']['login_count'], inline=True)
			
			await ctx.channel.send(embed = embed_log_in_off)


			embed_msgs_stat = discord.Embed(title=title, colour=discord.Colour.from_rgb(*rgb_values))

			embed_msgs_stat.add_field(name="Rank", value=all_stats['msg_ranks']['ranks'], inline=True)
			embed_msgs_stat.add_field(name="Username", value=all_stats['msg_ranks']['usernames'], inline=True)
			embed_msgs_stat.add_field(name="Number of messages sent", value=all_stats['msg_ranks']['msgs_sent'], inline=True)
			
			await ctx.channel.send(embed = embed_msgs_stat)


		else:
			user_stats = get_individual_stats(username)
			
			if 'message' not in user_stats:

				rgb_values = [255, 173, 51]

				title = "{} game Stats".format(username)

				embed_gametime = discord.Embed(title=title, colour=discord.Colour.from_rgb(*rgb_values))

				embed_gametime.add_field(name="Total gametime", value=user_stats['total_time_played'], inline=True)
				embed_gametime.add_field(name="Longest session", value=user_stats['longest_session'], inline=True)
				embed_gametime.add_field(name="Percentage of time played", value='{:.3f}%'.format(user_stats['percent']), inline=True)
				embed_gametime.add_field(name="Number of messages", value=user_stats['msgs_sent'], inline=True)
				embed_gametime.add_field(name="Number of times logged in/out", value=user_stats['login_count'], inline=True)

				await ctx.channel.send(embed = embed_gametime)

			else:
				await ctx.channel.send(user_stats['message'])


def setup(bot):
	bot.add_cog(MinecraftStats(bot))
