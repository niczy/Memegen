'''
Created on Mar 24, 2012

@author: charliezhang
'''

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import images
from google.appengine.api import files, urlfetch
from google.appengine.ext import blobstore

import httplib, mimetypes, mimetools, urllib2, cookielib, urllib2
import datetime

MAX_LIST_SIZE = 1000
FETCH_TIMEOUT = 1000

# Fetch the image from the given url and store in blobstore,
# Return blob_key if success, empty string otherwise
def fetch_image_to_blobstore(url):
    try:
        fetch_response = urlfetch.fetch(url)
        file_data = fetch_response.content
        content_type = fetch_response.headers.get('content-type', None)
        file_name = files.blobstore.create(mime_type=content_type)
        with files.open(file_name, 'a') as f:
            f.write(file_data)
        files.finalize(file_name)
        blob_key = files.blobstore.get_blob_key(file_name)
        return blob_key
    except urllib2.URLError, e:
        print e
        return ''
    
def get_latest_memes():
    memes = db.Query(Meme).order("-date").fetch(MAX_LIST_SIZE)
    return memes

def get_popular_memes():
    memes = db.Query(Meme).order("-like").fetch(MAX_LIST_SIZE)
    return memes
    
def get_memes_by_uid(uid):
    if not uid: return []
    memes = db.Query(Meme).filter("uid =", uid).order("-date").fetch(MAX_LIST_SIZE)
    return memes


#post img to a blobstore url, return the blob_key, empty if failed
def post_image_to_blobstore(img, url):
    
    def post_multipart(host, selector, fields, files):
        """
        Post fields and files to an http host as multipart/form-data.
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return the server's response page.
        """
        print "URL:: %s" % host
        content_type, body = encode_multipart_formdata(fields, files)
        h = httplib.HTTP(host)
        h.putrequest('POST', selector)
        h.putheader('content-type', content_type)
        h.putheader('content-length', str(len(body)))
        h.endheaders()
        h.send(body)
        errcode, errmsg, headers = h.getreply()
        return h.file.read()
    
    def encode_multipart_formdata(fields, files):
        """
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return (content_type, body) ready for httplib.HTTP instance
        """
        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
        CRLF = '\r\n'
        L = []
        for (key, value) in fields:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)
        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % get_content_type(filename))
            L.append('')
            L.append(value)
            L.append('--' + BOUNDARY + '--')
            L.append('')
            body = CRLF.join(L)
            content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body
    
    def get_content_type(filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    
    return post_multipart(url, '', [], [('file', '', img)])
    
    
def generate_meme_image(blob_key, top_caption, bottom_caption, style):
    blob_info = blobstore.get(blob_key) # this is the original image
    if blob_info:
        img = images.Image(blob_key=blob_key)
        img.im_feeling_lucky()
        generated_image = img.execute_transforms(output_encoding=images.JPEG) #TODO(do complex transforms here)
        url = blobstore.create_upload_url('/i/upload')
        return post_image_to_blobstore(generated_image, url)
    return ''
    

def make_meme(blob_key, top_caption, bottom_caption, style):
    new_blob_key = generate_meme_image(blob_key, top_caption, bottom_caption, style)
    print new_blob_key
    if not new_blob_key:
        return None
    meme = Meme(image = new_blob_key,
                original_image = blob_key,
                like = 0,
                dislike = 0,
                captions = [top_caption, bottom_caption],
                date = datetime.datetime)
    meme.put()
    
def get_images():
    images = db.Query(Image).order("-like").fetch(MAX_LIST_SIZE)
    return images
    
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

class Image(db.Model):
    blob_key = db.StringProperty()
    width = db.IntegerProperty()
    height = db.IntegerProperty()
    uid = db.IntegerProperty(indexed=True) # User's id. automatically generated id.
    date = db.DateProperty(indexed=True) # Publish date
    like = db.IntegerProperty(indexed=True)
