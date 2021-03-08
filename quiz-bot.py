import discord
import json
import random

from discord.ext import commands
client = commands.Bot(command_prefix="/", hello_command=None)

emoji_library       = ["😄", "😆", "😅", "😂", "🙃", "😉", "😇", "🥰", "😍", "😘", "😙", "😋", "😛", "😜", "🤪", "😝", "🤑", "🤗", "🤭", "🤫", "🤔", "🤐", "🙄", "😴", "🥴", "😵", "🤠", "🥳", "😎", "🤓", "🧐", "😲", "😳", "😱", "🥱", "😤", "🤡", "👽", "👾"]

@client.command(name="quiz", aliases=["q"])
async def hello_command(ctx, *args):

    # cap the max number of players
    if (len(args) > len(emoji_library)):
        return
    
    # save the players
    names = args

    emojis = []
    scores = []

    tmp = emoji_library
    for n in names:
        # initials of the score
        scores.append(0)

        # randomice avatars
        rand = random.randint(0, len(tmp)-1)

        emojis.append(tmp[rand])
        tmp.remove(tmp[rand])

    # send embed message
    embed=discord.Embed(title="Quiz Master 👀📝", description="press your emoji to buzzer")

    for i in range(len(names)):
        embed.add_field(name=names[i] + " " + emojis[i], value=scores[i], inline=True)

    message = await ctx.send(embed=embed)

    # add reactions
    for i in range(len(names)):
        await message.add_reaction(emojis[i])

@client.event
async def on_reaction_add(reactions, user):
    if (reactions.count <= 1):
        return

    if (reactions.message.author.discriminator != "3936"):
        return

    # TODO endscheide zwischen antwort und normal
    ctx = await client.get_context(reactions.message)

    emojis = []
    names = []
    answers = ["✅", "❌", "↩️"]
    scores = []

    for field in ctx.message.embeds[0].fields:
        names.append(field.name.split()[0])
        emojis.append(field.name.split()[1])
        scores.append(field.value)

    embed = None

    if (reactions.emoji in emojis):
        # buzzed

        index = None
        for i in range(len(emojis)):
            if (reactions.emoji == emojis[i]):
                index = i

        embed=discord.Embed(title="Quiz Master 👀📝", description=names[index] + " " + emojis[index] + " buzzed! Now, deside if he/she is right.")

        for i in range(len(names)):
            embed.add_field(name=names[i] + " " + emojis[i], value=scores[i], inline=True)

        await ctx.message.delete()
        message = await ctx.send(embed=embed)

        # add reactions
        for i in range(len(answers)):
            await message.add_reaction(answers[i])

    elif (reactions.emoji in answers):
        # answer given -> back to normal

        index = None
        for i in range(len(emojis)):
            if (ctx.message.embeds[0].description.split()[1] == emojis[i]):
                index = i

        if (reactions.emoji == "✅"):
            tmp = int(scores[index]) + 5
            scores[index] = str(tmp)

        elif (reactions.emoji == "❌"):
            for i in range(len(emojis)):
                if (i == index):
                    continue
                tmp = int(scores[i]) + 1
                scores[i] = str(tmp)

        # send embed message
        embed=discord.Embed(title="Quiz Master 👀📝", description="press your emoji to buzzer")

        for i in range(len(names)):
            embed.add_field(name=names[i] + " " + emojis[i], value=scores[i], inline=True)

        await ctx.message.delete()
        message = await ctx.send(embed=embed)

        # add reactions
        for i in range(len(names)):
            await message.add_reaction(emojis[i])


# handle discord token
config_file = open("config.json", "r").read()
config = json.loads(config_file)
token = config["token"]
client.run(token)