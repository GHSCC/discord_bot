import discord
import requests
import json
from configparser import ConfigParser
from os import listdir
from os.path import isfile

config = ConfigParser()
config.read('config.ini')

token = config.get('data', 'token')
StudentRole = config.getint('roles', 'StudentRole')
AdvisorRole = config.getint('roles', 'AdvisorRole')
AssignmentsPath = config.get('folders', 'assignmentsPath')

helpersPath = config.get('folders', 'HelpersPath')

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content.startswith('$help'):
        files = {}
        for i in listdir(helpersPath):
            if isfile(helpersPath + i):
                with open(helpersPath + i, 'r') as f:
                    files[i] = f.read()
                    f.close()
        for i in message.author.roles:
            if i.id == StudentRole:
                text = files['StudentCommands.txt']
                await message.channel.send(f'```{text}```')

            elif i.id == AdvisorRole:
                text = files['AdvisorCommands.txt']
                await message.channel.send(f'```{text}```')

    elif message.content.startswith('$register'):
        for i in message.author.roles:
            if i.id == StudentRole:
                await message.channel.send("You already have the Student role. "
                                           "If you want to switch, message a moderator.")
                return
            elif i.id == AdvisorRole:
                await message.channel.send("You already have the advisor role")
                return

        role = discord.utils.get(message.author.guild.roles, name="Student")
        try:
            await message.author.add_roles(role)
            await message.channel.send(f'Student role given to {message.author}')
        except discord.Forbidden:
            await message.channel.send('I don\'t have the permission to do that, contact a moderator')

    elif message.content.startswith('$assign_assignment'):
        with open('Database/assignments.json', 'r') as f:
            assignments = json.load(f)
            f.close()

        if len(message.attachments) > 0:
            description = message.content[18:]
            for file in message.attachments:
                if len(description) < 1:
                    await message.channel.send('Please provide a description \n'
                                               '$assign_assignment [description]')
                    return
                elif '.txt' not in file.filename:
                    await message.channel.send('Send a .txt file!')
                    return
                else:
                    # Downloading and saving the uploaded file
                    r = requests.get(file.url)
                    with open(AssignmentsPath+file.filename, 'w') as f:
                        f.write(str(r.content))
                        f.close()

                    # updating the database
                    assignments['AssignmentFileName'] = file.filename
                    assignments['description'] = description

                    await message.channel.send('the file has been downloaded and recorded in the database')
        else:
            await message.channel.send('Attach a text file!')
        with open('Database/assignments.json', 'w') as f:
            json.dump(assignments, f)
            f.close()

    elif message.content.startswith('$submit_assignment'):
        await message.channel.send('Command has not been coded yet')

    elif message.content.startswith('$check_assignment'):
        await message.channel.send('Command has not been coded yet')

    elif message.content.startswith('$assignment_progress'):
        await message.channel.send('Command has not been coded yet')


client.run(token)
