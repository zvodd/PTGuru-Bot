import os
import configparser
import logging



#Logging Capability
logging.basicConfig(filename="gurubot-log.txt", level=logging.INFO, format="%(asctime)s - %(levelname)s [+]%(message)s")


config = configparser.RawConfigParser()
config.read("settings.cfg")

# New Post Limit, per feed.
MAX_NEW_POSTS = int(config.get("limits", "max_new_posts"))

# Timers
FEED_UPDATE_DELTA = int(config.get("timers", "interval"))

# Bot token
TOKEN = config.get("DEFAULT", "token")


