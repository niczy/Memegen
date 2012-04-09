from models import user
import webapp2
import logging
import jinja2
import os
import json
import config

jinja_enviroment = jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates/")
        )

def response_json(handler, obj, type='application/json'):
    handler.response.headers['Content-Type'] = type
    handler.response.out.write(json.dumps(obj))
    
def render_page(handler, template_name, **kargs):
    template = jinja_enviroment.get_template(template_name + ".html")
    handler.response.out.write(template.render(kargs))

def redirect(handler, url, *args):
    handler.redirect(str(config.HOST + url), *args)
    
def require_login(url):
    def login_check(fn):
        def Get(self, *args):
            self.uid = int(self.request.cookies.get('uid'))
            if self.uid:
                key = self.request.cookies.get('key')
                expected_key = user.get_user_cookie_key(self.uid)
                if key != expected_key:
                    self.uid = None
                    
            if self.uid == None and url != None:
                self.redirect(url)
                return
            else:
                fn(self, *args)
        return Get
    return login_check
