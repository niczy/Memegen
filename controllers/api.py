'''
Created on Mar 24, 2012

@author: charliezhang
'''


import webapp2
from controllers import response_json
from controllers import require_login
from models import comment
from models import meme


# Map a list of Model to a list of objs
def obj_list(model_list):
    return map(lambda x: x.to_obj(), model_list)
    
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

class ApiComments(webapp2.RequestHandler):
    def get(self, mid):
        if not mid: return
        mid = int(mid)
        max_fetch = self.request.get("max_fetch")
        offset = self.request.get("offset")
        if offset and max_fetch: comments = obj_list(comment.get_comment(mid, max_fetch, offset))
        elif max_fetch: comments = obj_list(comment.get_comment(mid, max_fetch))
        else: comments = obj_list(comment.get_comment(mid))
        response_json(self, comments)
    
    @require_login('/')
    def post(self, mid):
        if not mid: return
        mid = int(mid)
        content = self.request.get("content")
        comment.post_comment(self.uid, mid, content)