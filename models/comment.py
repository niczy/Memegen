'''
Created on Mar 28, 2012

@author: charliezhang
'''

from models import MAX_LIST_SIZE
from google.appengine.ext import db
import datetime
import json

def get_comment(mid, max_fetch=MAX_LIST_SIZE, offset=0):
    comments = db.Query(Comment).filter("mid = ", mid).order("-date").fetch(max_fetch, offset)
    return comments

def post_comment(uid, mid, content):
    comment = Comment(uid = uid,
                      mid = mid,
                      content = content,
                      date = datetime.datetime.now())
    comment.put()

class Comment(db.Model):
    '''
    classdocs
    '''
    uid = db.IntegerProperty(indexed=True)
    mid = db.IntegerProperty(indexed=True)
    date = db.DateTimeProperty(indexed=True)
    content = db.StringProperty()
    
    def to_json_str(self):
        return json.dumps(self.to_obj())
    
    def to_obj(self):
        return {
          "uid": self.uid,
          "mid": self.mid,
          "content": self.content,
          "date": str(self.date)
        }