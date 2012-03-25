'''
Created on Mar 24, 2012

@author: charliezhang
'''

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import images
from google.appengine.api import files, urlfetch
from google.appengine.ext import blobstore

import datetime

MAX_LIST_SIZE = 1000
FETCH_TIMEOUT = 1000

#Write image file to blobstore, return blob_key
def write_blobstore(img, content_type, source):
    file_name = files.blobstore.create(content_type, source)
    with files.open(file_name, 'a') as f:
        f.write(img)
    files.finalize(file_name)
    blob_key = files.blobstore.get_blob_key(file_name)
    return blob_key
    
# Fetch the image from the given url and store in blobstore,
# Return blob_key if success, empty string otherwise
def fetch_image_to_blobstore(url):
    try:
        fetch_response = urlfetch.fetch(url)
        file_data = fetch_response.content
        content_type = fetch_response.headers.get('content-type', None)
        return write_blobstore(file_data, content_type, 'url_fetch')
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
    
def generate_meme_image(blob_key, top_caption, bottom_caption, style):
    blob_info = blobstore.get(blob_key) # this is the original image
    if blob_info:
        img = images.Image(blob_key=blob_key)
        img.rotate(90)
        img.im_feeling_lucky()
        generated_image = img.execute_transforms(output_encoding=images.JPEG) #TODO(do complex transforms here)
        #url = blobstore.create_upload_url('/i/uploadbyserver')#TODO
        return write_blobstore(generated_image, 'image/jpeg', 'generate_by_server')
    return ''
    
# Build a Meme and put in datastore, return numeric ID if success, -1 if failed
def make_meme(blob_key, top_caption, bottom_caption, style):
    new_blob_key = generate_meme_image(blob_key, top_caption, bottom_caption, style)
    if not new_blob_key:
        return -1
    meme = Meme(image = str(new_blob_key),
                original_image = blob_key,
                like = 0,
                dislike = 0,
                date = datetime.datetime.now(),
                captions = [top_caption, bottom_caption])
    meme.put()
    return meme.key().id()
    
def get_images():
    images = db.Query(Image).order("-like").fetch(MAX_LIST_SIZE)
    return images
    
class Meme(db.Model):
    image = db.StringProperty() # image blob key
    original_image = db.StringProperty(indexed=True) # image without captions
    # The Original size of image. Browser client can request thumbnail with any size smaller than this and layout images dynamically.
    original_width = db.IntegerProperty()
    original_height = db.IntegerProperty()
    uid = db.IntegerProperty(indexed=True) # User's id. automatically generated id.
    date = db.DateTimeProperty(indexed=True) # Publish date
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




import httplib, mimetypes, mimetools, urllib2, cookielib, urllib2
#post img to a blobstore url, return the blob_key, empty if failed
def DEPRECATED_post_image_to_blobstore(img, url, source, content_type='image/jpeg'):
    try:
        #fetch_response = urlfetch.fetch(url)
        file_data = img
        content_type = 'image/jpeg'
        file_name = files.blobstore.create(mime_type=content_type)
        with files.open(file_name, 'a') as f:
            f.write(file_data)
        files.finalize(file_name)
        blob_key = files.blobstore.get_blob_key(file_name)
        return blob_key
    except urllib2.URLError, e:
        print e
        return ''
    
    def post_multipart(host, selector, fields, files):
        """
        Post fields and files to an http host as multipart/form-data.
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return the server's response page.
        """
        content_type, body = encode_multipart_formdata(fields, files)
        
        h = httplib.HTTPConnection('127.0.0.1')
        
        h.putheader('content-type', content_type)
        h.putheader('content-length', str(len(body)))
        h.putheader("Accept", "*/*"); 
        h.putheader("Connection", "Keep-Alive"); 
        h.endheaders()
        h.request('POST', url)
        #h.send(body)
        #return body
        r1 = h.getresponse()
        return r1.status
        headers = h.getreply()
        return headers #TODOerrcodeheaders
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
        return content_type #TODO
        #return 'image/jpeg'
        #return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    
    return post_multipart(url, '', [('submit', 'Submit')], [('file', source, img)])