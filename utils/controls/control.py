import discord
from discord.ext import commands

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from json import load as json_load
from yaml import safe_load as yaml_safe_load 

class ArgumentParser(argparse.ArgumentParser):
	def error(self, message):
		return (sys.stderr)
		

class Control(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.MINECRAFT_PATH = Path(os.environ["MINECRAFT_PATH"])
		self.values = [180, 213, 0] # Yellow


	###############################################
	############### UTILITY METHODS ###############
	###############################################
	def message_list_builder(self, raw_data, properties):
		for key in raw_data:
			if type(raw_data[key]) == dict:
				value = "-------------"
				properties.append((key, value, False))
				self.message_list_builder(raw_data[key], properties)
			else:
				value = str(raw_data[key])
				properties.append((key, value, True))


	def make_embeds(self, title : str, color : list, key_list : list):
		embeds = []

		temp_embed = discord.Embed(title=title, colour=discord.Colour.from_rgb(*color))

		fields_counter = 0

		for (key, value, inline) in key_list:
			if fields_counter >= 25:
				embeds.append(temp_embed)
				temp_embed = discord.Embed(title=title, colour=discord.Colour.from_rgb(*color))
				fields_counter = 0

			temp_embed.add_field(name=str(key), value=str(value), inline=inline)
			fields_counter += 1

		embeds.append(temp_embed)

		return embeds


	def make_raw(self, title : str, key_list : list):
		messages = []

		temp_message = "```" + title + "\n\n"

		character_count = len(temp_message)
		for (key, value, inline) in key_list:
			if (character_count + len(str(key)) + len(str(value)) + 4) > 1950:
				temp_message += "```"
				messages.append(temp_message)
				temp_message = "```" + title + "\n"

			if not inline:
				temp_message += "\n"

			temp_message += str(key) + ":\t" + str(value)
			if "\n" not in value:
				temp_message += "\n"
			character_count += len(str(key)) + len(str(value)) + 4

		temp_message += "```"
		messages.append(temp_message)

		return messages


	###############################################
	################## BUILDERS ###################
	###############################################
	def invoke_banned_ips(self, file_path, raw : bool = None):
		with open(self.MINECRAFT_PATH / file_path, 'r') as F:
			banned_ips = json_load(F)

		banned_ips_properties = []
		for record in banned_ips:		
			self.message_list_builder(record, banned_ips_properties)

		if raw:
			reply = self.make_raw("Full-Stats: Banned-IPs", banned_ips_properties)
		else:
			reply = self.make_embeds("Full-Stats: Banned-IPs", self.values, banned_ips_properties)

		return reply


	def invoke_banned_players(self, file_path, raw : bool = None):
		with open(self.MINECRAFT_PATH / file_path, 'r') as F:
			banned_players = json_load(F)

		banned_players_properties = []
		for record in banned_players:
			self.message_list_builder(record, banned_players_properties)

		if raw:
			reply = self.make_raw("Full-Stats: Banned-Players", banned_players_properties)
		else:
			reply = self.make_embeds("Full-Stats: Banned-Players", self.values, banned_players_properties)

		return reply


	def invoke_bukkit(self, file_path, raw : bool = None):
		with open(self.MINECRAFT_PATH / file_path, 'r') as F:
			bukkit = yaml_safe_load(F)

		bukkit_properties = []
		self.message_list_builder(bukkit, bukkit_properties)

		if raw:
			reply = self.make_raw("Full-Stats: Bukkit", bukkit_properties)
		else:
			reply = self.make_embeds("Full-Stats: Bukkit", self.values, bukkit_properties)

		return reply


	def invoke_commands(self, file_path, raw : bool = None):
		with open(self.MINECRAFT_PATH / file_path, 'r') as F:
			commands = yaml_safe_load (F)
		
		commands_properties = []
		self.message_list_builder(commands, commands_properties)

		if raw:
			reply = self.make_raw("Full-Stats: Commands", commands_properties)
		else:
			reply = self.make_embeds("Full-Stats: Commands", self.values, commands_properties)

		return reply


	def invoke_eula(self, file_path, raw : bool = None):
		eula_properties = []
		with open(self.MINECRAFT_PATH / file_path, 'r') as F:
			for line in F:
				if len(line.split()) == 0:
					# Blank line
					continue

				key = line[:line.index("=")]
				value = line[line.index("=")+1:]

				eula_properties.append((key, value, False))

		if raw:
			reply = self.make_raw("Full-Stats: Eula", eula_properties)
		else:
			reply = self.make_embeds("Full-Stats: Eula", self.values, eula_properties)

		return reply


	def invoke_ops(self, file_path, raw : bool = None):
		with open(self.MINECRAFT_PATH / file_path, 'r') as F:
			ops = json_load(F)

		ops_properties = []
		for record in ops:
			ops_properties.append((record["name"], "-------------", False))
			record.pop("name", None)
			self.message_list_builder(record, ops_properties)

		if raw:
			reply = self.make_raw("Full-Stats: Ops", ops_properties)
		else:
			reply = self.make_embeds("Full-Stats: Ops", self.values, ops_properties)

		return reply


	def invoke_server_properties(self, file_path, force_force : bool = None, raw : bool = None):
		sensitive_fields = ["rcon.port", "enable-rcon", "rcon.password"]
		server_properties = []

		with open(self.MINECRAFT_PATH / file_path, 'r') as F:
			for line in F:
				if not line.startswith("#"):
					# This skips the comments in server-properties
					key = line[:line.index("=")]
					value = line[line.index("=")+1:]

					if len(value.split()) == 0:
						value = "-"

					if key in sensitive_fields and not force_force:
						continue

					server_properties.append((key, value, True))

		if raw:
			reply = self.make_raw("Full-Stats: Server Properties", server_properties)
		else:
			reply = self.make_embeds("Full-Stats: Server Properties", self.values, server_properties)

		return reply


	def invoke_whitelist(self, file_path, raw : bool = None):
		with open(self.MINECRAFT_PATH / file_path, 'r') as F:
			whitelist = json_load(F)

		whitelist_properties = []
		for record in whitelist:
			whitelist_properties.append((record["name"], record["uuid"], True))

		if raw:
			reply = self.make_raw("Full-Stats: Whitelist", whitelist_properties)
		else:
			reply = self.make_embeds("Full-Stats: Whitelist", self.values, whitelist_properties)

		return reply


	###############################################
	################## COMMANDS ###################
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

			Available files are: banned-ips, banned-players, bukkit, commands, eula, ops, server-properties (this is very dangerous), whitelist
			
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
			'server-properties': 'server.properties',
			'whitelist': 'whitelist.json'
		}

		if args.filename not in files.keys():
			await ctx.channel.send(args.filename + " is not in the available filenames. Type ++help full-stats to find out the available file name.")
			return

		if args.filename == "banned-ips":
			reply = self.invoke_banned_ips(Path(files["banned-ips"]), args.raw)

		elif args.filename == "banned-players":
			reply = self.invoke_banned_players(Path(files["banned-players"]), args.raw)

		elif args.filename == "bukkit":
			reply = self.invoke_bukkit(Path(files["bukkit"]), args.raw)

		elif args.filename == "commands":
			reply = self.invoke_commands(Path(files["commands"]), args.raw)

		elif args.filename == "eula":
			reply = self.invoke_eula(Path(files["eula"]), args.raw)

		elif args.filename == "ops":
			reply = self.invoke_ops(Path(files["ops"]), args.raw)

		elif args.filename == "server-properties":
			if not args.force:
				await ctx.channel.send("++full-stats server-properties requires the --force flag to run. Do this only if you know what you're doing.\
					This is dangerous and could lead to important information being seen by others if done in the wrong channel.")
				return

			reply = self.invoke_server_properties(Path(files["server-properties"]), args.force_force, args.raw)
			
		elif args.filename == "whitelist":
			reply = self.invoke_whitelist(Path(files["whitelist"]), args.raw)


		if not args.raw:
			for i, embed in enumerate(reply):
				embed.set_footer(text="[" + str(i+1) + "/" + str(len(reply))+ "] Time: " + str(datetime.now()))
				embed.set_thumbnail(url="https://raw.githubusercontent.com/IceCereal/RobotSteve/master/res/robotsteve.png")

			for embed in reply:
				await ctx.channel.send(embed=embed)

		else:
			for i, text in enumerate(reply):
				text+="\n" + str(i+1) + "/" + str(len(reply))+ "]"

			for text in reply:
				await ctx.channel.send(text)


def setup(bot):
	bot.add_cog(Control(bot))