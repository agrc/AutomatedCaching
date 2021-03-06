from unittest import TestCase
from agrc.caching.commands import cache

class testCreateCacheSchemaCommand(TestCase):
    def test_schema_gets_default_values(self):
        command = cache.CreateCacheSchemaCommand("terrain")
        
        self.assertEqual(command.tile_origin, "-5120900 9998100", "orgin")
        self.assertEqual(command.tile_format, "JPEG", "format")
        self.assertEqual(command.tiling_scheme, "NEW", "scheme")
        self.assertEqual(command.scheme_type, "CUSTOM", "type")
        self.assertEqual(command.number_of_scales, 15, "# scales {0}".format(command.number_of_scales))
        self.assertEqual(command.dpi, "96", "dpi")
        self.assertEqual(command.tile_size, "256 x 256", "size")
        self.assertEqual(command.storage_format, "COMPACT", "s format")
        self.assertEqual(command.compression, 85, "compression")
        self.assertEqual(command.basemap, "terrain", "service")