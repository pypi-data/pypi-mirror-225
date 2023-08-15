from dashpro.registry import model_registry,url_registry
from django.shortcuts import render
from django.views import View
from .listView import _list_view
from .createView import _create_view
from .updateView import _update_view
from .detailView import _detail_view
from .deleteView import _delete_view

from django.urls import path




def _views() -> None:
    if __name__ == 'dashpro.views':
        for app,data in model_registry.group_registry_by_apps().items():
            class AppView(View):
                def get(self,request):
                    context = {
                        "app":app,
                        "data":data
                    }
                    template = "views/app.html"
                    return render(request,template,context)
            
            url_registry.register(path(app+'/',AppView.as_view(),name=app))

            # model's views 
            for registry_object in data.get("registry_objects"):
                _list_view(registry_object)
                _create_view(registry_object)
                _update_view(registry_object)
                _detail_view(registry_object)
                _delete_view(registry_object)



_views()







