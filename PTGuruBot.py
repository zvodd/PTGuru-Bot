import discord
import asyncio
import aiohttp
import feedparser
import logging


client = discord.Client()
log = logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
author = "```Learning Penetration Testing\nThe Pen Testing Community```"
Help = "```!!author\n!!help\n!!joinredteam5```"
cve_feed = "http://bit.ly/2k97VtF"
news_channel = "275289702985367564"
newslist = open("newslist.txt", "r").read()
current_date = time.strftime("%m-%d-%Y")

@client.event
async def on_ready():
    log.info("Guru Bot Initiliazing")
    log.info(client.user.name)
    log.info(client.user.id)

async def post_feeds():
    await client.send_message(client.get_channel(news_channel), "Test News Feed")

async def post_exploits():
    async with aiohttp.get(cve_feed) as link:
        await client.send_message(client.get_channel(news_channel), "Exploit of The Day")

@client.event
async def on_message(message):
    joinredteam5 = "@{} You Are Now A Member Of Red Team 5!!!".format(message.author)

    if message.content == "!!author":
        await client.send_message(message.channel, author)

    if message.content == "!!help":
        await client.send_message(message.channel, Help)

    if message.content == "!!joinredteam5":
        with open("malware-image.jpg", "rb") as logo:
            await client.send_file(message.channel, logo)
            await client.send_message(message.channel, joinredteam5)


client.run("Mjc3MjMwODcyNDMwNzcyMjI2.C3awAA.66dkxAXIHrdg4wI7sp8LTtzXlCw")
