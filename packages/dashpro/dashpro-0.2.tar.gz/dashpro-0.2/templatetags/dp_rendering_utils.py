from django import template
from dashpro.utils import RegistryObjectUtils
from dashpro.registry import (model_registry,RELATIONAL_FIELDS)
from django.db.models import Model,ManyToManyRel


register = template.Library()


@register.simple_tag
def get_registry_object(model):
    return model_registry.get_registry_object(model)

@register.simple_tag
def get_view(model):
    
    get_registry_object(model).url_pattern.map


@register.simple_tag
def get_values(object,fields:list[str]):
    values = []
    
    for field in fields:
        try:
            if not field == 'id':
                values.append(getattr(object,field))
        except AttributeError:
            #!TODO 
            # get relation fields values 
            values.append("#TODO m2m field rendering")
            
    return values