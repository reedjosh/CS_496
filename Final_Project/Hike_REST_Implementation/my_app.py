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

import webapp2
from hike_history_handler import HikeHistoryHandler # NDB Database Model and HTTP Handlers
from hikers import Hiker, HikerHandler  # NDB Database Model and HTTP Handlers
from hikes import Hike, HikeHandler # NDB Database Model and HTTP Handlers

# Main page handler.
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("hello")
            
# Add patch as a http method.
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

# Set http routes.
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/hikes', HikeHandler),
                               ('/hikes/(.*)', HikeHandler),
                               ('/hikers/(.*)/hikes', HikeHistoryHandler),
                               ('/hikers/?(.*)', HikerHandler)],
                              debug=True)
    
