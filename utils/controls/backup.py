import discord
from discord.ext import commands

import asyncio
import subprocess

class Backup(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def run_cmd(self, cmd):
		subprocess.run(cmd)
		return 1

	@commands.has_role('Creeper')
	@commands.cooldown(1, 60*60*2)
	@commands.command(
		name = "backup",
		brief = "backup the minecraft/ directory on the server",
		description = "backup the minecraft/ directory on the server using bzip2 compression. (1 invoke per 2 hours)",
		enabled = True
	)
	async def backup(self, ctx):
		await ctx.channel.send("Backup has begun. It may take anywhere from 5 minutes to 15 minutes")

		try:
			task = self.bot.loop.create_task(self.run_cmd("meccraftbackup"))
			done, pending = await asyncio.wait({task})

			if task in done:
				await ctx.channel.send("Backup Completed!")

		except Exception as e:
			await ctx.channel.send("Failed " +str(e))

def setup(bot):
	bot.add_cog(Backup(bot))