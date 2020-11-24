import discord
import requests
from Database import helpers
from os import listdir


config = helpers.getConfig()
client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content.startswith('$help'):

        for i in message.author.roles:
            text = helpers.getHelpFile(i.id)
            if text:
                await message.channel.send(f'```{text}```')

    elif message.content.startswith('$register'):
        for i in message.author.roles:
            if i.id == config['StudentRole']:
                await message.channel.send("You already have the Student role. "
                                           "If you want to switch, message a moderator.")
                return
            elif i.id == config['AdvisorRole']:
                await message.channel.send("You already have the advisor role")
                return

        role = discord.utils.get(message.author.guild.roles, name="Student")
        try:
            await message.author.add_roles(role)
            await message.channel.send(f'Student role given to {message.author}')
        except discord.Forbidden:
            await message.channel.send('I don\'t have the permission to do that, contact a moderator')

    elif message.content.startswith('$assign_assignment'):
        assignments = helpers.load_assignments()

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
                    for i in listdir(config['AssignmentsPath']):
                        if config['AssignmentsPath'] + i == config['AssignmentsPath'] + file.filename:
                            await message.channel.send('the file already exist')
                            return

                    r = requests.get(file.url)
                    with open(config['AssignmentsPath'] + file.filename, 'w') as f:
                        f.write(r.text)
                        f.close()

                    # updating the database
                    assignments['AssignmentFileName'] = file.filename
                    assignments['description'] = description

                    await message.channel.send('the file has been uploaded and recorded in the database')
        else:
            await message.channel.send('Attach a text file!')

        helpers.save_assignments(assignments)

    elif message.content.startswith('$assignment_progress'):
        assignments = helpers.load_assignments()

        if len(assignments['submissions']) < 1:
            await message.channel.send('No one have submitted the assignment!, Idiots')
            return
        text = ""
        for username in assignments['submissions']:
            text += username + '\n'
        await message.channel.send(f'The following users have submitted the assignment \n {text}')

    elif message.content.startswith('$submit_assignment'):
        assignments = helpers.load_assignments()

        if len(message.attachments) > 0:
            for file in message.attachments:
                if '.txt' not in file.filename:
                    await message.channel.send('Send a .txt file!')
                    return
                else:
                    # Downloading and saving the uploaded file
                    for i in listdir(config['SubmissionsPath']):
                        if config['SubmissionsPath'] + i == config['SubmissionsPath'] + file.filename:
                            await message.channel.send(
                                'a file with the same name already exists, use a different filename please')
                            return

                    r = requests.get(file.url)
                    with open(config['SubmissionsPath'] + file.filename, 'w') as f:
                        f.write(r.text)
                        f.close()

                    # updating the database
                    username = message.author.display_name
                    if username not in assignments['submissions']:
                        assignments['submissions'][username] = file.filename
                        await message.channel.send('the file has been uploaded and recorded in the database')
                    else:
                        await message.channel.send('You have already submitted a file!')

        else:
            await message.channel.send('Attach a text file!')
        helpers.save_assignments(assignments)

    elif message.content.startswith('$check_assignment'):
        assignments = helpers.load_assignments()

        for i in assignments['submissions']:
            if i == message.author.display_name:
                await message.channel.send("You don't have an assignment waiting for you!")
                return

        await message.channel.send('You have one assignment!')
        await message.channel.send(file=discord.File(config['AssignmentsPath'] + assignments['AssignmentFileName']))


client.run(config['token'])
