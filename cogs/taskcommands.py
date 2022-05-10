from discord.ext import commands
import discord
import os
import json
from pathlib import Path

class Tasks(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.file = 'data\data.json'
		self.codefile = 'data\code.json'
		self.code = 0000

		self.taskList = {
			"Wood" : "Farm wood.",
			"Stone" : "Farm stone.",
			"Metal" : "Farm metal ore.",
			"Recycle" : "Recycle for scrap and other resources.",
			"Nodes" : "Farm nodes for furnaces.",
			"Patrol" : "Patrol the furnaces, roof or compound."
		}

	@commands.Cog.listener()
	async def on_ready(self):
		print("COG : Task has been loaded.")

	@commands.command()
	async def clear(self, ctx, amount=5):
		await ctx.channel.purge(limit=amount)

	@commands.command()
	async def assign(self,ctx, member: discord.Member = None):

		def check(msg):
			return msg.author.id == ctx.author.id and msg.channel.id == ctx.channel.id

		commander = discord.utils.get(ctx.guild.roles, name="Commander")

		if commander in ctx.author.roles:

			respEmbed1 = discord.Embed(title=member.name + "'s Task'",description="Please respond with the task " + member.name + " will be assigned.\nExample `Farm some wood.`\nHere are some suggestions : \n\n",color =0x6535c4)

			for pTask in self.taskList:
				respEmbed1.add_field(name=pTask,	value=self.taskList[pTask])

			await ctx.send(embed=respEmbed1)

			theTask = await self.client.wait_for("message", check=check)

			confirmEmbed = discord.Embed(title="Confirm Task",description="Are you sure you would like " + member.name + " to `" + theTask.content + "`?\nPlease respond `yes` or `no`.")
			await ctx.send(embed=confirmEmbed)

			theDecision = await self.client.wait_for("message", check=check)

			if (theDecision.content == "yes"):
				respEmbed2 = discord.Embed(title="Task Sent",description=member.name + " will be asked to " + theTask.content + "\nYou will be sent a PM on completion!",color=discord.Color.green())
				
				await ctx.send(embed=respEmbed2)

				with open(self.file) as f:
					data = json.load(f)

				data[member.id] = {"Task" : theTask.content, "Owner" :  ctx.author.id}

				with open(self.file, 'w') as f:
					json.dump(data, f)

				notifyEmbed = discord.Embed(title="New Task",description="You have been assigned a new task from " + ctx.author.name + "!\n\nTask : `" + theTask.content + "`\nTo complete this task you can reply `!done`.")
				
				await member.send(embed=notifyEmbed)

			elif (theDecision.content == "no"):
				badResponseEmbed = discord.Embed(title="Cancel Task",description=member.name + " will not be asked to " + theTask.content,color=discord.Color.green())
				await ctx.send(embed=badResponseEmbed)
			else:

				badResponseEmbed = discord.Embed(title="Bad Response",description="Please try again!",color=discord.Color.red())
				
				await ctx.send(embed=badResponseEmbed)

		else:

			deniedEmbed = discord.Embed(title="Lacking Permission",description="You do not have the require permission!",color=discord.Color.red())
			
			await ctx.send(embed=deniedEmbed)

	@commands.command()
	async def done(self,ctx):

		def check(msg):
			return msg.author.id == ctx.author.id and msg.channel.id == ctx.channel.id

		confirmEmbed = discord.Embed(title="Are you sure?",description="Are you sure you have completed your task?\nPlease respond `yes` or `no`.",color=0x6535c4)
		
		await ctx.send(embed=confirmEmbed)

		response = await self.client.wait_for("message", check=check)

		if (response.content == "yes"):

			completeEmbed = discord.Embed(title="Task Complete",description="The task owner will be sent a PM of completion!",color=discord.Color.green())
			
			await ctx.send(embed=completeEmbed)

			try:
				with open(self.file) as f:
					data = json.load(f)

				taskCompleteEmbed = discord.Embed(title="Task Submission",description= ctx.author.name + " has confirmed they have completed their task.\n\nTask : `" + data[str(ctx.author.id)]['Task'] + '`',color=0x6535c4)
				
				user = await self.client.fetch_user(data[str(ctx.author.id)]['Owner'])

				await user.send(embed=taskCompleteEmbed)

				del data[str(ctx.author.id)]

				with open(self.file, 'w') as f:
					json.dump(data, f)

			except Exception as e:
				print("Error : " + e)

				errorEmbed = discord.Embed(title="Task not found",description="Are you sure you have been assigned a task?",color=discord.Color.red())
				
				await ctx.send(embed=errorEmbed)
		else:

			cancelEmbed = discord.Embed(title="Action Discontinued",description="Seeya!",color=0x6535c4)
			
			await ctx.send(embed=cancelEmbed)

	@commands.command()
	async def setcode(self,ctx):
		def check(msg):
			return msg.author.id == ctx.author.id and msg.channel.id == ctx.channel.id

		trusted = discord.utils.get(ctx.guild.roles, name="Trusted")

		if (trusted in ctx.author.roles):

			confirmEmbed = discord.Embed(title="Confirm",description="Are you sure you would like to set the clan base code?\nPlease respond `yes` or `no`.",color =0x5626b5)
			await ctx.send(embed=confirmEmbed)

			response = await self.client.wait_for("message", check=check)

			if (response.content == "yes"):

				codeEmbed = discord.Embed(title="New Code",description="Please enter the new 4 digit code.")
				await ctx.send(embed=codeEmbed)

				newCode = await self.client.wait_for("message", check=check)

				if (len(newCode.content) == 4 and newCode.content.isdigit()):
					with open(self.codefile) as f:
						data = json.load(f)

					data["Code"] = newCode.content

					with open(self.codefile, 'w') as f:
						json.dump(data, f)

					codeSetEmbed = discord.Embed(title="Code Set",description="The new code is now `" + newCode.content + "`")
					self.code = newCode.content
					await ctx.send(embed=codeSetEmbed)
				else:
					errorEmbed = discord.Embed(title="Woops",description="Please try again using 4 digits.",color=discord.Color.red())
					await ctx.send(embed=errorEmbed)

	@commands.command()
	async def getcode(self,ctx):
		with open(self.codefile) as f:
			data = json.load(f)

		codeEmbed = discord.Embed(title="Base Code",description="Your base code is : `" +  data["Code"] + "`")
		await ctx.author.send(embed=codeEmbed)



def setup(client):
	client.add_cog(Tasks(client))
