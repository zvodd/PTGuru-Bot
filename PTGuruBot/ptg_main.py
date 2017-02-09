import discord
import logging
import asyncio

log = logging.getLogger()
# Client
client = discord.Client()

#import order is important here
import ptg_feeds








# Bot Responses
AUTHOR = "**Learning Penetration Testing\n\nThe Penetration Testing Community**"
HELP = "**!!author\n!!joinredteam5**"


@client.event
# After Client Connection
async def on_ready():
    log.info("Initialzation Complete..")
    log.info("Guru! Guru!.")
    await ptg_feeds.updatefeeds()


@client.event
# Bot Capabilities Upon Sent Message
async def on_message(message):
    log.info("{} Sent:".format(message.author))
    log.info("Message: {}".format(message.content))

    if message.content.startswith("!!author"):
        await client.send_message(message.channel, AUTHOR)

    if message.content.startswith("!!help"):
        await client.send_message(message.channel, HELP)

    if message.content.startswith("!!joinredteam5"):
        redteam5_about_page = open("assets/RedTeam5.txt", "r").read()
        with open("assets/malware-image.jpg", "rb") as community_logo:
            await client.send_message(message.channel, redteam5_about_page)
            await client.send_file(message.channel, community_logo)


