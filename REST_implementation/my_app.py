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
from dock_handler import DockHandler # NDB Database Model and HTTP Handlers
from slips import Slip, SlipHandler  # NDB Database Model and HTTP Handlers
from boats import Boat, BoatHandler  # NDB Database Model and HTTP Handlers

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
                               ('/boats', BoatHandler),
                               ('/boats/(.*)', BoatHandler),
                               ('/slips/(.*)/dock', DockHandler),
                               ('/slips/?(.*)', SlipHandler)],
                              debug=True)
    
