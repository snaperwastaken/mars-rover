from imaplib import Commands
import discord
from discord import Intents, Client, Message
from discord.ext import commands
import os
from apod import a
import requests
import random
from marsrover import mars_images

#lists
rovers = ['curiosity', 'opportunity', 'perseverance']
cameras = ['chemcam', 'fhaz', 'navcam', 'rhaz', 'mast', 'mahli', 'mardi', 'pancam', 'minites']

#setup discord bot
intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

os.environ['TOKEN'] = 'token here'

#if the bot is running/ the status
@bot.event
async def on_ready():
    print("Discord mod activated as {0.user}".format(bot))

#hello command
@bot.command()
async def hello(ctx):
    user = ctx.author
    category = 'knowledge'
    api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
    response = requests.get(api_url, headers={'X-Api-Key': 'i73mtuC9f6Utir25Z03oEg==7IC4TPmGuKg90vHk'})
    json_data = response.json()
    quote = json_data[0]['quote']
    author = json_data[0]['author']
    if response.status_code == requests.codes.ok:
        print (json_data)
        await ctx.channel.send(f"Hello there {user}! \n \"{quote}\" \n\n by {author}")
    else:
        await ctx.channel.send("Error:", response.status_code, response.text)

#APOD command
@bot.command()
async def apod(message):
    if message.author == bot.user:
        return
    else:
        title = a.title
        date = a.date
        explanation = a.explanation
        url = a.url
        await message.channel.send(f'***NASA PICTURE OF THE DAY***\n\n**{title}**\n\n*{date}*\n\n{explanation}\n\n{url}\n')

#MARS rover command
@bot.command()
async def mars(ctx, rover=None, sol=None, cam=None):

    msg_main = 'Here are some of the pictures of mars '

    if rover == None or rover not in rovers:
        rover = random.choice(rovers)

    if cam == None or cam not in cameras:
        cam = ''
        msg_camera = ''
        msg_main = 'Here is a picture of mars '
    else:
        cam = cam
        msg_camera = f"with the '{cam}' camera"

    f = mars_images(rover, sol, cam)
    message = f[0]
    max_sols = f[1]

    if str(sol).isdigit() == False:
        msg_sol = f'at {max_sols} Solar Days '
    elif sol == None or int(sol) > max_sols or int(sol) < 0 or sol.isdigit() == False:
        msg_sol = f'at {max_sols} Solar Days '
    else:
        msg_sol = f'at {sol} Solar Days '

    msg_rover = f'taken by the {rover} rover '
    exl = msg_main + msg_rover + msg_sol + msg_camera
    if f[0][0] == "Cam not available" or f[0][0] == 'No Cam available':
        await ctx.channel.send('Error' + "\n\n" + f[0][0])
    else:
        await ctx.channel.send(exl)
        for i in message:
            await ctx.channel.send(i)

token = os.environ['TOKEN']
bot.run(token)
