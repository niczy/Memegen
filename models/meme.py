'''
Created on Mar 24, 2012

@author: charliezhang
'''

from google.appengine.ext import db
from google.appengine.ext import webapp

class Meme(db.Model):
    image = db.StringProperty() # image blob key
    original_image = db.StringProperty(indexed=True) # image without captions
    # The Original size of image. Browser client can request thumbnail with any size smaller than this and layout images dynamically.
    original_width = db.IntegerProperty(required=True)
    original_height = db.IntegerProperty(required=True)
    uid = db.IntegerProperty(indexed=True) # User's id. automatically generated id.
    date = db.DateProperty(indexed=True) # Publish date
    like = db.IntegerProperty(indexed=True)
    dislike = db.IntegerProperty(indexed=True)
    captions = db.StringListProperty() # Store the texts for indexing