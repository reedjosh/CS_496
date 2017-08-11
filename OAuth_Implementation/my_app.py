# Joshua Reed
# OSU EECS
# CS_496 -> Web Development
# Summer, 2017
#
# my_app.py
#
# Description: Contains the boat ndb model and boat handler classes.
#
# Use: To run, enter "dev_appserver.py ./*". Then check the porst listed in 
# the console. Thereafter, the page shouldu be usable at that port via a 
# browser or rest client.

import os
import json
import jinja2
import webapp2
from google.appengine.api import app_identity
import google.appengine.api.urlfetch as urlfetch

response = urlfetch.get('http://python.org/')
print(response.status, response.reason)
print(len(response.content))


JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"))

class OauthHandler(webapp2.RequestHandler):
    def get(self):
        logging.debug('The contents of the Get request are:' + repr(self.request.GET))

# Main page handler.
class MainPage(webapp2.RequestHandler):
    def get(self):
        template_vars = {"title": "Welcome to ABC Inc."}
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.out.write(template.render(template_vars))

class AboutPage(webapp2.RequestHandler):
    def get(self):
        template_vars = {"title": "About ABC Inc."}
        template = JINJA_ENVIRONMENT.get_template('about.html')
        self.response.out.write(template.render(template_vars))

class ProductsPage(webapp2.RequestHandler):
    def get(self):
        template_vars = {"title": "Products"}
        template = JINJA_ENVIRONMENT.get_template('products.html')
        self.response.out.write(template.render(template_vars))

class ProductsPage(webapp2.RequestHandler):
    def get(self):
        try:
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            result = urlfetch.fetch(
                url='http://localhost:8080/submit_form',
                method=urlfetch.GET,
                headers=headers)
            self.response.write(result.content)
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')
        template_vars = {"title": "Products"}
        template = JINJA_ENVIRONMENT.get_template('products.html')
        self.response.out.write(template.render(template_vars))
            
# Add patch as a http method.
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

# Set http routes.
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/index.html', MainPage),
                               ('/about.html', AboutPage),
                               ('/products.html', ProductsPage),
                               ('/oauth', OauthHandler)],
                              debug=True)
    
