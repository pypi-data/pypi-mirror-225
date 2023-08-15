
class DictToObject:
    
    def __init__(self,dict:dict) -> None:
        for key,value in dict.items():
            setattr(self,key,value)



class Registry:
    
    """URL's  Registry
    
    a urls registry returns a list of URLResolver objects
    
    """
    
    def __init__(self) -> None:
        self._registry = []
        
    
    @property
    def get_registry(self) -> list:
        
        return self._registry
    
    def register(self,path):
        
        if not path in self.get_registry:
            self._registry.append(path)

class DashProRegistry:
    """ DashProRegistry
    
    This registry is only for DashPro custom views \n
    please do not use it this may occurce a bug in your project     
    """


url_registry = Registry()

