from unittest import TestCase
from agrc.caching.models import AreaOfChange
from agrc.caching.commands import dto

class TestDto(TestCase):
    def testFourCacheJobsCreatedForDifferentScaleGroupsOfSameLayer(self):
        """scale groups are groups of levels
                Groups
                    0-2
                    3-4
                    5-12
                    12-14
            They each use a different extent for which to cache within.
        """
        
        changes = []
        changes.append(AreaOfChange([0,1,2], "a"))
        changes.append(AreaOfChange([2,3,4], "b"))
        changes.append(AreaOfChange([3,4], "c"))
        
        command = dto.GetCacheJobFromAreaOfChangeCommand(changes)
        jobs = command.execute()
        
        self.assertIsNotNone(jobs, "jobs are empty")
        self.assertEqual(4, len(jobs), "incorrect amount of jobs from changes {0}".format(len(jobs)))        
        self.assertTrue(any(x.service_name == "a" and 0 in x.levels and 1 in x.levels and 2 in x.levels for x in jobs))
        self.assertTrue(any(x.service_name == "c" and 3 in x.levels and 4 in x.levels for x in jobs))