from unittest import TestCase
from agrc.caching import models
from nose.tools import nottest

@nottest 
class TestModels(TestCase):
    def test_get_scales_from_level(self):
        job = models.CacheJob()