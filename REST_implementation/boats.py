from google.appengine.ext import ndb
import webapp2
import json


class Boat(ndb.Model):
    """Models a boat with associated properties."""
    name = ndb.StringProperty(required=True)
    type = ndb.StringProperty(required=True)
    length = ndb.IntegerProperty(required=True)
    at_sea = ndb.BooleanProperty(required=True)
    slip = ndb.StringProperty()



class BoatHandler(webapp2.RequestHandler):

    
    def post(self):
        """Create a Boat."""
        boat_data = json.loads(self.request.body)
        boat_data['at_sea'] = True
        new_boat = Boat(**boat_data)
        new_boat.put()
        boat_dict = new_boat.to_dict()
        boat_dict['self'] = '/boats/' + new_boat.key.urlsafe()
        self.response.write(json.dumps(boat_dict, sort_keys=True, indent=4))

    def get(self, id=None):
        """Get info about a boat or boats."""
        if id:
            boat = ndb.Key(urlsafe=id).get()
            if boat:
                boat = ndb.Key(urlsafe=id).get()
                boat_dict = boat.to_dict()
                boat_dict['self'] = '/boats/' + id
                self.response.write(json.dumps(boat_dict, sort_keys=True, indent=4))
            else:
                self.response.status = "405 Bad ID";
                self.response.write('Bad Id Provided')
        else: # respond with a list of boats
            boats = Boat.query().fetch()
            boat_dicts = {'Boats':[]}
            for boat in boats: # Convert boats to a dictionary.
                id = boat.key.urlsafe()
                boat_data = boat.to_dict()
                boat_data['self'] = '/boats/' + id
                boat_data['id'] = id
                boat_dicts['Boats'].append(boat_data)
            self.response.write(json.dumps(boat_dicts, sort_keys=True, indent=4))

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
                self.response.write(json.dumps(boat_dict, sort_keys=True, indent=4))
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
