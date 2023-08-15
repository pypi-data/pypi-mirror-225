from dashpro.registry.model_registry import RegistryObject
from django.db.models import Model


class RegistryObjectUtils:
    
    def __init__(self,registry_object:RegistryObject) -> None:
        self.object = registry_object
    
    
    def table_headers(self):
        return self.object.admin.display_fields
    
    
    @classmethod
    def get_values(self,model:Model):
        values = []
        
        for field in self.object.admin.display_fields:
            if hasattr(model,field):
                values.append(getattr(model,field))

        return values
