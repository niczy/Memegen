'''
Created on Mar 24, 2012

@author: charliezhang
'''


import webapp2
from controllers import response_json
from controllers import require_login
from models import comment
from models import meme
from models import likes
from models import favorites


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
        response_json(self, comment.post_comment(self.uid, mid, content))


class ApiLike(webapp2.RequestHandler):
    @require_login('/')
    def get(self, mid):
        if not mid: return
        response_json(self, likes.like_record(self.uid, int(mid)))

class ApiAddToFavorites(webapp2.RequestHandler):
    @require_login('/')
    def get(self, mid):
        if not mid: return
        category = self.request.get('category')
        #TODO reduce these codes
        if category: res = favorites.add_user_favorite(self.uid, mid, category)
        else: res = favorites.add_user_favorite(self.uid, mid)
        response_json(self, res)

class ApiGetFavorites(webapp2.RequestHandler):
    @require_login('/')
    def get(self):
        response_json(self, obj_list(favorites.get_favorites(self.uid)))
        
    '''
MAX_LIKE_IN_CACHE = 10
like_cache = {(0, 'mid'): 0}

        #mid = int(mid)
        like_cache.keys()
        if not like_cache.has_key(mid): like_cache[mid] = 1
        else: like_cache[mid] = like_cache[mid] + 1
        if like_cache[mid] >= MAX_LIKE_IN_CACHE:
            tmp = like_cache[mid]
            like_cache[mid] = 0
            m = meme.get_meme_by_id(int(mid))
            m.like = m.like + tmp
            m.put()
        print self.uid
    '''
        