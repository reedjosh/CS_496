# Joshua Reed
# OSU EECS
# CS_496 -> Web Development
# Summer, 2017
#
# slips.py
#
# Description: Contains the slip ndb model and slip handler classes.
#
# Use: To run, enter "dev_appserver.py ./*". Then check the porst listed in 
# the console. Thereafter, the page shouldu be usable at that port via a 
# browser or rest client.

from google.appengine.ext import ndb
from google.net.proto.ProtocolBuffer import ProtocolBufferDecodeError
import webapp2
import json
from helpers import jsonDumps, getObj

class Slip(ndb.Model):
    """Models a slip that can store a boat."""
    number = ndb.IntegerProperty(required=True)
    current_boat = ndb.StringProperty(required=True) 
    arrival_date = ndb.StringProperty(required=True) 

    
    def toJsonStr(self):
        """Converts a slip to a pretty JSON string for responses."""
        id = self.key.urlsafe()
        slip_data = self.to_dict()
        slip_data['id'] = id
        slip_data['self'] = '/slips/' + id
        if slip_data['current_boat'] != 'null':
            slip_data['boat_link'] = '/boats/' + slip_data['current_boat']
        return jsonDumps(slip_data)
        


class SlipHandler(webapp2.RequestHandler):


    def __init__(self, *args, **kwargs):
        """Template from the super class's init and add err flag."""
        self.err = False
        super(SlipHandler, self).__init__(*args, **kwargs)


    def _sendErr(self, code, message):
        """Send an error code and set the err flag."""
        self.response.status = code
        self.response.write(message)
        self.err=True


    def post(self, id=None):
        """Create a slip."""

        # Get the body of the post.
        try: body = json.loads(self.request.body)
        except: self._sendErr(405, "Error: Couldn't get body data")

        # Prevent posting with an id.
        if id:
            self._sendErr(403, "Error: A slip cannot be posted with an id.")

        # Prevent duplicate numbered slips...
        if Slip.query(Slip.number == body['number']).get(): 
            self._sendErr(403, "Error: A slip of that numer already exists.")

        # If no errors, create the slip...
        if not self.err:
            body['arrival_date'] = "null";
            body['current_boat'] = "null";
            print("hello")
            print(body)
            new_slip = Slip(**body)
            new_slip.put()
            self.response.write(new_slip.toJsonStr())


    def get(self, id=None):
        """Get either a specific slip, or a list of all slips."""
        if id:

            # Attempt to get slip with given id.
            slip = getObj(id)

            # Send an error if no slip found with said id.
            if not slip: 
                self.sendErr(405, "Error: Bad slip id.")

            # If no error set, respond with slip info.
            if not self.err:
                self.response.write(slip.toJsonStr())
        else:
            # Get all slips.
            slips = Slip.query().fetch()

            # Populate the list of slips.
            slip_dicts = {'Slips':[]}
            for slip in slips: # Convert slips to a dictionary.
                slip_dicts['Slips'].append(json.loads(slip.toJsonStr()))

            # Send all slips.
            self.response.write(jsonDumps(slip_dicts))

    def patch(self, id=None):
        """Edit a slip."""
        # Enforce id requriement.
        if not id:
            self._sendErr(403, 'Error: Id Required for Patch')
        
        # If no error, attempt to get slip with given id, send error if not.
        if not self.err:
            slip = getObj(id)
            if not slip: 
                self.sendErr(405, "Error: Bad slip id.")

        # If no errors, get the body of the post.
        if not self.err:
            try: body = json.loads(self.request.body)
            except: self._sendErr(405, "Error: Couldn't get body data")

        # If no errors, then patch using body data.
        if not self.err:
            if 'number' in body:
                slip.number = body['number']
            slip.put()
            self.response.write(slip.toJsonStr())

    def delete(self, id=None):
        """Delete a slip."""
        # Enforce id requriement.
        if not id:
            self._sendErr(403, 'Error: Id Required for Delete.')

        # If no error, attempt to get slip with given id, send error if not.
        if not self.err:
            slip = getObj(id)
            if not slip: 
                self.sendErr(405, "Error: Bad slip id.")

        # If no errors, delete the slip.
        if not self.err:
            slip.key.delete()
            self.response.write('Slip Deleted')
