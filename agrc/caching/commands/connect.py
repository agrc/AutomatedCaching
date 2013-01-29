from agrc.caching.abstraction.base import Command
from agrc.caching.config import Server
import requests

class GetTokenCommand(Command):
    def execute(self):
        server = Server()
        server.usePort = True
        
        tokenUrl = server.getTokenUrl()
        
        payload = {
                   'username': '', 
                   'password': '',
                   'f': 'json'
        }
        
        r = requests.post(tokenUrl, data = payload)
        
        print r.text
        
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        
        response = r.json()
        
        return response['token']