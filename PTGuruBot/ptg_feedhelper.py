import feedparser
import hashlib


import ipdb
from pprint import pprint, pformat

class FeedTacker(object):
    """
    Takes a rssfeed url, retrive entries with tracked_parse().
    only returning new entries on each subsiquent call.
    Only remebers entries from last parse call to determin "newness".
    """
    def __init__(self, feedurl):
        self.feedurl = feedurl
        self.entries = []
        self.entry_ids = []
        self.seen_ids = []
        self.new_entries = []


    def parse(self):
        self.entries = feedparser.parse(self.feedurl).entries
        self.entry_ids = [self.eid(ent) for ent in self.entries]
        return self.entries


    def tracked_parse(self, limit=None, dont_clean=False):
        self.parse()
        self.filter_updated(dont_clean)

        if limit:
            return self.new_entries[:min(len(self.new_entries), limit)]
        else:
            return self.new_entries


    def filter_updated(self, dont_clean=False):
        #if seen_ids is empty (first run)
        if len(self.seen_ids) < 1:
            #add all entries to seen_ids
            self.seen_ids = self.entry_ids
            filtered_ents = self.entries
        else:
            #filter already seen items
            filtered_ents = [e for e in self.entries if self.eid(e) not in self.seen_ids]

            # add filtered_ents to seen_ids
            self.seen_ids += map(self.eid, filtered_ents)

            if dont_clean:
                pass
            else:
                self.clean()

        self.new_entries = filtered_ents


    def clean(self):
        # remake the seen_ids list without lost/dead entries
        new_seen = []
        for eid in self.seen_ids:
            if eid in self.entry_ids:
                new_seen.append(eid)
        self.seen_ids = new_seen


    def eid(self, ent):
        "Hash feed entry"
        return hashlib.md5((ent.link+ent.title).encode('utf-8')).digest()


    def __repr__(self):
        return '{}:{}'.format(self.__class__, self.feedurl)


    # return ent.title