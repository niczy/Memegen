#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from controllers import account
from controllers import api
from controllers import images
from controllers import login
from controllers import page
from controllers import signup
import jinja2
import os
import config

URL_MAP = [
    ('/', page.PageHandler),
    (r'/makememe', page.MakeMemeHandler),
    (r'/makememe/(.*)', page.MakeMemeHandler),
    (r'/make', page.MakeHandler),
    (r'/make/(.*)', page.MakeHandler),
    ('/meme/(.*)', page.MemeHandler),
    ('/api/comments/([^/]+)', api.ApiComments), # Get a list of comments OR Post a comment, given the mid.
    ('/api/meme/([^/]+)', api.ApiMeme), # Get/Post a Meme by ID.
    ('/api/memelist/([^/]+)', api.ApiMemeList), # Get a list of Meme by different criterias.
    ('/api/templatelist/([^/]+)?', api.ApiTemplateList), # Get a list of Meme by different criterias.
    ('/i/upload', images.UploadHandler),
    ('/i/download/([^/]+)?', images.DownloadHandler),
    ('/i/serve/([^/]+)?', images.ServeHandler),
    ('/makememe', page.MakeMeme),
    ('/upload', images.UploadPageHandler),  
    (r'/resetpassword', account.ResetPassword),
    (r'/setnewpassword/(.*)', account.SetNewPassword),             
    (r'/signup_check/(.*)', signup.SignUpCheck),
    (r'/signup', signup.SignUp),
    (r'/login', login.Login),
    (r'/logout', login.Logout)
]
URL_MAP_DEBUG = [
    (r'/debug', page.Debug),
    ('/([^/]+)', page.PageHandler)
]

if config.DEBUG:
    for i in URL_MAP_DEBUG:
        URL_MAP.append(i)

app = webapp2.WSGIApplication(URL_MAP, debug=config.DEBUG)
