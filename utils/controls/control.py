import discord
from discord.ext import commands

import os
import sys
from json import load
from pathlib import Path
from datetime import datetime
import argparse

class ArgumentParser(argparse.ArgumentParser):
	def error(self, message):
		return (sys.stderr)
		

class Control(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	###############################################
	############### UTILITY METHODS ###############
	###############################################
	def make_embeds(self, title : str, color : list, key_list : list):
		embeds = []

		temp_embed = discord.Embed(title=title, colour=discord.Colour.from_rgb(*color))

		fields_counter = 0

		for (key, value) in key_list:
			if fields_counter >= 25:
				embeds.append(temp_embed)
				temp_embed = discord.Embed(title=title, colour=discord.Colour.from_rgb(*color))
				fields_counter = 0

			temp_embed.add_field(name=str(key), value=str(value), inline=True)
			fields_counter += 1

		embeds.append(temp_embed)

		return embeds

	def make_raw(self, title : str, key_list : list):
		messages = []

		temp_message = "```" + title + "\n\n"

		character_count = len(temp_message)
		for (key, value) in key_list:
			if (character_count + len(str(key)) + len(str(value)) + 4) > 1950:
				temp_message += "```"
				messages.append(temp_message)
				temp_message = "```" + title + "\n"

			temp_message += str(key) + ":\t" + str(value)
			if "\n" not in value:
				temp_message += "\n"
			character_count += len(str(key)) + len(str(value)) + 4

		temp_message += "```"
		messages.append(temp_message)

		return messages

	###############################################
	################### COMMANDS ##################
	###############################################
	@commands.has_permissions(administrator=True)
	@commands.command(
		name = "full-stats",
		brief = "get full stats from the minecraft/ folder",
		usage = ["[OPTIONS] -f=filename"],
		enabled = True
	)
	async def full_stats(self, ctx):
		"""
			Get the statistics of a file name from the minecraft/ folder in the Digital Ocean Droplet.

			Available files are: banned-ips, banned-players, bukkit, commands, eula, ops, password-protect, core-protect, server-properties (this is very dangerous), whitelist
			
			To use this command, type ++full-stats [OPTIONS] -f=filename
			
			OPTIONS:
			    --raw, -r : raw output and not prettified
			    --force : only to be used with server-properties. This will show most of the server-properties that are safe to share.
			    --force-force : only to be used with server-properties. This will show all the server-properties. [DANGEROUS].

			    --filename, -f : filename from available files
		"""

		"""
			export MINECRAFT_PATH=path/to/minecraft/
			minecraft_path = os.environ["MINECRAFT_PATH"]
		"""

		minecraft_path = Path(os.environ["MINECRAFT_PATH"])

		await ctx.trigger_typing()

		# This is a bad fix to a -f=[NAME] arg not being there in the message, but eh. It works
		if " -f=" not in ctx.message.content and " --filename=" not in ctx.message.content:
			await ctx.channel.send("Missing argument: --filename, -f. Type ++help full-stats")
			return

		parser = ArgumentParser()
		parser.add_argument("--raw", '-r', action='store_true')
		parser.add_argument("--force", action='store_true')
		parser.add_argument("--force-force", action='store_true')
		parser.add_argument("--filename", '-f', required=True)

		try:
			args = parser.parse_args(ctx.message.content.split()[1:])
		except:
			# I can't catch this exception for whatever reason...? Anyway, it continues as per normal
			# Even if there are arguments that don't match, for example: `--raww` is ignored
			pass

		files = {
			'banned-ips': 'banned-ips.json',
			'banned-players': 'banned-players.json',
			'bukkit': 'bukkit.yml',
			'commands': 'commands.yml',
			'eula': 'eula.txt',
			'ops': 'ops.json',
			'password-protect': 'plugins/PasswordProtect/config.yml',
			'core-protect': 'plugins/CoreProtect/config.yml',
			'server-properties': 'server.properties',
			'whitelist': 'whitelist.json'
		}

		if args.filename not in files.keys():
			await ctx.channel.send(args.filename + " is not in the available filenames. Type ++help full-stats to find out the available file name.")
			return

		reply_embeds = []
		reply_texts = []
		values = [180, 213, 0] # Yellow

		if args.filename == "server-properties":
			if not args.force:
				await ctx.channel.send("++full-stats server-properties requires the --force flag to run. Do this only if you know what you're doing.\
					This is dangerous and could lead to important information being seen by others if done in the wrong channel.")
				return
			
			sensitive_fields = ["rcon.port", "enable-rcon", "rcon.password"]
			server_properties = []

			with open(minecraft_path / files["server-properties"], 'r') as F:

				for line in F:
					if not line.startswith("#"):
						# This skips the comments in server-properties
						key = line[:line.index("=")]
						value = line[line.index("=")+1:]

						if len(value.split()) == 0:
							value = "-"

						if key in sensitive_fields and not args.force_force:
							continue

						server_properties.append((key, value))

				if args.raw:
					reply_texts = self.make_raw("Full-Stats: Server Properties", server_properties)
				else:
					reply_embeds = self.make_embeds("Full-Stats: Server Properties", values, server_properties)

		elif args.filename == "whitelist":
			whitelist_properties = []

			with open(minecraft_path / files["whitelist"], 'r') as F:
				whitelist = load(F)

				for user in whitelist:
					key = user["name"]
					value = user["uuid"]

					whitelist_properties.append((key, value))

				if args.raw:
					reply_texts = self.make_raw("Full-Stats: Whitelist", whitelist_properties)
				else:
					reply_embeds = self.make_embeds("Full-Stats: Whitelist", values, whitelist_properties)
				

		if len(reply_embeds) > 0:
			for i, embed in enumerate(reply_embeds):
				embed.set_footer(text="[" + str(i+1) + "/" + str(len(reply_embeds))+ "] Time: " + str(datetime.now()))
				embed.set_thumbnail(url="https://raw.githubusercontent.com/IceCereal/RobotSteve/master/res/robotsteve.png")

			for embed in reply_embeds:
				await ctx.channel.send(embed=embed)

		elif len(reply_texts) > 0:
			for i, text in enumerate(reply_texts):
				text+="\n" + str(i+1) + "/" + str(len(reply_texts))+ "]"

			for text in reply_texts:
				await ctx.channel.send(text)
		
		return


def setup(bot):
	bot.add_cog(Control(bot))