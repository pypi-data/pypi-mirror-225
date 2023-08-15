from dashpro.registry import RegistryObject


def _delete_view(registry_object:RegistryObject,**kwargs) -> None:
    
    from django.views.generic import DeleteView
    from django.http import (HttpRequest,HttpResponse)
    from django.shortcuts import render
    from typing import Any
    from dashpro.registry import url_registry
    from django.urls import path
    
    _queryset = registry_object.model.objects.all()
    _model = registry_object.model
    _form_class = registry_object.admin.form
    _template_name = kwargs.get("template_name",'views/delete.html')
    _success_url = kwargs.get("success_url","/")
    _app = _model._meta.app_label
    _route = f'{_app}/{_model._meta.model_name.lower()}/delete/<int:pk>/'
    _view_name = kwargs.get("view_name",_model._meta.model_name.lower() + '-delete')
    
    class _View(DeleteView):
        queryset = _queryset
        model = _model
        form_class = _form_class
        template_name = _template_name
        success_url = _success_url
        def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
            obj = self.model.objects.filter(pk=kwargs.get("pk"))
            
            if obj.exists():
                obj = obj[0]
                
                context = {
                    "form":self.form_class(instance=obj)
                }
                
                return render(request,self.template_name,context)
                
            
            return HttpResponse("Not found ")
    
    url_registry.register(path(_route,_View.as_view(),name=_view_name))
    
    
    

