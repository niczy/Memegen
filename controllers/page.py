import webapp2
import logging
import jinja2
import os

from models import meme

jinja_enviroment = jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates/")
        )

def render_page(handler, template_name, values = {}):
    template = jinja_enviroment.get_template(template_name + ".html")
    handler.response.out.write(template.render(values))

class PageHandler(webapp2.RequestHandler):
    def get(self, page_name='index'):
        render_page(self,page_name, {'page_name': page_name.lower()})

class MakeMeme(PageHandler):
    def post(self):
        blob_key = self.request.get('blob_key')
        top_caption = self.request.get('top_caption')
        bottom_caption = self.request.get('bottom_caption')
        style = self.request.get('style')
        fetch_url = self.request.get('fetch_url')
        if fetch_url:
            self.response.out.write(meme.fetch_image_to_blobstore(fetch_url))
        else:
            meme.make_meme(blob_key, top_caption, bottom_caption, style)