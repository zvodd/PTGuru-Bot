
import discord
import logging
import asyncio
import feedparser
import time
import re

logging.basicConfig(filename="gurubot-log.txt", level=logging.INFO, format="%(asctime)s - %(levelname)s [+]%(message)s")
log = logging.getLogger()

client = discord.Client()

author = "**Learning Penetration Testing\n\nThe Penetration Testing Community**"
Help = "**!!author\n!!joinredteam5**"

newslist = open("newslist.txt", "r")
cve_feed = "http://bit.ly/2k97VtF"
ctf_upcoming = "https://ctftime.org/event/list/upcoming/rss/"

news_channel = "278244337752735744"
vulnerability_channel = "278244156759867392"
ctf_channel = "274925767924776960"

cve_feeder = feedparser.parse(cve_feed)
ctf_feeder = feedparser.parse(ctf_upcoming)

current_date = time.strftime("%m-%d-%Y")


@client.event
async def on_ready():
    log.info("Initialzation Complete..")
    log.info("Guru! Guru!.")
    await post_upcoming_ctfs()
    await post_vulnerabilities()

async def post_feeds():
    await client.send_message(client.get_channel(news_channel), "**Test News Feed**")

async def post_vulnerabilities():
    await client.send_message(client.get_channel(vulnerability_channel), "**New Posted Vulnerability!!{}\n{}\n{}**".format(cve_feeder.entries[0].title, cve_feeder.entries[0].summary, cve_feeder.entries[0].link))

async def post_upcoming_ctfs():
    await client.send_message(client.get_channel(ctf_channel), "**Newly Posted CTF!!\n\n{}\n\n{}**".format(ctf_feeder.entries[0].title, re.sub("<.*?>", "", ctf_feeder.entries[0].summary)))


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
