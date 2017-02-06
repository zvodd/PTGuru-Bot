
import discord
import logging
import asyncio
import aiohttp
import feedparser
import time

logging.basicConfig(filename="log.txt", level=logging.INFO, format="%(asctime)s - %(levelname)s [+]%(message)s")
log = logging.getLogger()

client = discord.Client()
author = "```Learning Penetration Testing\n\nThe Penetration Testing Community```"
Help = "```!!author\n!!joinredteam5```"
cve_feed = "http://bit.ly/2k97VtF"
news_channel = "275289702985367564"
vulnerability_channel = "277950292807516161"
newslist = open("newslist.txt", "r").read()
current_date = time.strftime("%m-%d-%Y")

@client.event
async def on_ready():
    log.info("Initialzation Complete..")
    log.info("Guru Bot Ready.")

async def post_feeds():
    await client.send_message(client.get_channel(news_channel), "```Test News Feed```")

async def post_exploits():
    async with aiohttp.get(cve_feed) as link:
        await client.send_message(client.get_channel(vulnerability_channel), "```Vulnerability of The Day```")

@client.event
async def on_message(message):
    log.info("{} Sent:".format(message.author))
    log.info("Message: {}".format(message.content))

    if message.content.startswith("!!author"):
        await client.send_message(message.channel, author)

    if message.content.startswith("!!help"):
        await client.send_message(message.channel, Help)

    if message.content.startswith("!!joinredteam5"):
        redteam5_about_page = open("RedTeam5.txt", "r").read()
        with open("malware-image.jpg", "rb") as community_logo:
            await client.send_message(message.channel, redteam5_about_page)
            await client.send_file(message.channel, community_logo)

client.run("Mjc3MjMwODcyNDMwNzcyMjI2.C3awAA.66dkxAXIHrdg4wI7sp8LTtzXlCw")
