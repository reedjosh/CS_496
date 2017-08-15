# Joshua Reed
# OSU EECS
# CS_496 -> Web Development
# Summer, 2017
#
# my_app.py
#
# Description: Contains the boat ndb model and boat handler classes.
#
# Use: To run, enter "dev_appserver.py ./*". Then check the ports listed in 
# the console. Thereafter, the Handler should be usable at that port via a 
# browser or rest client.

import os
import json
import jinja2
import webapp2
import urllib
import google.appengine.api.urlfetch as urlfetch


# The following are the app's id's.
CLIENT_ID = "976169239874-c4tghbm9r0400si67vhu6nhv5u2i75br.apps" + \
            ".googleusercontent.com"  
CLIENT_SECRET = "mWx1FT7jRMWEqFE89tmwk9NY" 


# This is the url to request an oauth token from google.
GOOGLE_URL = "https://accounts.google.com/o/oauth2/v2/auth"

# This is the url to request user data once a token is obtained.
GPLUS_URL = "https://www.googleapis.com/plus/v1/people/me"

# Switching either of these allows for local or cloud hosting.
# Local is useful for development.
HOME_URL = "https://oauth-reedjosh.appspot.com"
HOME_URL = "http://localhost:8080"
REDIRECT_URI = HOME_URL + "/oauth"


JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"))



# OAuth Handler -> Gets user data and posts it to user_info.html page.
class OauthHandler(webapp2.RequestHandler):
    def get(self):
        callback_state = self.request.get('state')
        code = self.request.get('code')
        
        if callback_state != "SuperSecret9000":
        	template_vars = {'error': "State var didn't match."}
        	template = JINJA_ENVIRONMENT.get_template('500_server_error.html')
        	self.response.write(template.render(template_vars))
        	return

        # Setup for token request.
        header = {'Content-Type':'application/x-www-form-urlencoded'}
        post_vars ={'code':code,
        	    'client_id':CLIENT_ID,
        	    'client_secret':CLIENT_SECRET,
        	    'redirect_uri':REDIRECT_URI,
        	    'grant_type':'authorization_code'}
        encoded_data = urllib.urlencode(post_vars)

        # Request token.
        result = urlfetch.fetch("https://www.googleapis.com/oauth2/v4/token/",
                                headers=header, payload=encoded_data,
                                method=urlfetch.POST)
        token = json.loads(result.content)

        # Google Plus URL (https required).
        header = {'Authorization': 'Bearer ' + token['access_token']}
        response = urlfetch.fetch(GPLUS_URL, headers=header)
        
        gplus_data = json.loads(response.content)
    
        template = JINJA_ENVIRONMENT.get_template('user_info.html')
        template_vars = {'username': gplus_data['displayName'],
                         'email': gplus_data['emails'][0]['value']}
        self.response.write(template.render(template_vars))
        return
 

# Main handler.
class MainHandler(webapp2.RequestHandler):
    def get(self):
        # Build the url to request OAuth credentials from Google
        login = GOOGLE_URL + '?' + 'response_type=code&' + \
                'client_id=' + CLIENT_ID +'&' + \
                'redirect_uri=' + REDIRECT_URI + '&' + \
                'scope=email&' + 'state=SuperSecret9000'
        print(login)
        template_vars = {"title": "Welcome to ABC Inc.",
                         "login": login}
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.out.write(template.render(template_vars))



class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template_vars = {"title": "About ABC Inc."}
        template = JINJA_ENVIRONMENT.get_template('about.html')
        self.response.out.write(template.render(template_vars))



class NotFoundHandler(webapp2.RequestHandler):
    def get(self):
        template_vars = {"title": "404 Not Found",
                         "url": "bad_url..."} # TODO have this post it's own url.
        template = JINJA_ENVIRONMENT.get_template('404_page_not_found.html')
        self.response.out.write(template.render(template_vars))



# Add patch as a http method.
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods


# Set http routes.
app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/index.html', MainHandler),
                               ('/about.html', AboutHandler),
                               ('/oauth', OauthHandler),
                               ('/.*', NotFoundHandler)],
                              debug=True)
    
