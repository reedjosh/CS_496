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

def jsonDumps(dict):
    """Use this function and change format of json dumps here for uniformity."""
    json.dumps(dict, sort_keys=True, indent=2)
