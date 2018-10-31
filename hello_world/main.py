# Copyright 2016 Google Inc.
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

import webapp2
import os
from google.appengine.ext.webapp import template
import sys

from google.appengine.api import urlfetch


# from google.cloud import automl_v1beta1
# from google.cloud.automl_v1beta1.proto import service_pb2


class MainPage(webapp2.RequestHandler):
    def get(self):
        # self.response.headers['Content-Type'] = 'text/plain'
        # self.response.write('<h1>Hello friend</h1><input type="text"/><button>Submit</button>')

        url = 'http://www.google.com/humans.txt'
        try:
            result = urlfetch.fetch(url)
            if result.status_code == 200:
                self.response.write(result.content)
            else:
                self.response.status_code = result.status_code
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')

        # path = os.path.join(os.path.dirname(__file__), 'index.html')
        # self.response.out.write(template.render(path, {}))


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
