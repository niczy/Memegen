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
from controllers import images
from controllers import api
from controllers import page
import jinja2
import os

app = webapp2.WSGIApplication([
    ('/', page.PageHandler),
    ('/api/meme/([^/]+)', api.ApiMeme), # Get/Post a Meme by ID.
    ('/api/memelist/([^/]+)', api.ApiMemeList), # Get a list of MemeID by different criterias.
    ('/i/upload', images.UploadHandler),
    ('/i/download/([^/]+)?', images.DownloadHandler),
    ('/i/serve/([^/]+)?', images.ServeHandler),
    ('/upload', images.UploadPageHandler),
    ('/([^/]+)', page.PageHandler)
],debug=True)
