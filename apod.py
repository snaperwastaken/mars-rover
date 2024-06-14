import requests
import json
import discord

class a():
    url = 'https://api.nasa.gov/planetary/apod?api_key=api key here'

    response = requests.get(url)
    apod = json.loads(response.text)

    title = apod['title']
    date = apod['date']
    explanation = apod['explanation']
    url = apod['url']
    media_type = apod['media_type']
    service_version = apod['service_version']

