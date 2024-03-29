# bot.py
import os

import discord
from dotenv import load_dotenv

from lib import Rolling as roll, Help as help, gSheetReference as sheet, userDataBase as connect

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$roll'):
        await message.channel.send(embed = createEmbed(message.author, roll.GetSuccess(message.content)))
    
    if message.content.startswith('$lookup'):
        await message.channel.send(embed = createEmbed(message.author, sheet.Lookup(message.content)))
    
    if message.content.startswith('$help'):
        await message.channel.send(embed = createEmbed(message.author, help.HelpCommand(message.content)))
    
    if message.content.startswith('$import'):
        await message.channel.send(embed = createEmbed(message.author, connect.importSheet(message)))
    
    if message.content.startswith('$list'):
        await message.channel.send(embed = createEmbed(message.author, connect.listSheets(message)))
    if message.content.startswith('$char'):
        try:
            await message.channel.send(embed = createEmbed(message.author, connect.setCurrent(message)))
        except:
            text = ["Oops!", "You currently have no Characters. Attach one now using `$import [url]` now!", '$char']
            await message.channel.send(embed = createEmbed(message.author, text))
    if message.content.startswith('$check'):
        try:
            await message.channel.send(embed = createEmbed(message.author, connect.rollSheet(message)))
        except:
            text = ["Oops!", "You currently have no Characters. Attach one now using `$import [url]` now!", "$check"]
            await message.channel.send(embed = createEmbed(message.author, text))

def createEmbed(author, content = []):
    #Content follows format of Heading, Body, Footer
    embed = discord.Embed(title=content[0], url="http://www.Google.com", description=content[1], color=0xFAA61A)
    embed.set_footer(text=content[2])
    if len(content) == 4:
        embed.set_thumbnail(url=content[3])
    embed.set_author(name=author, icon_url= author.avatar)
    return embed



client.run(TOKEN)