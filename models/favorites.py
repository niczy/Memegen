'''
Created on Apr 1, 2012

@author: charliezhang
'''
from google.appengine.ext import db
import json
import logging

def get_favorites(uid):
    return db.Query(Favorites).filter("uid =", uid)
    
def add_user_favorite(uid, mid, category='default'):
    f = get_favorite_category(uid, category)
    if not f:
        f = create_favorite_category(uid, category)
    logging.info('User #%s added Meme #%s to category "%s"' % (uid, mid, category))
    f.memes.append(str(mid))
    f.put()

def create_favorite_category(uid, category):
    if not get_favorite_category(uid, category):
        f = Favorites(uid = uid, category_name = category)
        f.put()
        logging.info('User #%s created category "%s"' % (uid, category))
        return f
    return None
  
def get_favorite_category(uid, category='default'):
    favorite = db.Query(Favorites).filter("uid =", uid).filter("category_name", category)
    for f in favorite: return f
    return None
    
class Favorites(db.Model):
    uid = db.IntegerProperty(indexed=True)
    category_name = db.StringProperty(indexed=True)
    memes = db.StringListProperty(default=["1", "2"])
    
    def to_json_str(self):
        return json.dumps(self.to_obj())
    
    def to_obj(self):
        return {
          "uid": self.uid,
          "category": self.category_name,
          "memes": self.memes,
        }