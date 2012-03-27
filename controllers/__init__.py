from models import user
import webapp2
import logging
import jinja2
import os
import json

jinja_enviroment = jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates/")
        )

def response_json(handler, obj, type='application/json'):
    handler.response.headers['Content-Type'] = type
    handler.response.out.write(json.dumps(obj))
    
def render_page(handler, template_name, **kargs):
    template = jinja_enviroment.get_template(template_name + ".html")
    handler.response.out.write(template.render(kargs))
    
def require_login(url):
    def login_check(fn):
        def Get(self, *args):
            self.username = self.request.cookies.get('username')
            if self.username:
                key = self.request.cookies.get('key')
                expected_key = user.get_user_cookie_key(self.username)
                if key != expected_key:
                    self.username = None
                    
            if self.username == None and url != None:
                self.redirect(url)
                return
            else:
                fn(self, *args)
        return Get
    return login_check