import webapp2
import logging
import jinja2
import os

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


