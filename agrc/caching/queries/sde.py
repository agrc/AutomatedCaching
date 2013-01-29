from agrc.caching.abstraction.base import Command

class AreasOfChangeQuery(Command):
    def execute(self):
        # query sde get new changes
        return _querySdeForAreasOfChange()
    
    def _querySdeForAreasOfChange(self):
        pass
