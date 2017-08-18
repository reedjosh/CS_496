# Joshua Reed
# OSU EECS
# CS_496 -> Web Development
# Summer, 2017
#
# hike_history_handler.py
#
# Description: Contains the HikeHistorykHandler class that manages docking hikers 
# and hikes.
# Use: To run, enter "dev_appserver.py ./*". Then check the porst listed in 
# the console. Thereafter, the page shouldu be usable at that port via a 
# browser or rest client.

import webapp2
import json
from helpers import jsonDumps, getObj
from google.appengine.ext import ndb
from google.net.proto.ProtocolBuffer import ProtocolBufferDecodeError

class HikeHistoryHandler(webapp2.RequestHandler):

    def _sendErr(self, code, message):
        self.response.status = code
        self.response.write(message)
        self.err=True

    def put(self, hiker_id):
        """Add a hike to a hiker's hike history."""
        self.err = False

        # Attempt to get body
        try:
            body = json.loads(self.request.body)
        except ValueError:
            self._sendErr(405, 'Error: Body not proper JSON.')

        # Attempt to get hike obj.
        if not self.err:    
            hike = getObj(body['hike_id'])
            if not hike:
                self._sendErr(405, 'Error: Bad hike ID.')
        
        # Attempt to get hiker obj.
        if not self.err:    
            hiker = getObj(hiker_id)
            if not hiker:
                self._sendErr(405, 'Error: Bad hiker ID.')
        
        # If no errors yet, add hike to hiker's history.
        if not self.err:
            hike.hiker = hiker_id;
            hiker.hiking_history.append(body['hike_id'])
            hiker.hiking_history = list(set(hiker.hiking_history)) # Prevent duplicates
            hiker.put()
            hike.put()
            # Modify the dictionaries' to link to proper urls in responses.
            hiker_dict = hiker.to_dict()
            hike_dict  = hike.to_dict()
            hiker_dict['hike_links'] = \
                ['/hikes/' + hike for hike in hiker_dict['hiking_history']]
            self.response.write(jsonDumps(hiker_dict))
            #self.response.write(jsonDumps(hike_dict))
