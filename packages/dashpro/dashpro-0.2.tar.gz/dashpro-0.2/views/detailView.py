from dashpro.registry import RegistryObject


def _detail_view(registry_object:RegistryObject,**kwargs) -> None:
    
    from django.views.generic import DetailView
    from django.http import (HttpRequest,HttpResponse)
    from django.shortcuts import render
    from typing import Any
    from dashpro.registry import url_registry
    from django.urls import path
    
    _model = registry_object.model
    _context_object_name = kwargs.get("context_object_name","object")
    _template_name = kwargs.get("template_name",'views/detail/detail.html')
    _app = _model._meta.app_label
    _route = f'{_app}/{_model._meta.model_name.lower()}/detail/<int:pk>/'
    _view_name = kwargs.get("view_name",_model._meta.model_name.lower() + '-detail')
    
    class _View(DetailView):
        model = _model
        template_name = _template_name
        context_object_name = _context_object_name
        
        def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
            obj = self.model.objects.filter(pk=kwargs.get("pk"))

            if obj.exists():
                obj = obj[0]
                
                context = {
                    "object":obj
                }
                
                return render(request,self.template_name,context)
                
            
            return HttpResponse("Not found ")
        
        def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
            
            form = self.form_class(request.POST,files=request.FILES)
            context = {
                "form":form
            }
            
            if form.is_valid():
                form.save()

                context["detaild"] = True
            

            return render(request,self.template_name,context)
            
    
    url_registry.register(path(_route,_View.as_view(),name=_view_name))
    
    
    

