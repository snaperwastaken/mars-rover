from imaplib import Commands
import discord
from discord import Intents, Client, Message
import os
from apod import a
import requests
from marsrover import *

intents: Intents = Intents.default()
intents.message_content = True

bot = Commands.bot(command_prefix="!", intents = discord.Intents.all())

os.environ['TOKEN'] = 'token here'

rovers = ['curiosity', 'opportunity', 'perseverance']
cam = ['chemcam', 'fhaz', 'navcam']

@bot.event
async def on_ready():
    print("Discord mod activated as {0.user}".format(bot))
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}!", ephemeral=True)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith("-picoftheday"):
        title = a.title
        date = a.date
        explanation = a.explanation
        url = a.url
        await message.channel.send(f'***NASA PICTURE OF THE DAY***\n\n**{title}**\n\n*{date}*\n\n{explanation}\n\n{url}\n')

token = os.environ['TOKEN']
bot.run(token)
