'''
Created on Mar 27, 2012

@author: charliezhang
'''

import webapp2

from controllers import render_page
from google.appengine.api import mail
from models import user

class SetNewPassword(webapp2.RequestHandler):
    def get(self, link, expired=False, error=False, msg=''):
        username = ''
        if expired == False:
            usr = user.check_password_reset_link(link)
            if usr == None:
                expired = True
            else:
                username = usr.username
        render_page(self, "set_password", expired= expired, error=error, msg=msg)

    def post(self, link):
        usr = user.check_password_reset_link(link)
        password = self.request.get('password')
        confirm = self.request.get('confirm')
        expired = False
        error = False
        msg = ''
        if usr:
            msg = user.validate_password(password, confirm)
            if not msg:
                user.reset_user_password(usr, password)
                user.clear_password_reset_link(usr)
                self.redirect('/login')
            else: 
                error = True
        else:
            expired = True
        self.get(link, expired=expired, error=error, msg=msg)

class ResetPassword(webapp2.RequestHandler):
    def get(self):
        render_page(self, "get_password", msg = '', success =False)
    
    def post(self):
        uoe = self.request.get('uoe')
        usr = user.get_user_by_username_or_email(uoe)
        msg = ''
        success = False
        if usr == None:
            msg = 'User doesn\'t exist'
        else:
            link = user.create_password_reset_link(user)
            user.set_password_reset_link(usr, link)
            self.send_password_reset_email(usr, link)
            success = True
            msg = 'The password reset link has been sent to you by email.'
        render_page(self, "get_password", msg = msg, success = success)

    @staticmethod
    def send_password_reset_email(usr, link):
        #TODO(Zero): Change the link to the actual domain
        body = 'Click the following link to reset your password:\n http://localhost:8080/setnewpassword/%s\n' % link
        
        #TODO(Zero): Change to team email address.
        me = 'zero891109@gmail.com'
        you = usr.email
        # you == the recipient's email address
        subject = 'Your password on toeflkiller.com'

        mail.send_mail(me, you, subject, body)