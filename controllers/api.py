'''
Created on Mar 24, 2012

@author: charliezhang
'''

import json
import webapp2
from models import meme

# Map a list of Model to a list of objs
def obj_list(model_list):
    return map(lambda x: x.to_obj(), model_list)
    
def response_json(handler, obj):
    handler.response.headers['Content-Type'] = 'application/json'
    handler.response.out.write(json.dumps(obj))
        
class ApiMeme(webapp2.RequestHandler):
    def get(self, mid):
        self.response.out.write("Get Meme: %s" % mid)

class ApiMemeList(webapp2.RequestHandler):
    def get(self, type):
        if not type:
            self.error(404)
            return
        if type == 'popular':
            memes = obj_list(meme.get_popular_memes())
            response_json(self, memes)
        if type == 'latest':
            memes = obj_list(meme.get_latest_memes())
            response_json(self, memes)   
        if type == 'byuser':
            uid = self.request.get("uid")

class ApiTemplateList(webapp2.RequestHandler):
    def get(self, type):
        if not type: type = 'popular'
        if type == 'popular':
            templates = obj_list(meme.get_popular_templates())
            response_json(self, templates)
        return
