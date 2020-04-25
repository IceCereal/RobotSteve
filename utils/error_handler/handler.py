import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound):
			await ctx.send("Command not found. Type ++help for a list of the commands.")

		elif isinstance(error, commands.CommandOnCooldown):
			await ctx.send("You need to wait **{:.2f}s**.".format(error.retry_after))

		elif isinstance(error, commands.MissingRole):
			await ctx.send("You can't do that unless you have the {} role.".format(error.missing_role))

		elif isinstance(error, commands.NotOwner):
			await ctx.send("Yeah... no, you can't do that.")

		else:
			await ctx.send("Something went wrong.")

def setup(bot):
	bot.add_cog(ErrorHandler(bot))