'''
Created on Apr 1, 2012

@author: charliezhang
'''

import unittest
from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.ext import blobstore
from models import meme
from controllers import api
import datetime
from tests import init_test

def get_id_list(list, field):
    return map(lambda x: x[field], api.obj_list(list))

def mock_make_meme(blob_key, top_caption, bottom_caption, style, like=0, dislike=0):
    new_blob_key = blob_key + 'MEME'
    m = meme.Meme(image = str(new_blob_key),
                template = blob_key,
                like = like,
                dislike = dislike,
                original_width = 33,
                original_height = 44,
                date = datetime.datetime.now(),
                captions = [top_caption, bottom_caption])
    m.put()
    return m.key().id()
    
class MemeTests(unittest.TestCase):
    def setUp(self):
        init_test(self)

    def tearDown(self):
        self.testbed.deactivate()
    
    def test_meme_model(self):
        m = meme.Meme(image = "MEME1",
                    template = "TEMPLATE1",
                    like = 0,
                    dislike = 0,
                    original_width = 10,
                    original_height = 20,
                    date = datetime.datetime.now(),
                    captions = ["top_caption", "bottom_caption"])
        m.put()
        memes = api.obj_list(meme.Meme.all().fetch(2))
        self.assertEqual(len(memes), 1, "Model Meme Error! results:" + str(memes))
    
    def test_make_meme(self):
        res = meme.make_meme("TEMPLATE", "hello", "btn", "BIG")
        self.assertEqual(res, -1, "Template doesn't exist, make_meme() should fail!")
        
        '''
        TODO:
        Unable to test actual make_meme() due to no stub service for files.
        Find other solution.
        '''

    def test_get_memes(self):
        m1 = mock_make_meme("M1", "hello", "world", "Courier New", 10)
        m2 = mock_make_meme("M2", "Top", "Bottom", "Courier New", 30)
        m3 = mock_make_meme("M3", "Fuck", "You", "Courier New", 5)
        memes = api.obj_list(meme.Meme.all().fetch(1000))
        self.assertEqual(len(memes), 3, "make_meme() Error!, results: " + str(memes))
        memes = get_id_list(meme.get_latest_memes(), 'mid')
        self.assertEqual(memes, [m3, m2, m1], "meme.get_latest_memes() Error!, results:" + str(memes))
        memes = get_id_list(meme.get_popular_memes(), 'mid')
        self.assertEqual(memes, [m2, m1, m3], "meme.get_popular_memes() Error!, results:" + str(memes))
