import webapp2
import logging
import jinja2
import os

jinja_enviroment = jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates/")
        )

def render_page(handler, template_name, values = {}):
    template = jinja_enviroment.get_template(template_name + ".html")
    handler.response.out.write(template.render(values))

class PageHandler(webapp2.RequestHandler):
    def get(self, page_name='index'):
        render_page(self,page_name)


