'''
Created on Mar 27, 2012

@author: charliezhang
'''
import webapp2

from controllers import render_page
from controllers import response_json
from models import user

class SignUp(webapp2.RequestHandler):
    def get(self):
        render_page(self, 'signup', error=False)
    
    def post(self):
        
        username = self.request.get('username')
        email = self.request.get('email')
        password = self.request.get('password')
        confirm = self.request.get('confirm')
        msg = user.register_user(username, email, password, confirm)
        if msg:
            render_page(self, 'signup', error=True,
                                        error_msg  = msg,
                                        username = username,
                                        email = email)
            return
        
        msg = user.login_with_username_or_email(self, username, password)
        if not msg:
            self.redirect('/');
        else:
            self.redirect('/login')
           
class SignUpCheck(webapp2.RequestHandler):
    def get(self, check_field):
        pass
    
    def post(self, check_field):
        value = self.request.get('value')
        result = ''
        if check_field == 'username':
            result = user.validate_username(value)
            if not result:
                result = 'good'

        elif check_field == 'email':
            result = user.validate_email(value)
            if not result:
                result = 'good'
        response_json(self, result, 'text/plain');