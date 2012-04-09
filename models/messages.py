'''
Created on Apr 4, 2012

@author: charliezhang
'''

import json
from google.appengine.ext import db
from models import MAX_LIST_SIZE

#Types:
COMMENT = "COMMENT"
SYSTEM = "SYSTEM"
CHAT = "CHAT"

#Status:
NEW = "NEW"
READ = "READ"

#Add a message when someone commented on uid's post
def add_comment_message(uid, mid):
    messages = db.Query(Message).filter("uid =", uid).filter("mid = ", mid).filter("type = ", COMMENT).filter("status = ", NEW).fetch(2)
    if len(messages) > 0: m = messages[0]
    else: m = Message(uid = uid, mid = mid, type = COMMENT, status = NEW, count = 0)
    m.count = m.count + 1
    m.put()

def get_user_messages(uid, only_new = True):
    q = db.Query(Message).filter("uid =", uid)
    if only_new: q = q.filter("status =", NEW)
    messages = q.fetch(MAX_LIST_SIZE)
    return messages

#Set Users' messages as 'Read'
def set_user_message_read(uid):
    messages = db.Query(Message).filter("uid =", uid).fetch(MAX_LIST_SIZE)
    for m in messages: 
        m.status = READ
        m.put()
    
#TODO: set uid as parent
class Message(db.Model):
    '''
    Messages that a user sees when logs in.
    For example, when user 31 logs in, he probably sees:
      "22 Users commented on your Meme XX."  --> Messages(uid=31, type=COMMENT, mid=XX, content="", status=NEW, count=22)
    '''
    uid = db.IntegerProperty(indexed=True)
    type = db.StringProperty() # Types are: 
    mid = db.IntegerProperty(required=False)
    content = db.StringProperty(required=False)
    status = db.StringProperty()
    count = db.IntegerProperty()
    
    def to_json_str(self):
        return json.dumps(self.to_obj())
    
    def to_obj(self):
        return {
          "uid": self.uid,
          "mid": self.mid,
          "type": self.type,
          "content": self.content,
          "status": self.status,
          "count": self.count
        }
    