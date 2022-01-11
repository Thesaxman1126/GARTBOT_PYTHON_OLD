#IMPORTS#
import discord
from discord.ext import commands, tasks
import random
from discord import FFmpegPCMAudio
import youtube_dl
import os
from discord import Spotify
import asyncio
from discord.utils import get


#SET UP TYPE TIME
type_time = random.uniform(0.5, 2)

#SETUP OF THE BOT#
intents = discord.Intents.default()
intents.members = True
intents.messages = True
token = 'YOUR TOKEN HERE'
client = commands.Bot(command_prefix='&', intents = intents)


#EVENTS#
#STARTUP
@client.event
async def on_ready():
    change_status.start()
    
    print('Ya boi be running (Hopefully smoothly)')

@client.event
async def on_member_join(member):
	welcome = client.get_channel(870128815119138887)
	print('Someone has joined a server')
	await welcome.send(f'Welcome {member.mention}')

@client.event
async def on_member_remove(member):
	leave = client.get_channel(870128815119138887)
	print('A bitch left a server')
	await leave.send(f'{member.mention} is a bitch for leaving the server')

@client.event
async def on_voice_state_update(member, prev, cur):
    user = f"{member.name}#{member.discriminator}"
    if cur.afk and not prev.afk:
        print(f"{user} went AFK!")
				
    elif prev.afk and not cur.afk:
        print(f"{user} is no longer AFK!")
    elif cur.self_mute and not prev.self_mute: # Would work in a push to talk channel
        print(f"{user} stopped talking!")
    elif prev.self_mute and not cur.self_mute: # As would this one
        print(f"{user} started talking!")

@client.event
async def on_message(message):
	#No scooby#
	if '>>r34 scoob' in message.content.lower():
		
		await message.author.send(f"You\'re a sicko {message.author.mention}")
		print('Keyword Scoob found in message')
		await message.channel.send(f'NO SCOOBY {message.author.mention}')
	

	#Hello there -> General Kenobi#
	if message.content.lower() == 'hello there' : 
		await message.channel.send('GENERAL KENOBI')
		await message.channel.send('https://media.giphy.com/media/8JTFsZmnTR1Rs1JFVP/giphy.gif')
		await message.add_reaction('\N{THUMBS UP SIGN}')

	#Sorry -> apolocheese#
	if 'sorry' in message.content.lower():
		await message.channel.send(f"{message.author.mention} did you mean...")
		await message.channel.send('https://media.discordapp.net/attachments/690355066279952384/864685693992173588/Screenshot_2021-05-21-18-41-592.png?width=600&height=572')
	
	#Gart -> I've been summoned (with mention)#
	if 'gart' in message.content.lower():
		await message.channel.send(f"{message.author.mention} has summoned me")
	await client.process_commands(message)   



#TASKS#
#Do math faster every two minutes
@tasks.loop(minutes = 2)
async def change_status():
	
	GARTisms = ['@everyone Do Math Faster', '@everyone Yeah I\'m happy with this grade distribution.', '@everyone If you do the GRE faster you do better in Grad school']
	channel = client.get_channel(870128815119138887)
	await client.change_presence(activity=discord.Game('with your emotions'))
	print('Reminded them to do math faster.')
	await channel.send(random.choice(GARTisms))




#COMMANDS#
#&hello, Says Hello and mentions the author
@client.command(aliases = ['Hello', 'Hi', 'hi'])
async def hello(ctx):
	async with ctx.typing():
		await asyncio.sleep(type_time)
	await ctx.send(f"Hello {ctx.author.mention}!", mention_author = True)
    
#&ping, Says pong and latency
@client.command()
async def ping(ctx):
	print('A User sent a ping, sending a ping back')
	async with ctx.typing():
		await asyncio.sleep(type_time)
	await ctx.send(f'Pong! {round(client.latency * 1000)} ms.\nIn that time I did 1,000 calculations and they\'re all correct. ')

#&8ball, Gives response to Y/N question
@client.command(aliases = ['8ball'])
async def _8ball(ctx, *, question):
	responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
	"Don’t count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "My reply is no.", "My sources say no.",
	"Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.", "Without a doubt.",
	"Yes.", "Yes – definitely.", "You may rely on it.", "Who's to say?"]
	async with ctx.typing():
		await asyncio.sleep(type_time)
	await ctx.send(f'Quesion: {question}\nAnswer: {random.choice(responses)}')

#>clear, Clears a certain amount of msgs (default 5 but if you give it an int it will clear that many msgs)
@client.command(aliases = ['clc'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit = amount)

#&join command, Join Voice Chat
@client.command()
async def join(ctx):
		if (ctx.author.voice):
			channel = ctx.author.voice.channel
			await channel.connect()
			await ctx.send('Joining you creatures.')

		else:
			await ctx.send('You are not in a voice channel. I cannot join you\nPathetic.')


#&leave command, Leaves The Voice Chat
@client.command()
async def leave(ctx):
		await ctx.voice_client.disconnect()

#&Kick, Kicks member given a mention
@client.command()
async def kick(ctx, member:discord.Member, *, reason = None):
	if reason == None:
		await member.send(f'You got kicked for no reason\nYou\'re probably just a prick')
		await member.kick(reason = reason)
		await ctx.send(f'Kicked {member.mention} for no reason')
	else:
		await member.send(f'You got kicked for the following reason\n\"{reason}\"')
		await member.kick(reason = reason)
		await ctx.send(f'Kicked {member.mention} for the following reason:\n\" {reason}\"')


#&Ban, Bans member given a mention
@client.command()
async def ban(ctx, member:discord.Member, *, reason = None):
	await member.send(f'You got banned for the following reason\n\"{reason}\"')
	await member.ban(reason = reason)
	if reason == None:
		await ctx.send(f'Banned {member.mention}')
		await member.send("You got banned with ")
	else: 
		await ctx.send(f'Banned {member.mention} for the following reason:\n\"{reason}\"')

#&Unban, Unbans a member given the name and discriminator 
@client.command()
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	memeber_name, member_discriminator = member.split('#')

	for ban_entry in banned_users:
		user = ban_entry.user

		if (user.name, user.discriminator) == (memeber_name, member_discriminator):
			await ctx.guild.unban(user)
			await ctx.send(f"I've shown mercy and unbanned {user.mention}")
			return



#&Play command, plays a yt video's audio given a url, kinda slow
@client.command()
async def play(ctx, url:str):
		if (ctx.author.voice):
			channel = ctx.author.voice.channel
			voice = await channel.connect()


			ydl_opts = {
				'format': 'bestaudio/best',
				'postprocessors': [{
					'key': 'FFmpegExtractAudio',
					'preferredcodec': 'mp3',
					'preferredquality': '192'
				}]
				}

			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				ydl.download([url])
			for file in os.listdir("./"):
				if file.endswith(".mp3"):
					os.rename(file, "song.mp3")


			source = FFmpegPCMAudio('song.mp3')
			player = voice.play(source)		
			await ctx.send('Playing the only song that matters.')

		else:
			await ctx.send('You are not in a voice channel. I cannot join you\nPathetic.')


#&poke, Dm's mentioned user a message.
@client.command()
async def poke(ctx, user: discord.Member = None, *, memo):

    if user is None:
        await ctx.send("Incorrect Syntax:\nUsage: `!poke [user]`")

    await user.send(memo)

#&free, prunes memebers without any given role
@client.command()
async def free(ctx, role: discord.Role):
    [await member.kick() for member in ctx.guild.members if role in member.roles]
		
#&members
@client.command()
async def members(ctx):
    members = ctx.guild.members
    for member in members:
        await ctx.send(member.name)
    await ctx.send("done")

client.run(token)
