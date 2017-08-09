# Joshua Reed
# OSU EECS
# CS_496 -> Web Development
# Summer, 2017
#
# boats.py
#
# Description: Implements a restful api that tracks boats in and out of slips.
# Uses Google App Engine as the service provider.
#
# Use: To run, enter "dev_appserver.py ./*". Then check the porst listed in 
# the console. Thereafter, the page shouldu be usable at that port via a 
# browser or rest client.

from google.appengine.ext import ndb
import webapp2
import json
from helpers import jsonDumps, getObj


class Boat(ndb.Model):
    """Models a boat with associated properties."""
    name = ndb.StringProperty(required=True)
    type = ndb.StringProperty(required=True)
    length = ndb.IntegerProperty(required=True)
    at_sea = ndb.BooleanProperty(required=True)
    slip = ndb.StringProperty()

class BoatHandler(webapp2.RequestHandler):


    def __init__(self, *args, **kwargs):
        """Template from the super class's init and add err flag."""
        self.err = False
        super(BoatHandler, self).__init__(*args, **kwargs)

    
    def _sendErr(self, code, message):
        """Send an error code and set the err flag."""
        self.response.status = code
        self.response.write(message)
        self.err=True


    def post(self):
        """Create a Boat."""
        
        # Attempt to get body
        try:
            body = json.loads(self.request.body)
        except ValueError:
            self._sendErr(405, 'Error: Body not proper JSON.')

        if not self.err:
            # Set the boat data to be at sea...
            body['at_sea'] = True

            # Create and store boat...
            new_boat = Boat(**body)
            new_boat.put()

            # Set boat's self url...
            boat_dict = new_boat.to_dict()
            boat_dict['self'] = '/boats/' + new_boat.key.urlsafe()

            # Responde to request with JSON boat data...
            self.response.write(jsonDumps(boat_dict))


    def get(self, id=None):
        """Get info about a boat or boats."""

        # If an id was provided, attempt to return the associated boat's data.
        # Else return the data for all boats.
        if id:
            boat = getObj(id)
            if boat:
                boat_dict = boat.to_dict()
                boat_dict['self'] = '/boats/' + id
                self.response.write(jsonDumps(boat_dict))
            else:
                sendErr(405, "Error: Bad boat id provided.")
        else:
            # Get all boats.
            boats = Boat.query().fetch()

            # Convert boats to a dictionary with key Boats...
            boat_dicts = {'Boats':[]}
            for boat in boats: 
                id = boat.key.urlsafe()
                boat_data = boat.to_dict()
                boat_data['self'] = '/boats/' + id
                boat_data['id'] = id
                boat_dicts['Boats'].append(boat_data)

            # Respond with data of Boats.
            self.response.write(jsonDumps(boat_dicts))

    def patch(self, id=None):
        """Edit a Boat."""
        if id:
            boat = ndb.Key(urlsafe=id).get()
            if boat:
                boat_data = json.loads(self.request.body)
                if 'name' in boat_data:
                    boat.name = boat_data['name']
                if 'length' in boat_data:
                    boat.length = boat_data['length']
                if 'type' in boat_data:
                    boat.type = boat_data['type']
                boat.put()
                boat_dict = boat.to_dict()
                self.response.write(jsonDumps(boat_dict))
            else:
                self.response.status = "405 Bad Id";
                self.response.write('Error: Bad Id Provided')
        else:
            self.response.status = "403 No ID";
            self.response.write('Error: Id Required for Patch')

    def delete(self, id=None):
        """Delete a boat."""
        if id:
            boat = ndb.Key(urlsafe=id).get()
            if boat:
                boat.key.delete()
                self.response.write('Boat Deleted')
            else:
                self.response.status = "405 Bad Id";
                self.response.write('Error: Bad Id Provided')
        else:
            self.response.status = "403 No ID";
            self.response.write('Error: Id Required for Delete')
