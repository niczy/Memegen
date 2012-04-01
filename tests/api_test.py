'''
Created on Mar 31, 2012

@author: charliezhang
'''

import unittest
from google.appengine.ext import db
from google.appengine.api import urlfetch
from tests import init_test
import httplib, urllib

class DatastoreApiTests(unittest.TestCase):
    def setUp(self):
        init_test(self)

    def tearDown(self):
        self.testbed.deactivate()
    
    def test_hello_world(self):
        self.assert_(0==0, "HELLO WORLD")
    
    def test_meme_list(self):
        from tests.meme_test import mock_make_meme
        m1 = mock_make_meme("M1", "hello", "world", "Courier New", 10)
        m2 = mock_make_meme("M2", "Top", "Bottom", "Courier New", 30)
        m3 = mock_make_meme("M3", "Fuck", "You", "Courier New", 5)
        '''
        conn = httplib.HTTPConnection("localhost:8080")
        conn.request("GET", "/api/memelist/latest")
        r1 = conn.getresponse()
        fetch_response = urlfetch.fetch("http://localhost:8080/api/memelist/latest")
        file_data = fetch_response.content
        self.assertEqual(1, 200, "/api/memelist/latest Broken!! response:" + file_data)
        '''
        
    def test_post_comment(self):
        pass
        #params = urllib.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})