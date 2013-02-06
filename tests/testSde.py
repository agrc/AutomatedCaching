from agrc.caching.queries import sde
from unittest import TestCase
from nose.tools import nottest

@nottest 
class TestConnect(TestCase):
    def test_command_can_connect_to_file_gdb(self):
        query = sde.AreasOfChangeQuery()
        result = query.execute()
        
        self.assertIsNotNone(result, "query is broken")
        self.assertEqual(len(result), 1, "no areas of change")
    
    