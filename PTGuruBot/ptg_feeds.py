import logging
import asyncio
import re
import feedparser
from ptg_feedhelper import FeedTacker
import ptg_configure as cfg
from ptg_main import client

log = logging.getLogger()


def NEWS(item):
    args = (item.title, item.link)
    fstr = "**{}**\n\n{}"
    chan = cfg.CTF_CHANNEL
    return (fstr.format(*args), chan)

def CVE(item):
    args = (item.title, item.summary, item.link)
    fstr = "**Newly Posted Vulnerability!!\n{}\n\n{}\n{}**"
    chan = cfg.CVE_CHANNEL
    return (fstr.format(*args), chan)

def CTF(item):
    args = (item.title, re.sub("<[^>]*>", "", item.summary))
    fstr = "**Newly Posted CTF!!\n\n{}\n\n{}**"
    chan = cfg.CTF_CHANNEL
    return (fstr.format(*args), chan)


# Feeder loop
async def updatefeeds():
    #initialize tracking
    cve_feeder = FeedTacker(cfg.CVE_FEED_URL)
    ctf_feeder = FeedTacker(cfg.CTF_FEED_URL)
    news_feeders = [FeedTacker(feed_source) for feed_source in cfg.NEWS_FEED_URLS]
        
    while True:
        for news_feeder in news_feeders:
            await post_feeds(news_feeder, post_format=NEWS, limit=cfg.MAX_NEW_POSTS)
        await post_feeds(ctf_feeder, post_format=CTF, limit=cfg.MAX_NEW_POSTS)
        await post_feeds(cve_feeder, post_format=CVE, limit=cfg.MAX_NEW_POSTS)
        await asyncio.sleep(cfg.FEED_UPDATE_DELTA)


# Post a feed.
async def post_feeds(feed, post_format=NEWS, limit=300,):
    logging.info("post_feeds: {0!a}".format(feed))
    for entry in feed.parse(limit):
        msg, channel = post_format(entry)
        logging.debug(msg)    
        await client.send_message(client.get_channel(channel), msg)