import webapp2
import logging
import jinja2
import os

from models import meme

jinja_enviroment = jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates/")
        )

def render_page(handler, template_name, **kargs):
    template = jinja_enviroment.get_template(template_name + ".html")
    handler.response.out.write(template.render(kargs))

class PageHandler(webapp2.RequestHandler):
    def get(self, page_name='popular'):
        lower_name = page_name.lower()
        render_page(self,lower_name, page_name=lower_name)

class MemeHandler(webapp2.RequestHandler):
    def get(self, meme_id):
        if meme_id:
            render_page(self, "single_meme", meme_id=meme_id)

class MakeMeme(PageHandler):
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
