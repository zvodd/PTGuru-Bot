import os
import configparser
import logging



#Logging Capability
logging.basicConfig(filename="gurubot-log.txt", level=logging.INFO, format="%(asctime)s - %(levelname)s [+]%(message)s")


config = configparser.RawConfigParser()
config.read("settings.cfg")

# News Feeds
CTF_FEED_URL = config.get('feeds', 'ctf_feed_url')
CVE_FEED_URL = config.get('feeds', 'cve_feed_url')
## hard coded
with open("assets/newslist.txt", "r") as fh:
    NEWS_FEED_URLS = [line for line in fh]

# Channel IDs
NEWS_CHANNEL = config.get('channels', 'news_channel')
CVE_CHANNEL = config.get('channels', 'vulnerability_channel')
CTF_CHANNEL = config.get('channels', 'ctf_channel')

# New Post Limit, per feed.
MAX_NEW_POSTS = int(config.get("limits", "max_new_posts"))

# Timers
FEED_UPDATE_DELTA = int(config.get("timers", "interval"))

# Bot token
TOKEN = config.get("DEFAULT", "token")


