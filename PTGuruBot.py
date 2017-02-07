
import discord
import logging
import asyncio
import feedparser
import time
import re

#Logging Capability
logging.basicConfig(filename="gurubot-log.txt", level=logging.INFO, format="%(asctime)s - %(levelname)s [+]%(message)s")
log = logging.getLogger()

# Client
client = discord.Client()

# Bot Responses
author = "**Learning Penetration Testing\n\nThe Penetration Testing Community**"
Help = "**!!author\n!!joinredteam5**"

# Feed Sources
newslist = open("newslist.txt", "r")
cve_feed = "http://bit.ly/2k97VtF"
ctf_upcoming = "https://ctftime.org/event/list/upcoming/rss/"

# Channel IDs
news_channel = "278244337752735744"
vulnerability_channel = "278244156759867392"
ctf_channel = "274925767924776960"

# Single Feeders
cve_feeder = feedparser.parse(cve_feed)
ctf_feeder = feedparser.parse(ctf_upcoming)



@client.event
# After Client Connection
async def on_ready():
    log.info("Initialzation Complete..")
    log.info("Guru! Guru!.")
    await post_upcoming_ctfs()
    await post_vulnerabilities()
    await post_feeds()

# InfoSec Feeds
async def post_feeds():
    # Multi Feeder
    for feed_source in newslist:
        news_feeder = feedparser.parse(feed_source)
        await client.send_message(client.get_channel(news_channel), "**{}**\n\n{}".format(news_feeder.entries[0].title, news_feeder.entries[0].link))
        await asyncio.sleep(3)

# CVE Vulnerability Feed
async def post_vulnerabilities():
    await client.send_message(client.get_channel(vulnerability_channel), "**Newly Posted Vulnerability!!\n{}\n\n{}\n{}**".format(cve_feeder.entries[0].title, cve_feeder.entries[0].summary, cve_feeder.entries[0].link))

# Upcoming CTFs Feed "CTFtime.org"
async def post_upcoming_ctfs():
    await client.send_message(client.get_channel(ctf_channel), "**Newly Posted CTF!!\n\n{}\n\n{}**".format(ctf_feeder.entries[0].title, re.sub("<.*?>", "", ctf_feeder.entries[0].summary)))

@client.event
# Bot Capabilities Upon Sent Message
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
