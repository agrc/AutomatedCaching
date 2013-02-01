from unittest import TestCase
from agrc.caching import models

class testModels(TestCase):
    def test_cachejob_updatemode_defaults_to_all(self):
        job = models.CacheJob()
        
        self.assertEqual(job.update_mode, "RECREATE_ALL_TILES", "enum not working correctly")