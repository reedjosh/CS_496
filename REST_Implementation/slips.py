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
from helpers import jsonDumps

class Slip(ndb.Model):
    """Models a slip that can store a boat."""
    number = ndb.IntegerProperty(required=True)
    current_boat = ndb.StringProperty(required=True) 
    arrival_date = ndb.StringProperty(required=True) 


class SlipHandler(webapp2.RequestHandler):
    def _getSlip(self, id):
        """A slip getter that submits error if needed."""
        if id:
            try: slip = ndb.Key(urlsafe=id).get()
            except (TypeError, ValueError, ProtocolBufferDecodeError):
                slip = None
                self.response.status = "405 Bad Id";
                self.response.write('Error: Bad Id Provided')
        return slip 

    def post(self, id=None):
        """Create a slip."""
        try: slip_data = json.loads(self.request.body)
        except: slip_data = None
        if id:
            print(id)
            print(id)
            self.response.status = "403 Forbidden"
            self.response.write('Error: A slip cannot be posted with an id.')
        elif not slip_data:
                self.response.status = "405 Bad Input";
                self.response.write('Error: No body provided with post.')
        elif Slip.query(Slip.number == slip_data['number']).get() is None: 
            slip_data['arrival_date'] = "null";
            slip_data['current_boat'] = "null";
            new_slip = Slip(**slip_data)
            new_slip.put()
            slip_dict = new_slip.to_dict()
            slip_dict['self'] = '/slip/' + new_slip.key.urlsafe()
            self.response.write(jsonDumps(slip_data))
        else:
            self.response.status = "403 Forbidden"
            self.response.write('Error: A slip of that number exists.')

    def get(self, id=None):
        if id:
            slip = self._getSlip(id)
            if slip:
                slip_key = ndb.Key(urlsafe=id)
                slip = slip_key.get()
                slip_dict = slip.to_dict()
                slip_dict['self'] = '/slips/' + id
                self.response.write(jsonDumps(slip_dict))

        else: # respond with a list of slips
            slips = Slip.query().fetch()
            slip_dicts = {'Slips':[]}
            for slip in slips: # Convert slips to a dictionary.
                id = slip.key.urlsafe()
                slip_data = slip.to_dict()
                slip_data['self'] = '/slips/' + id
                slip_data['id'] = id
                slip_dicts['Slips'].append(slip_data)
            self.response.write(jsonDumps(slip_dicts))

    def patch(self, id=None):
        """Edit a slip."""
        if id:
            slip = ndb.Key(urlsafe=id).get()
            if slip:
                slip_data = json.loads(self.request.body)
                if 'number' in slip_data:
                    slip.number = slip_data['number']
                slip.put()
                slip_dict = slip.to_dict()
                self.response.write(jsonDumps(slip_dict))
            else:
                self.response.status = "405 Bad Id";
                self.response.write('Error: Bad Id Provided')
        else:
            self.response.status = "403 No ID";
            self.response.write('Error: Id Required for Patch')

    def delete(self, id=None):
        """Delete a slip."""
        if id:
            slip = ndb.Key(urlsafe=id).get()
            if slip:
                slip.key.delete()
                self.response.write('Slip Deleted')
            else:
                self.response.status = "405 Bad Id";
                self.response.write('Error: Bad Id Provided')
        else:
            self.response.status = "403 No ID";
            self.response.write('Error: Id Required for Delete')
