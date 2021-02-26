import discord
import subprocess
import os

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author != client.user: #If message is not from the bot itself
        
        if message.content.startswith("$restart"):
            if message.author.guild_permissions.administrator: #User that send the message is admin
                
                await message.channel.send("Restarting the Valheim Server now.")
                #Run the sh file from here, for now disabled since it's a test.
                #subprocess.call(['sh','./restartValheimDocker.sh'])
                
            else:
                await message.channel.send("You're not an admin.")
TOKEN = None
with open('token.txt') as f:
    TOKEN = f.readlines()[0]

client.run(TOKEN)
