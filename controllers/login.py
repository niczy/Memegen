'''
Created on Mar 27, 2012

@author: charliezhang
'''

import webapp2
from controllers import render_page
from models import user

class Login(webapp2.RequestHandler):
    def get(self):
        render_page(self, 'login', error=False);
        
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        error = user.login_with_username_or_email(self, username, password)
        if not error:
            self.redirect("/")
        else:
            render_page(self, 'login', error=True,
                                       error_msg=error);

class Logout(webapp2.RequestHandler):
    def get(self):
        self.response.headers.add_header('Set-Cookie','uid=''; expires=Sun, 31-May-1999 23:59:59 GMT; path=/;')
        self.redirect('/')