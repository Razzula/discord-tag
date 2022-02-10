import discord

f = open("token.txt", "r")
token = f.read()
f.close()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user} (discord-tag)\n'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user: #ignore self
        return

client.run(token)