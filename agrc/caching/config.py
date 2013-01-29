class Server(object):
	tokenEndpoint = "http{0}://{1}{3}/{2}/tokens/generateToken"
	useHttps = False
	usePort = False
	defaultInstance = "arcgis"
	serverName = "localhost"
	port = "6080"
	
	def getTokenUrl(self, server=None):
		https = ""
		if self.useHttps:
			https = "s"
			
		if server is None:
			server = self.serverName
			
		port = ""
		if self.usePort:
			port = ":{0}".format(self.port) 
		
		return self.tokenEndpoint.format(https, server, self.defaultInstance, port)