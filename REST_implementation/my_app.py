# Joshua Reed
# OSU EECS
# CS_496 -> Web Development
# Summer, 2017
#
# boats_and_slips.py
#
# Description: Implements a restful api that tracks boats in and out of slips.
# Uses Google App Engine as the service provider.
#
# Use: To run, enter "dev_appserver.py ./*". Then check the porst listed in 
# the console. Thereafter, the page shouldu be usable at that port via a 
# browser or rest client.

import webapp2
import json
from google.appengine.ext import ndb
from slips import Slip, SlipHandler  # NDB Database Model and HTTP Handlers
from boats import Boat, BoatHandler  # NDB Database Model and HTTP Handlers
from google.net.proto.ProtocolBuffer import ProtocolBufferDecodeError


class DockHandler(webapp2.RequestHandler):
    def put(self, slip_id):
        """Dock a boat in a slip."""
        print(self.request.body)
        err = False
        # Attempt to get body
        try:
            body = json.loads(self.request.body)
        except ValueError:
            self.response.status = '405 Bad Input'
            self.response.write('Error: Body not proper JSON.')
            err = True
        if not err:    
            # Try block here for google bug...
            try:
                boat = ndb.Key(urlsafe=body['boat_id']).get()
            except ProtocolBufferDecodeError:
                self.response.status = '405 Bad Input'
                self.response.write('Error: Bad boat ID.')
                err = True
        if not err:    
            # Try block here for google bug...
            try:
                slip = ndb.Key(urlsafe=slip_id).get()
            except ProtocolBufferDecodeError:
                self.response.status = '405 Bad Input'
                self.response.write('Error: Bad slip ID.')
                err = True
        if not err:
            slip.arrival_date = body['arrival_date']
            slip.current_boat = body['boat_id']
            boat.at_sea = False  
            boat.slip = slip_id  
            slip.put()
            boat.put()
            # Modify the dictionaries' to link to proper urls in responses.
            slip_dict = slip.to_dict()
            boat_dict  = boat.to_dict()
            slip_dict['current_boat'] = '/boats/' + body['boat_id']
            boat_dict['slip'] = '/slips/' + slip_id  
            self.response.write(json.dumps(slip_dict, sort_keys=True, indent=4))
            self.response.write(json.dumps(boat_dict, sort_keys=True, indent=4))
            

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
    
