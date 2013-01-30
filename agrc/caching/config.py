class Server(object):
	_baseurl_format = "http{0}://{1}{2}/{3}/"
	_baseurl = None
	_token_url = "{0}tokens/generateToken"
	_stats_url = "{0}admin/services/System/{1}/statistics"
	
	_use_https = False
	_use_port = False
	_instance = None
	_server = None
	_port = None
	
	def __init__(self, server_name = "localhost", instance_name = "arcgis", use_https = False, use_port = False, port = "6080"):
		self._use_https = use_https
		self._use_port = use_port
		self._instance = instance_name
		self._server = server_name
		self._port = port
		
		self._baseurl = self._format_base_url()
	
	def get_token_url(self):
		return self._token_url.format(self._baseurl)
	
	def get_statistics_url(self, service):
		return self._stats_url.format(self._baseurl, service)
	
	def _format_base_url(self):
		https = ""
		if self._use_https:
			https = "s"
			
		port = ""
		if self._use_port:
			port = ":{0}".format(self._port) 
		
		return self._baseurl_format.format(https, self._server, port, self._instance)