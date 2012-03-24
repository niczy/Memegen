'''
Created on Mar 24, 2012

@author: charliezhang
'''

import urllib
from google.appengine.api import images
from google.appengine.ext import webapp
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class UploadPageHandler(webapp.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/i/upload')
        self.response.out.write('<html><body>')
        self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
        self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit"
            name="submit" value="Submit"> </form></body></html>""")
        
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        blob_info = upload_files[0]
        self.redirect('/i/serve/%s' % blob_info.key())

class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)

class ServeHandler(webapp.RequestHandler):
    def get(self, blob_key):
        if blob_key:
            blob_key = str(urllib.unquote(blob_key))
            blob_info = blobstore.get(blob_key)
            
            if blob_info:
                img = images.Image(blob_key=blob_key)
                img.resize(width=80, height=100)
                img.im_feeling_lucky()
                thumbnail = img.execute_transforms(output_encoding=images.JPEG)

                self.response.headers['Content-Type'] = 'image/jpeg'
                self.response.out.write(thumbnail)
                return
        self.error(404)