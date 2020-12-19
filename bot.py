# bot.py
import os

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from dotenv import load_dotenv
import json
from re import search
import requests
from loggingChannel import sendLog

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(await sendLog(log=(f'{client.user} has connected to Discord!'), client=client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Lore"))
    channel = client.get_channel(785703473147936808)
    await channel.send("Ready")


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(await sendLog(log=(f'Hello, {member.name}, welcome traveller!'), client=client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    mentions = message.mentions
    if len(mentions) > 0:
        if mentions[0].id == 785611565075791922:
            if search("^!quit", message.content.lower()) and message.channel == client.get_channel(789190323326025789):
                await client.logout()

    if search("^!lore", message.content):
        length = 6
    if search("^\?", message.content):
        length = 1
    if search("^!lore", message.content) or search("^\?", message.content):
        if len(message.content) > length:
            # Get Search Key
            searchKey = message.content[length:]

            server = message.guild.id
            # channel = client.get_channel(785703473147936808)
            # await channel.send("Server " + str(server))
            print(await sendLog(log=("Server: " + server), client=client))
            # Open Data Based on Server
            if server == 785611085418987531:
                path = './lore_books/rimworld.json'
            else:
                path = './lore_books/blank.json'
                await message.channel.send(f'No Lore was found for {message.guild.name}.')
                return

            with open(path) as f:
                data = json.load(f)
            print(await sendLog(log=("Data: \n" + data), client=client))

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
                        type = lore["type"]
                        found = True

            # Send Lore if Found
            if found:
                embed = discord.Embed(title=title, colour=discord.Colour(0x78dfee), description=description)
                if len(image) > 0:
                    embed.set_thumbnail(url=image)
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(title=str(searchKey), colour=discord.Colour(0x78dfee),
                                      description=('The term ' + str(searchKey) + ' was not found...'))
                await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="Incorrect Format", colour=discord.Colour(0x78dfee),
                                  description=('Please type !lore followed by the search.'))
            await message.channel.send(embed=embed)


client.run(TOKEN)
