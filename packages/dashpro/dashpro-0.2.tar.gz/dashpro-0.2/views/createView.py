from dashpro.registry import RegistryObject


def _create_view(registry_object:RegistryObject,**kwargs) -> None:
    
    from django.views.generic import CreateView
    from dashpro.registry import url_registry
    from django.urls import path
    
    _queryset = registry_object.model.objects.all()
    _model = registry_object.model
    _form_class = registry_object.admin.form
    _template_name = kwargs.get("template_name",'views/create.html')
    _success_url = kwargs.get("success_url","/")
    _app = _model._meta.app_label
    _route = f'{_app}/{_model._meta.model_name.lower()}/create/'
    _view_name = kwargs.get("view_name",_model._meta.model_name.lower() + '-create')
    
    class ModelCreateView(CreateView):
        queryset = _queryset
        model = _model
        form_class = _form_class
        template_name = _template_name
        success_url = _success_url
    
    url_registry.register(path(_route,ModelCreateView.as_view(),name=_view_name))
    
    
    

