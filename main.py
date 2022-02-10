import discord
from discord.ext import commands
import random
import time

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
        role = await ctx.guild.create_role(name="It")
    await role.edit(colour=0x9b59b6)

    #move role as high as possible
    try:
        pos = 1
        while True:
            await role.edit(position=pos)
            pos += 1
    except:
        await ctx.message.add_reaction('👍')

@client.command()
async def re(ctx):
    file = open('leaderboard.txt', 'w')
    playerRole = discord.utils.get(ctx.guild.roles, name='PlayingTag')
    for user in ctx.guild.members:
        if playerRole in user.roles:
            file.write(str(user.id) + ':0\n')
    file.close()
    file = open('tolt.txt', 'w').close()
    print("File 'leaderboard.txt' reset")
    await ctx.message.add_reaction('👍')

@client.command()
async def le(ctx):
    tagRole = discord.utils.get(ctx.guild.roles, name="It")
            
    try:
        toltFile = open('tolt.txt', 'r')
        for line in toltFile:
            line = line.rstrip()
        toltFile.close()
        timeOfLastTag = float(line)
        try: #if file exists
            file = open('leaderboard.txt', 'r')
            leaderboard = []
            for line in file:
                line = line.rstrip()
                user = ctx.guild.get_member(int(line[0:18]))
                l = len(line)
                t = float(line[19:l])
                if tagRole in user.roles:
                    t += int(time.time() - timeOfLastTag)
                leaderboard.append([user.name, int(t)])
            file.close()

            flag = True
            while flag:
                flag = False
                for i in range(len(leaderboard) - 1):
                    if leaderboard[i][1] > leaderboard[i+1][1]:
                        temp = leaderboard[i]
                        leaderboard[i] = leaderboard[i+1]
                        leaderboard[i+1] = temp
                        flag = True
            
            counter = 0
            msg = ''
            for i in range(len(leaderboard)):
                #convert delta epoch to d/h/m/s
                temp = ' : '
                if leaderboard[i][1] > 86400:
                    value = int(leaderboard[i][1] / 86400)
                    leaderboard[i][1] -= value * 86400
                    temp += str(value) + 'd'
                if leaderboard[i][1] > 3600:
                    value = int(leaderboard[i][1] / 3600)
                    leaderboard[i][1] -= value * 3600
                    temp += str(value) + 'h'
                if leaderboard[i][1] > 60:
                    value = int(leaderboard[i][1] / 60)
                    leaderboard[i][1] -= value * 60
                    temp += str(value) + 'm'

                #if bot is winning, give 1st place to actual player
                if i == 0:
                    if leaderboard[i][0] == str(client.user.name):
                        offset = 0
                    else:
                        offset = 1
                msg += '\n' + str(i+offset) + '. ' + leaderboard[i][0] + temp + str(leaderboard[i][1]) + 's'

                #add medals
                if offset == 0: #if bot winning, skip medal
                    counter -= 1
                elif counter == 0:
                    msg += ' 🥇'
                elif counter == 1:
                    msg += ' 🥈'
                elif counter == 2:
                    msg += ' 🥉'
                counter += 1
            await ctx.message.channel.send(msg)
        except:
            await ctx.message.channel.send("Error: Leaderboard not found")
    except:
        if tagRole == None:
            await ctx.message.channel.send("Game not setup. Run `$setup` first.")
        else:
            await ctx.message.channel.send("Game hasn't started yet. <@&" + str(tagRole.id) + ">, tag someone to begin the game.")

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
                await message.author.remove_roles(tagRole)

                #time tracking
                leaderboard = []
                try: #if file exists
                    file = open('leaderboard.txt', 'r')
                    for line in file:
                        line = line.rstrip()
                        leaderboard.append(line)
                    file.close()

                except: #otherwise, create new file and fill with players
                    print("File 'leaderboard.txt' not found")
                    for user in message.guild.members:
                        if playerRole in user.roles:
                            leaderboard.append(str(user.id) + ':0')
                    print("New leaderboard created")

                #assign role
                offset = 0
                if user.id == client.user.id: #if bot is tagged
                    await user.add_roles(tagRole)
                    if random.randint(0, 100) < 40:
                        responses = ['https://tenor.com/view/starwars-han-solo-tag-youre-it-stormtrooper-gif-20240479', 'https://tenor.com/view/monty-python-holy-grail-horse-on-my-way-omw-gif-13663405', 'https://imgur.com/VVMZWAn', 'https://tenor.com/view/halo-master-chief-halo-infinite-xbox-xbox-series-x-gif-19586612']
                        await message.channel.send(random.choice(responses))
                    time.sleep(2)
                    offset = 2

                    await user.remove_roles(tagRole)

                    for i in range(len(leaderboard)):
                        line = leaderboard[i]
                        if int(line[0:18]) == user.id:
                            l = len(line)
                            delta = float(line[19:l]) + 2
                            leaderboard[i] = line[0:18] + ':' + str(delta)

                    n = message.guild.member_count - 1
                    while playerRole not in user.roles or user.id == client.user.id: #no tagging non-players, or self
                        user = message.guild.members[random.randint(0, n)]

                    await message.channel.send('<@' + str(user.id) + '>')
                await user.add_roles(tagRole)

                #store data in file
                file = open('leaderboard.txt', 'w')
                for line in leaderboard:
                    if int(line[0:18]) == message.author.id:
                        l = len(line)
                        try:
                            toltFile = open('tolt.txt', 'r')
                            for item in toltFile:
                                item = item.rstrip()
                                timeOfLastTag = float(item)
                            toltFile.close()
                            delta = int(time.time() - timeOfLastTag + float(line[19:l]) - offset)
                        except:
                            print("'timeOfLastTag' is undefined")
                            delta = int(float(line[19:l]))
                        file.write(str(message.author.id) + ':' + str(delta) + '\n')
                    else:
                        file.write(line + '\n')
                file.close()
                timeOfLastTag = time.time()
                file = open('tolt.txt', 'w')
                file.write(str(timeOfLastTag))
                file.close()

    await client.process_commands(message)

client.run(token)