import webapp2

from google.appengine.ext import blobstore
from controllers import render_page
from controllers import redirect
from models import meme
import logging


class MakeHandler(webapp2.RequestHandler):

    def get(self, source='template'):
        if source == 'template':
            render_page(self,'make_from_template', source=source)
        elif source == 'url':
            render_page(self, 'make_from_url', source=source)
        elif source == 'img':
            post_url = blobstore.create_upload_url('/i/upload')
            logging.info("got post url is " + post_url)
            render_page(self, 'make_from_img', source=source, post_url=post_url)



class PageHandler(webapp2.RequestHandler):
    def get(self, page_name='popular'):
        lower_name = page_name.lower()
        render_page(self,lower_name, page_name=lower_name)

class MakeMemeHandler(webapp2.RequestHandler):
    def post(self):
        blob_key = self.request.get('blob_key')
        top_caption = self.request.get('top_caption')
        bottom_caption = self.request.get('bottom_caption')
        style = self.request.get('style')
        fetch_url = self.request.get('fetch_url')
        if fetch_url:
            blob_key = meme.fetch_image_to_blobstore(fetch_url)
            meme.save_template(blob_key)
            self.response.out.write(blob_key) #TODO
        else:
            self.response.out.write(meme.make_meme(blob_key, top_caption, bottom_caption, style)) #TODO
            
    def get(self, template_id = None):
        url = self.request.get('url')
        if url:
            #fetch the url then redirect to /makememe/tempalteid
            logging.info("got url is " + url)
            blob_key = meme.fetch_image_to_blobstore(url)
            meme.save_template(blob_key)
            redirect(self, '/makememe/%s' % blob_key)
            return
        render_page(self, 'make_meme', template_id=template_id)

class MemeHandler(webapp2.RequestHandler):
    def get(self, meme_id):
        if meme_id:
            render_page(self, "single_meme", meme_id=meme_id)
            
#DEBUG MODE ONLY
class Debug(PageHandler):
    def get(self):
        render_page(self, "debug")

#DEBUG MODE ONLY
class RunTest(PageHandler):
    def get(self):
        import unittest
        unittest.main()
        

