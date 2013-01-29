from agrc.caching.abstraction.base import Command
from agrc.caching.config import Server
import requests
import ConfigParser
import os

class GetTokenCommand(Command):
    section = "ArcGIS Admin Credentials"
    
    def execute(self):
        server = Server()
        server.usePort = True
        
        tokenUrl = server.getTokenUrl()
        
        credentials = self._getArcGisCredentials()
          
        payload = {
                   'username': credentials[0], 
                   'password': credentials[1],
                   'f': 'json'
        }
        
        r = requests.post(tokenUrl, data = payload)
        
        print r.text
        
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        
        response = r.json()
        
        return response['token']
    
    def _getArcGisCredentials(self):
        config = ConfigParser.RawConfigParser()
        
        file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", 'secrets.cfg')
        
        print file
        
        config.read(file)
        
        user = config.get(self.section, "username")
        password = config.get(self.section, "password")
        
        return user, password