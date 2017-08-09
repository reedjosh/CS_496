# Joshua Reed
# OSU EECS
# CS_496 -> Web Development
# Summer, 2017
#
# helpers.py
#
# Description: Helper functions used in various places in the project.


from google.appengine.ext import ndb
import webapp2
import json
from google.net.proto.ProtocolBuffer import ProtocolBufferDecodeError

def jsonDumps(dict):
    """Use this function and change format of json dumps here for uniformity."""
    return json.dumps(dict, sort_keys=True, indent=2)

def getObj(id):
    """Attempt to get ndb obj and return none if error."""
    obj = None
    # Try block here for google bug...
    try:
        obj = ndb.Key(urlsafe=id).get()
    except ProtocolBufferDecodeError:
        pass
    return obj
            
