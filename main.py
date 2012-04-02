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
    (r'/', page.PageHandler),
    (r'/api/addtofavorites/([^/]+)?', api.ApiAddToFavorites), #User add a Meme to his Favorites
    (r'/api/comments/([^/]+)', api.ApiComments), # Get a list of comments OR Post a comment, given the mid.
    (r'/api/getfavorites', api.ApiGetFavorites), #Return lists of user's favorite memes by different category
    (r'/api/like/([^/]+)?', api.ApiLike),
    (r'/api/meme/([^/]+)', api.ApiMeme), # Get/Post a Meme by ID.
    (r'/api/memelist/([^/]+)', api.ApiMemeList), # Get a list of Meme by different criterias.
    (r'/api/templatelist/([^/]+)?', api.ApiTemplateList), # Get a list of Meme by different criterias.
    (r'/i/upload', images.UploadHandler),
    (r'/i/download/([^/]+)?', images.DownloadHandler),
    (r'/i/serve/([^/]+)?', images.ServeHandler),
    (r'/login', login.Login),
    (r'/logout', login.Logout),
    (r'/make', page.MakeHandler),
    (r'/make/(.*)', page.MakeHandler),
    (r'/makememe', page.MakeMemeHandler),
    (r'/makememe/(.*)', page.MakeMemeHandler),
    (r'/meme/(.*)', page.MemeHandler),   
    (r'/resetpassword', account.ResetPassword),
    (r'/setnewpassword/(.*)', account.SetNewPassword),             
    (r'/signup_check/(.*)', signup.SignUpCheck),
    (r'/signup', signup.SignUp),
    (r'/upload', images.UploadPageHandler)   
]
URL_MAP_DEBUG = [
    (r'/debug', page.Debug),
    (r'/([^/]+)', page.PageHandler)
]

if config.DEBUG:
    for i in URL_MAP_DEBUG:
        URL_MAP.append(i)

app = webapp2.WSGIApplication(URL_MAP, debug=config.DEBUG)
