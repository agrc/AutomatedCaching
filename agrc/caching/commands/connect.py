from agrc.caching.abstraction.base import Command
from agrc.caching.config import Server
import requests
import ConfigParser
import os

class GetTokenCommand(Command):
    section = "ArcGIS Admin Credentials"
    _server = None
    
    def __init__(self, server = Server()):
        self._server = server
    
    def execute(self):      
        token_url = self._server.get_token_url()
        
        credentials = self._get_arcgis_credentials()
          
        payload = {
                   'username': credentials[0], 
                   'password': credentials[1],
                   'f': 'json'
        }
        
        r = requests.post(token_url, data = payload)
        
        print r.text
        
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        
        response = r.json()
        
        return response['token']
    
    def _get_arcgis_credentials(self):
        config = ConfigParser.RawConfigParser()
        
        file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", 'secrets.cfg')
        
        print file
        
        config.read(file)
        
        user = config.get(self.section, "username")
        password = config.get(self.section, "password")
        
        return user, password

class GetServiceStatisticsCommand(Command):
    service_name = None
    token = None
    _server = None
      
    def __init__(self, service_name, token, server = Server()):
        self._server = server
        self.service_name = service_name
        self.token = token
    
    def execute(self):
        url = self._server.get_statistics_url(self.service_name)
        
        payload = {
                   "token": self.token,
                   'f': 'json' 
                   }
        
        r = requests.get(url, params = payload)
        
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        
        return r.json()     