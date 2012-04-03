'''
Created on Apr 1, 2012

@author: charliezhang
'''

from google.appengine.ext import db
from models import meme
import logging

def gen_entry_key(uid, mid):
    return str(uid) + '^' + str(mid)

#Record a user's "Like" action.
#Return 'success' or 'duplicate'
def like_record(uid, mid):
    k = gen_entry_key(uid, mid)
    entries = db.Query(LikeEntry).filter("str_key =", k).fetch(2)
    if len(entries) > 0: return 'duplicate'
    msg = meme.add_like_count(mid, 1)
    if msg: return msg
    entry = LikeEntry(str_key = k, uid = uid, mid = mid)
    entry.put()
    logging.info('User #%s liked Meme #%s' % (uid, mid))
    return 'success'
    
class LikeEntry(db.Model):
    str_key = db.StringProperty(indexed=True)
    uid = db.IntegerProperty(indexed=True)
    mid = db.IntegerProperty(indexed=True)