from agrc.caching.abstraction.base import Command
from agrc.caching.config import Server
import requests
import ConfigParser
import os

class GetTokenCommand(Command):
    section = "ArcGIS Admin Credentials"
    
    def execute(self):
        server = Server(use_port = True)
        
        token_url = server.get_token_url()
        
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
    service_name = ""
        
    def __init__(self, service_name):
        self.service_name = service_name
    
    def execute(self):
        server = Server()  
        server.usePort = True
        
        url = server.get_statistics_url(self.service_name)
        
        return url  
    