import feedparser
import hashlib


import ipdb
from pprint import pprint, pformat

class FeedTacker(object):
    """
    Takes a rssfeed url, retrives entries on each call of parse,
    only returning new entries on each subsiquent call.

    Only remebers entries from last parse call to determin "newness".

    """
    def __init__(self, feedurl):
        self.feedurl = feedurl
        self.seen_ids = None

    def parse(self, limit=None):
        # load feed 
        entries = feedparser.parse(self.feedurl).entries
        entry_ids = [_id_ent(ent) for ent in entries]
        #if seen_ids is empty (first run)
        if not self.seen_ids:
            #add all entries to seen_ids
            self.seen_ids = entry_ids
            new_entries = entries
        else:
            #filter already seen items
            new_entries = [e for e in entries if _id_ent(e) not in self.seen_ids]

            # add new_entries to seen_ids
            self.seen_ids += map(_id_ent, new_entries)

            # remake the seen_ids list without lost/dead entries
            new_seen = []
            for eid in self.seen_ids:
                if eid in entry_ids:
                    new_seen.append(eid)
            self.seen_ids = new_seen

            # delta = len(self.seen_ids) - len(new_entries)
            # self.seen_ids = self.seen_ids[delta:]

        if limit:
            res = new_entries[:min(len(new_entries), limit)]
        else:
            res = new_entries
        return res

    def __repr__(self):
        return '%s:%s' % (self.__class__, self.feedurl)

def _id_ent(ent):
    "Hash feed entry"
    return hashlib.md5((ent.link+ent.title).encode('utf-8')).digest()
    # return ent.title
