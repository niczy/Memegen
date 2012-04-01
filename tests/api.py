'''
Created on Mar 31, 2012

@author: charliezhang
'''

import unittest
from google.appengine.ext import db
from google.appengine.ext import testbed


class ApiCommentsTest(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()

    def tearDown(self):
        self.testbed.deactivate()
    
    def test_post_comment(self):
        pass