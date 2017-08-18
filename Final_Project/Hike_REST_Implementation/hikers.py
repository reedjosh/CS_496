# Joshua Reed
# OSU EECS
# CS_496 -> Web Development
# Summer, 2017
#
# hikers.py
#
# Description: Contains the hiker ndb model and hiker handler classes.
#
# Use: To run, enter "dev_appserver.py ./*". Then check the porst listed in 
# the console. Thereafter, the page shouldu be usable at that port via a 
# browser or rest client.

from google.appengine.ext import ndb
from google.net.proto.ProtocolBuffer import ProtocolBufferDecodeError
import webapp2
import json
from helpers import jsonDumps, getObj

class Hiker(ndb.Model):
    """Models a hiker with associated properties."""
    name = ndb.StringProperty(required=True)
    height = ndb.IntegerProperty(required=True)
    weight = ndb.IntegerProperty(required=True)
    hiking_history = ndb.StringProperty(required=False, repeated=True)

    
    def toJsonStr(self):
        """Converts a hiker to a pretty JSON string for responses."""
        id = self.key.urlsafe()
        hiker_data = self.to_dict()
        hiker_data['id'] = id
        hiker_data['self'] = '/hikers/' + id
        if hiker_data['hiking_history'] != 'null':
            hiker_data['hike_links'] = \
                ['/hikes/' + hike for hike in hiker_data['hiking_history']]
        return jsonDumps(hiker_data)
        


class HikerHandler(webapp2.RequestHandler):


    def __init__(self, *args, **kwargs):
        """Template from the super class's init and add err flag."""
        self.err = False
        super(HikerHandler, self).__init__(*args, **kwargs)


    def _sendErr(self, code, message):
        """Send an error code and set the err flag."""
        self.response.status = code
        self.response.write(message)
        self.err=True


    def post(self, id=None):
        """Create a hiker."""

        # Get the body of the post.
        try: body = json.loads(self.request.body)
        except: self._sendErr(405, "Error: Couldn't get body data")

        # Prevent posting with an id.
        if id:
            self._sendErr(403, "Error: A hike cannot be posted with an id.")

        # Prevent duplicate numbered hiker...
        #if Hiker.query(Hiker.number == body['']).get(): 
        #    self._sendErr(403, "Error: A hiker of that numer already exists.")

        # If no errors, create the hiker...
        if not self.err:
            new_hiker = Hiker(**body)
            new_hiker.put()
            self.response.write(new_hiker.toJsonStr())


    def get(self, id=None):
        """Get either a specific hiker, or a list of all hikers."""  
        if id:

            # Attempt to get hiker with given id.
            hiker = getObj(id)

            # Send an error if no hiker found with said id.
            if not hiker: 
                self.sendErr(405, "Error: Bad hiker id.")

            # If no error set, respond with hiker info.
            if not self.err:
                self.response.write(hiker.toJsonStr())
        else:
            # Get all hiker.
            hiker = Hiker.query().fetch()

            # Populate the list of hiker.
            hiker_dicts = {'hikers':[]}
            for hiker in hiker: # Convert hiker to a dictionary.
                hiker_dicts['hikers'].append(json.loads(hiker.toJsonStr()))

            # Send all hiker.
            self.response.write(jsonDumps(hiker_dicts))

    def patch(self, id=None):
        """Edit a hiker."""
        # Enforce id requriement.
        if not id:
            self._sendErr(403, 'Error: Id Required for Patch')
        
        # If no error, attempt to get hiker with given id, send error if not.
        if not self.err:
            hiker = getObj(id)
            if not hiker: 
                self.sendErr(405, "Error: Bad hiker id.")

        # If no errors, get the body of the post.
        if not self.err:
            try: body = json.loads(self.request.body)
            except: self._sendErr(405, "Error: Couldn't get body data")

        # If no errors, then patch using body data.
        if not self.err:
            if 'name' in body:
                hiker.name = body['name']
            if 'height' in body:
                hiker.height = body['height']
            if 'hiking_history' in body:
                hiker.hiking_history = body['hiking_history']
            if 'weight' in body:
                hiker.weight = body['weight']

            hiker.put()
            self.response.write(hiker.toJsonStr())

    def delete(self, id=None):
        """Delete a hiker."""
        # Enforce id requriement.
        if not id:
            self._sendErr(403, 'Error: Id Required for Delete.')

        # If no error, attempt to get hiker with given id, send error if not.
        if not self.err:
            hiker = getObj(id)
            if not hiker: 
                self.sendErr(405, "Error: Bad hiker id.")

        # If no errors, delete the hiker.
        if not self.err:
            hiker.key.delete()
            self.response.write('Hiker Deleted')
