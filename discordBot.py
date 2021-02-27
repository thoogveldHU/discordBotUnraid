import discord
import subprocess
import os
import socket
import zipfile

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author != client.user: #If message is not from the bot itself
        
        #====== Below this line, there are the 'admin' commands =====================================================

        if message.content.lower().startswith("$restart"):
            if message.author.guild_permissions.administrator or str(message.author.id) == '270934134627500033': #User that send the message is admin or is TheDankestPutin (:
                subprocess.call(['sh','./restartValheimDocker.sh'])
                await message.add_reaction('👍')
            else:
                await message.channel.send("You're not an admin. ({})".format(message.author.id))

        elif message.content.lower().startswith("$load_backup"): #Needs work
            if message.author.guild_permissions.administrator or str(message.author.id) == '270934134627500033': #User that send the message is admin or is TheDankestPutin (:
                #list the backups by date?

                #Get user input from x ?

                #shut off server

                #replace the current save folder with the unzipped backup file.
                await message.add_reaction('👍')
                pass
            else:
                await message.channel.send("You're not an admin. ({})".format(message.author.id))

        #====== Below this line, there are no 'admin' commands =====================================================

        elif message.content.lower().startswith("$ip"): #Works
            await message.reply(str(socket.gethostbyname('valheim.hoogveld.me')))

        elif message.content.lower().startswith("$save_backup"): #needs works            
            currentWorldFolder = '../appdata/valheim2/.config'
            backupFolder = '../appdata/valheim2/Backups/'
            
            #Zip
            zipf = zipfile.ZipFile("python.zip",'w',zipfile.ZIP_DEFLATED)
            zipdir(currentWorldFolder,zipf)
            zipf.close()

            #Place in backup folder.
            #TO-DO
            
            await message.add_reaction('👍')
            pass

        elif message.content.lower().startswith('$download_backup'): #needs work
            await message.add_reaction('👍')
            pass

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))
 

TOKEN = None
with open('token.txt') as f:
    TOKEN = f.readlines()[0]

client.run(TOKEN)
