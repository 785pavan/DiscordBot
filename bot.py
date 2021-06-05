import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# client
client = discord.Client()


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel_send(
        f'HI {member.name}, Welcome to test server'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
        '"Title of your sex tape.” — Jake Peralta',

        '"Sarge, with all due respect, I am gonna completely ignore everything you just said.” — Jake Peralta',

        '"I ate one string bean. It tasted like fish vomit. That was it for me.” – Sergeant Jeffords',

        '"The English language can not fully capture the depth and complexity of my thoughts, '
        'so I’m incorporating emojis into my speech to better express myself. Winky face.” – Gina Linetti',

        '"A place where everybody knows your name is hell. You’re describing hell.” – Rosa Diaz',

        '"Cool, cool, cool, cool, cool. No doubt, no doubt, no doubt.” – Jake Peralta',

        '"If I die, turn my tweets into a book.” – Gina Linetti',

        '"Fine. but in protest, I’m walking over there extremely slowly!” – Jake',

        '"Jake, why don’t you just do the right thing and jump out of a window?” – Gina',

        '"I asked them if they wanted to embarrass you, and they instantly said yes.” – Captain Holt',

        '"Captain Wuntch. Good to see you. But if you’re here, who’s guarding Hades?” – Captain Holt',

        '"I’m playing Kwazy Cupcakes, I’m hydrated as hell, and I’m listening to Sheryl Crow. I’ve got my own party going on.” – Terry Jeffords',

        '"Anyone over the age of six celebrating a birthday should go to hell.” – Rosa Diaz',

        '"Captain, turn your greatest weakness into your greatest strength. Like Paris Hilton RE: her sex tape.” – Gina Linetti',

        '"Title of your sex tape.” — Amy Santiago'
    ]

    if message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)
    elif message.content == 'raise-exception':
        raise discord.DiscordException


@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


# client.run(TOKEN)


# bot

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord')


@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(context):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
        '"Title of your sex tape.” — Jake Peralta',

        '"Sarge, with all due respect, I am gonna completely ignore everything you just said.” — Jake Peralta',

        '"I ate one string bean. It tasted like fish vomit. That was it for me.” – Sergeant Jeffords',

        '"The English language can not fully capture the depth and complexity of my thoughts, '
        'so I’m incorporating emojis into my speech to better express myself. Winky face.” – Gina Linetti',

        '"A place where everybody knows your name is hell. You’re describing hell.” – Rosa Diaz',

        '"Cool, cool, cool, cool, cool. No doubt, no doubt, no doubt.” – Jake Peralta',

        '"If I die, turn my tweets into a book.” – Gina Linetti',

        '"Fine. but in protest, I’m walking over there extremely slowly!” – Jake',

        '"Jake, why don’t you just do the right thing and jump out of a window?” – Gina',

        '"I asked them if they wanted to embarrass you, and they instantly said yes.” – Captain Holt',

        '"Captain Wuntch. Good to see you. But if you’re here, who’s guarding Hades?” – Captain Holt',

        '"I’m playing Kwazy Cupcakes, I’m hydrated as hell, and I’m listening to Sheryl Crow. '
        'I’ve got my own party going on.” – Terry Jeffords',

        '"Anyone over the age of six celebrating a birthday should go to hell.” – Rosa Diaz',

        '"Captain, turn your greatest weakness into your greatest strength. Like Paris Hilton '
        'RE: her sex tape.” – Gina Linetti',

        '"Title of your sex tape.” — Amy Santiago'
    ]

    response = random.choice(brooklyn_99_quotes)
    await context.send(response)


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(context, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await context.send(', '.join(dice))


@bot.command(name='create-channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='bot_testing'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


bot.run(TOKEN)
