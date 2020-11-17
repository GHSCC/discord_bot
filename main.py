import discord
import config as c

client = discord.Client()
roles = {'Student': 778053523187040297,
         'Advisor': 778053252431609868}


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$help'):
        await message.channel.send('identifier $ ')
        # TODO: finish this crap

    if message.content.startswith('$register'):
        for i in message.author.roles:
            if i.id == roles['Student']:
                await message.channel.send("You already have the Student role. "
                                           "If you want to switch, message a moderator.")
                return

        role = discord.utils.get(message.author.guild.roles, name="Student")
        try:
            await message.author.add_roles(role)
            await message.channel.send(f'Student role given to {message.author}')
        except discord.Forbidden:
            await message.channel.send('I don\'t have the permission to do that, contact a moderator')

client.run(c.token)
