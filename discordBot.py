import discord
import subprocess
import os
import socket
import zipfile
import shutil
import datetime
import seafileapi

client = discord.Client()

filesDict = {}

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

        elif message.content.lower().startswith("$save_backup"): #Works
            try:         
                currentWorldFolder = 'currentFolder/.config' #CurrentFolder is mapped in the runMe.sh ---> currentFolder = /mnt/user/appdata/valheim2
                backupFolder = 'currentFolder/Backups/'
                fileName = str(datetime.datetime.now()).replace(' ','_') + '.zip'

                #Zip
                zipf = zipfile.ZipFile(fileName,'w',zipfile.ZIP_DEFLATED)
                zipdir(currentWorldFolder,zipf)
                zipf.close()

                #Place in backup folder. The python.zip is in the root of the docker container.
                shutil.move(fileName,backupFolder)
                await message.add_reaction('👍')
            except Exception as e:
                #await message.channel.send(str(e))
                await message.add_reaction('👎')


        elif message.content.lower().startswith('$list_backup'): #needs work
            try:
                backupFolder = 'currentFolder/Backups/'

                fileNames = [filename for filename in os.listdir(backupFolder) if filename.endswith('.zip')]

                for i,file in enumerate(fileNames):
                    if str(file).endswith(".zip"):
                        filesDict[i] = file

                await message.channel.send(filesDict)
                await message.add_reaction('👍')
            except Exception as e:
                await message.channel.send(e)

        elif message.content.lower().startswith('$download_backup'): #needs work
            try:
                backupFolder = '/currentFolder/Backups/'
                
                intFound = -1
                for word in message.content:
                    try:
                        intFound = int(word)
                        break
                    except Exception:
                        pass
                
                if intFound != -1:

                    #Getting the password from the server from the txt file
                    SEAFILE_PASSWORD = ''
                    with open('seafilepassword.txt') as f : SEAFILE_PASSWORD = f.readlines()[0]

                    #Getting the directory we need to upload to
                    c = seafileapi.connect('https://seafile.hoogveld.me', 'twan@hoogveld.me', '{}'.format(SEAFILE_PASSWORD))
                    repos = c.repos.list_repos()
                    valheimRepo = [repo for repo in repos if repo.name == 'backups_valheim'][0]
                    valheimDir = valheimRepo.get_dir('/')

                    #upload the file into this directory
                    full_name_of_file = backupFolder + str(filesDict[intFound])
                    valheimDir.upload_local_file(full_name_of_file) #ERROR HERE

                    #create a link to the file
                    website = 'https://seafile.hoogveld.me/d/e050bf894bb749339c06/files/?p=/{}'.format(str(filesDict[intFound]))
                    
                    #send the link to the channel
                    await message.channel.send(website)
                    await message.add_reaction('👍')
                else:
                    await message.channel.send('Need to know which backup you want nibba')

            except Exception as e:
                await message.channel.send(e)

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))
 

TOKEN = None
with open('token.txt') as f:
    TOKEN = f.readlines()[0]

client.run(TOKEN)
