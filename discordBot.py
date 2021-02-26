import discord
import subprocess

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author != client.user:
        if message.content.startswith("$restart"):
            if message.author.guild_permissions.administrator: #isAdmin
                await message.channel.send("Restarting the Valheim Server now.")
                subprocess.call(['sh','./restartValheimDocker.sh'])
            else:
                await message.channel.send("You're not an admin.")

TOKEN = None
with open('token.txt') as f:
    TOKEN = f.readlines()[0]

client.run(TOKEN)