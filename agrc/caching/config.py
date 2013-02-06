from os import path

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
	
class BaseMap(object):
	def get_low_quality(self):
		return 68

	def get_high_quality(self):
		return 85

	def get_compression_level(self, service_name):
		service_name = service_name.upper()
		
		if "TERRAIN" in service_name:
			return self.terrain
		if "LITE" in service_name:
			return self.lite
		if "HYBRID" in service_name:
			return self.hybrid
		if "VECTOR" in service_name:
			return self.vector
		if "HILLSHADE" in service_name:
			return self.hillshade
		if "IMAGERY" in service_name:
			return self.imagery
		if "TOPO" in service_name:
			return self.topo		 

	terrain = property(get_high_quality, None)
	lite = property(get_high_quality, None)
	hybrid = property(get_high_quality, None)
	vector = property(get_high_quality, None)
	hillshade = property(get_high_quality, None)
	imagery = property(get_low_quality, None)
	topo = property(get_high_quality, None)
	
class Scales(object):
	#: the mapping betten the cache level and the utm scale
	_level_scale_map = { 
        0: '18489297.737236',
        1: '9244648.868618',
        2: '4622324.434309',
        3: '2311162.217155',
        4: '1155581.108577',
        5: '577790.554289',
        6: '288895.277144',
        7: '144447.638572',
        8: '72223.819286',
        9: '36111.909643',
        10: '18055.954822',
        11: '9027.977411',
        12: '4513.988705',
        13: '2256.994353',
        14: '1128.497176'
    }
	
	def get_scales(self):
		return self._level_scale_map
	
	def _get_scale_count(self):
		return len(self._level_scale_map)
	
	scale_map = property(get_scales, None)
	scale_count = property(_get_scale_count, None)

class Geodatabase(object):
	#: the path to where the py script is running
	base_path = path.join(path.abspath(path.dirname(__file__)), "..\..", "data")
	
	#: the path to where the gdb is sitting - will need to modify this for sde probably
	path = "\AreasOfChange.gdb"
	
	#: the name of the feature class for changes
	change_feature_class = "AreasOfChange"
	
	#: the name of the feature class for caching jobs
	job_feature_class = "CacheJob"