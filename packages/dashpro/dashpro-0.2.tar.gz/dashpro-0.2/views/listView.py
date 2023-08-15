from typing import Any, Dict
from dashpro.registry import RegistryObject,model_registry


def _list_view(registry_object: RegistryObject, **kwargs) -> None:
    from django.views.generic import ListView
    from dashpro.registry import url_registry
    from django.urls import path

    _queryset = registry_object.model.objects.all()
    _context_object_name = kwargs.get("context_object_name", "objects")
    _model = registry_object.model
    _template_name = kwargs.get("template_name", "views/list/list.html")
    _app = _model._meta.app_label
    _url_config = registry_object.url_pattern.get_pattern_for_("list")
    _view_name = _url_config.get("view_name")
    _route = _url_config.get("route")

    class _View(ListView):
        queryset = _queryset
        model = _model
        template_name = _template_name
        context_object_name = _context_object_name
        paginate_by = 10
        
        def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
            context = super().get_context_data(**kwargs)
            context['registry_object'] = model_registry.get_registry_object(self.model)
            context['views'] = model_registry.get_registry_object(self.model).url_pattern.map
            context['page_title'] = f'{self.model._meta.model_name} - list objects'

            return context
            
    url_registry.register(path(_route, _View.as_view(), name=_view_name))
