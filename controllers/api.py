'''
Created on Mar 24, 2012

@author: charliezhang
'''

import webapp2
from models import meme

def response_json(handler, json):
    handler.response.headers['Content-Type'] = 'application/json'
    handler.response.out.write(json)
        
class ApiMeme(webapp2.RequestHandler):
    def get(self, mid):
        self.response.out.write("Get Meme: %s" % mid)

class ApiMemeList(webapp2.RequestHandler):
    def get(self, type):
        if not type:
            self.error(404)
            return
        if type == 'popular':
            response_json(self, '["1", "2", "3"]')
        if type == 'latest':
            response_json(self, '["3", "2", "1"]')   
        if type == 'byuser':
            uid = self.request.get("uid")
            