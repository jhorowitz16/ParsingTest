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
import urllib
import logging


# from google.cloud import automl_v1beta1
# from google.cloud.automl_v1beta1.proto import service_pb2


class MainPage(webapp2.RequestHandler):
    def get(self):
        # self.response.headers['Content-Type'] = 'text/plain'
        # self.response.write('<h1>Hello friend</h1><input type="text"/><button>Submit</button>')

        url = 'http://www.google.com/humans.txt'

        form_fields = {
            'textSnippet': {
                'content': 'hello friend',
                'mime_type': 'text/plain'
            }
        }

        url = 'https://automl.googleapis.com/v1beta1/projects/confident-trail-214602/locations/us-central1/models/TCN5019025096457053612:predict'

        try:
            form_data = urllib.urlencode(form_fields)
            form_data = 'textSnippet%3A%20%7B%22content%22%3A%20%22YOUR%20TEXT%20HERE%22%2C%22mime_type%22%3A%20%22text%2Fplain%22%20%7D'
            headers = {
                'Authorization': 'Bearer ya29.c.ElpHBimhOCsmYiSMJRHHctXEfVsHYe8VhQYwvECTXtBPo4_vNLoHE3OvumiywKV2Odt1_ZLtAxT5jsCH8lcJpWYT7HcGWKaeT_6a7f2smzEKJJ7ZEZmrMS9w5dY',
                'Content-Type': 'application/json'
                }
            # result = urlfetch.fetch(url)
            result = urlfetch.fetch(
                url=url,
                payload=form_data,
                method=urlfetch.POST,
                headers=headers)
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
