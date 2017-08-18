# Joshua Reed
# OSU EECS
# CS_496 -> Web Development
# Summer, 2017
#
# hikes.py
#
# Description: Implements a restful api that tracks Hikers and Hikes
# Uses Google App Engine as the service provider. Intended to interact with
# an Android app.
#
# Use: To run, enter "dev_appserver.py ./*". Then check the porst listed in 
# the console. Thereafter, the page shouldu be usable at that port via a 
# browser or rest client.

from google.appengine.ext import ndb
import webapp2
import json
from helpers import jsonDumps, getObj


class Hike(ndb.Model):
    """Models a hike with associated properties."""
    name = ndb.StringProperty(required=True)
    total_time = ndb.IntegerProperty(required=True)
    min_altitude = ndb.IntegerProperty(required=True)
    max_altitude= ndb.IntegerProperty(required=True)
    coordinates = ndb.JsonProperty(required=True)
    hiker = ndb.StringProperty(required=False)
    distance = ndb.IntegerProperty(required=True)

class HikeHandler(webapp2.RequestHandler):


    def __init__(self, *args, **kwargs):
        """Template from the super class's init and add err flag."""
        self.err = False
        super(HikeHandler, self).__init__(*args, **kwargs)

    
    def _sendErr(self, code, message):
        """Send an error code and set the err flag."""
        self.response.status = code
        self.response.write(message)
        self.err=True


    def post(self):
        """Create a hike."""
        
        # Attempt to get body
        try:
            body = json.loads(self.request.body)
        except ValueError:
            self._sendErr(405, 'Error: Body not proper JSON.')

        if not self.err:
            # Create and store hike...
            newHike = Hike(**body)
            newHike.put()

            # Set hike's self url...
            hike_dict = newHike.to_dict()
            hike_dict['self'] = '/hike/' + newHike.key.urlsafe()
            hike_dict['id'] = newHike.key.urlsafe()

            # Responde to request with JSON hike data...
            self.response.write(jsonDumps(hike_dict))


    def get(self, id=None):
        """Get info about a hike."""

        # If an id was provided, attempt to return the associated hike's data.
        # Else return the data for all hike.
        if id:
            hike = getObj(id)
            if hike:
                hike_dict = hike.to_dict()
                hike_dict['self'] = '/hike/' + id
                hike_dict['id'] = id
                self.response.write(jsonDumps(Hike_dict))
            else:
                sendErr(405, "Error: Bad hike id provided.")
        else:
            # Get all hikes.
            hikes = Hike.query().fetch()

            # Convert hike to a dictionary with key hikes...
            hike_dicts = {'hikes':[]}
            print(type(ndb))
            for hike in hikes: 
                id = hike.key.urlsafe()
                hike_data = hike.to_dict()
                hike_data['self'] = '/hike/' + id
                hike_data['id'] = id
                hike_dicts['hikes'].append(hike_data)

            # Respond with data of hike.
            self.response.write(jsonDumps(hike_dicts))

    def patch(self, id=None):
        """Edit a hike."""
        if id:
            hike = ndb.Key(urlsafe=id).get()
            if hike:
                hike_data = json.loads(self.request.body)
                if 'coordinates' in hike_data:
                    hike.coordinates = hike_data['coordinates']
                if 'distance' in hike_data:
                    hike.distance = hike_data['distance']
                if 'total_timeime' in hike_data:
                    hike.total_time = hike_data['total_timeime']
                if 'min_altitude' in hike_data:
                    hike.min_altitude = hike_data['min_altitude']
                if 'max_altitude' in hike_data:
                    hike.max_altitude = hike_data['max_altitude']
                hike.put()
                hike_dict = hike.to_dict()
                self.response.write(jsonDumps(hike_dict))
            else:
                self.response.status = "405 Bad Id";
                self.response.write('Error: Bad Id Provided')
        else:
            self.response.status = "403 No ID";
            self.response.write('Error: Id Required for Patch')

    def delete(self, id=None):
        """Delete a hike."""
        if id:
            hike = ndb.Key(urlsafe=id).get()
            if hike:
                if hike.hiker:
                    hiker = getObj(hike.hiker);
                    hiker.hiking_history.remove(id);
                    hiker.put()
                hike.key.delete()
                self.response.write('Hike Deleted')
            else:
                self.response.status = "405 Bad Id";
                self.response.write('Error: Bad Id Provided')
        else:
            self.response.status = "403 No ID";
            self.response.write('Error: Id Required for Delete')

























