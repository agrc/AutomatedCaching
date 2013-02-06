from unittest import TestCase
from agrc.caching.commands import scales
from nose.tools import nottest

@nottest 
class TestScales(TestCase):
    def test_get_scales(self):
        command = scales.GetUtmScaleFromLevelCommand()
        command.levels = [0]
        
        result = command.execute()
        
        self.assertEqual(result, "18489297.737236")
        
        command.levels = [0,1,2]
        result = command.execute()
        
        self.assertEqual(result, "18489297.737236;9244648.868618;4622324.434309")