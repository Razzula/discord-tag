import discord

f = open("token.txt", "r")
token = f.read()
f.close()

intents = discord.Intents.default()
intents.members = True
activity = discord.Game(name="Tag")
client = discord.Client(intents=intents, activity=activity)

@client.event
async def on_ready():
    print('Logged in as {0.user} (discord-tag)\n'.format(client))

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

            #get tagged user's id
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

            #remove role
            user = message.author
            await user.remove_roles(tagRole)

            #assign role
            user = message.guild.get_member(id)
            await user.add_roles(tagRole)

client.run(token)