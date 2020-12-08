# bot.py
import os

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from dotenv import load_dotenv
import json
from re import search

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    # activity = discord.Game(name="to Lore", type=2)
    await client.change_presence(activity=discord.Streaming(name="to Lore", url=""))


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hello, {member.name}, welcome traveller!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if search("^!lore", message.content):
        if len(message.content) > 6:
            # Get Search Key
            searchKey = message.content[6:]

            # Open Data
            with open('./lore_books/rimworld.json') as f:
                data = json.load(f)
            print(data)

            # Find Lore
            found = False
            for lore in data:
                if searchKey.lower() in lore["title"].lower():
                    title = lore["title"]
                    description = lore["description"]
                    image = lore["image"]
                    found = True
            if not found:
                for lore in data:
                    if searchKey.lower() in lore["description"].lower():
                        title = lore["title"]
                        description = lore["description"]
                        image = lore["image"]
                        found = True

            # Send Lore if Found
            if found:
                embed = discord.Embed(title=title, colour=discord.Colour(0x78dfee), description=description)
                if len(image) > 0:
                    embed.set_thumbnail(url=image)
                await message.channel.send(embed=embed)
            else:
                response = 'The term ' + str(searchKey) + ' was not found...'
                await message.channel.send(response)
        else:
            await message.channel.send("Please type something to search after the command...")

client.run(TOKEN)
