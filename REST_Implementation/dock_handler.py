# Joshua Reed
# OSU EECS
# CS_496 -> Web Development
# Summer, 2017
#
# dock_handler.py
#
# Description: Contains the DockHandler class that manages docking slips 
# and boats.
# Use: To run, enter "dev_appserver.py ./*". Then check the porst listed in 
# the console. Thereafter, the page shouldu be usable at that port via a 
# browser or rest client.

import webapp2
import json
from helpers import jsonDumps, getObj
from google.appengine.ext import ndb
from google.net.proto.ProtocolBuffer import ProtocolBufferDecodeError

class DockHandler(webapp2.RequestHandler):

    def _sendErr(self, code, message):
        self.response.status = code
        self.response.write(message)
        self.err=True

    def put(self, slip_id):
        self.err = False
        """Dock a boat in a slip."""
        print(self.request.body)
        err = False

        # Attempt to get body
        try:
            body = json.loads(self.request.body)
        except ValueError:
            self._sendErr(405, 'Error: Body not proper JSON.')

        # Attempt to get boat obj.
        if not self.err:    
            boat = getObj(body['boat_id'])
            if not boat:
                self._sendErr(405, 'Error: Bad boat ID.')
        
        # Attempt to get slip obj.
        if not self.err:    
            slip = getObj(slip_id)
            if not slip:
                self._sendErr(405, 'Error: Bad slip ID.')
        
        # Check if slip is occupied. 
        if not self.err:
            if slip.current_boat != 'null':
                self._sendErr(403, 'Error: Slip already occupied.')

        # If no errors yet, dock boat in slip.
        if not self.err:
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
            self.response.write(jsonDumps(slip_dict))
            self.response.write(jsonDumps(boat_dict))
