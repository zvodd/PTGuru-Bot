import unittest
from PTGuruBot.ptg_feedhelper import FeedTacker
import requests
import os
import sys
import subprocess
import psutil
import random

TEST_SERVER_LOCATION = os.path.dirname(os.path.abspath(__file__))
TEST_SERVER_FILENAME = "fakefeed_server.py"
TEST_SERVER_HOSTNAME = "localhost"
TEST_SERVER_PORT = "5080"
ROOT_URL = "http://{}:{}/".format(TEST_SERVER_HOSTNAME, TEST_SERVER_PORT)
SET_URL = ROOT_URL+"set/"
FEED_URL = ROOT_URL+"feed/x"

class TestFeedTracker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        exe = sys.executable
        serverpath = os.path.join(TEST_SERVER_LOCATION, TEST_SERVER_FILENAME)
        print("TestFeedTracker: starting test server...")
        args = [exe, serverpath, '0', '0', 'server',
                 TEST_SERVER_HOSTNAME, TEST_SERVER_PORT]
        cls.flask_server = subprocess.Popen(args)
        print("TestFeedTracker: testing...")


    @classmethod
    def tearDownClass(cls):
        proc_pid = cls.flask_server.pid
        process = psutil.Process(proc_pid)
        for proc in process.children(recursive=True):
            proc.kill()
        process.kill()
        print("TestFeedTracker: done")

    def _test_updates(self):
        feed = FeedTacker(FEED_URL)

        requests.get(SET_URL+"0/5/x")
        ents = feed.parse()
        titles = [e.title for e in ents]
        self.assertEqual(titles, ['0', '1', '2', '3', '4'])

        requests.get(SET_URL+"0/10/x")
        ents = feed.parse()
        titles = [e.title for e in ents]
        self.assertEqual(titles, ['5', '6', '7', '8', '9'])

        requests.get(SET_URL+"5/15/x")
        ents = feed.parse()
        titles = [e.title for e in ents]
        self.assertEqual(titles, ['10', '11', '12', '13', '14'])


    def test_updates2(self):
        requests.get(SET_URL+"0/5/x")

        feed = FeedTacker(FEED_URL)
        ents = feed.parse()
        titles = [e.title for e in ents]
        print (titles)
        self.assertEqual(titles, ['0', '1', '2', '3', '4'])

        x = 5
        for _ in range(0,4):
            y = random.randrange(x+1, x+11)
            requests.get(SET_URL+"{}/{}/x".format(x,y))
            ents = feed.parse()
            titles = [e.title for e in ents]
            print (titles)
            self.assertEqual(titles, [str(i) for i in range(x,y)])
            x += y - x



if __name__ == '__main__':
    unittest.main()
