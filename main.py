import discord
from discord.ext import commands

f = open("token.txt", "r")
token = f.read()
f.close()

intents = discord.Intents.default()
intents.members = True
activity = discord.Game(name="Tag")
client = commands.Bot(command_prefix='$', intents=intents, activity=activity)

@client.event
async def on_ready():
    print('Logged in as {0.user} (discord-tag)\n'.format(client))

@client.command()
async def setup(ctx):

    role = discord.utils.get(ctx.guild.roles, name="PlayingTag")
    if role == None:
        await ctx.guild.create_role(name="PlayingTag")

    role = discord.utils.get(ctx.guild.roles, name="It")
    if role == None:
        await ctx.guild.create_role(name="It")
    await role.edit(colour=0x9b59b6)

    #move role as high as possible
    try:
        pos = 1
        while True:
            await role.edit(position=pos)
            pos += 1
    except:
        await ctx.message.add_reaction('👍')

@client.event
async def on_message(message):
    if message.author == client.user: #ignore self
        return

    #if author is 'it'
    tagRole = discord.utils.get(message.guild.roles, name="It")
    if tagRole in message.author.roles:

        #if message contains mention
        if '<@' in str(message.content) and '&' not in str(message.content):
            if '<@!' in str(message.content):
                keynote = '!'
            else:
                keynote = '@'

            #get tagged user
            msg = str(message.content)
            temp = ''
            flag = False
            for i in range(len(msg)):
                if msg[i] == keynote:
                    flag = True
                    continue
                if flag:
                    if msg[i] == '>':
                        break
                    else:
                        temp += msg[i]
            id = int(temp)
            user = message.guild.get_member(id)

            #only pass on role if taggee is playing
            playerRole = discord.utils.get(message.guild.roles, name='PlayingTag')
            if playerRole in user.roles:

                #remove role
                user = message.author
                await user.remove_roles(tagRole)

                #assign role
                user = message.guild.get_member(id)
                await user.add_roles(tagRole)

    await client.process_commands(message)

client.run(token)