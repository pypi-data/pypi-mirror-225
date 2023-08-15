from django.db.models import Model
from django.forms import ModelForm
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from dashpro.models import ModelConfig

RELATIONAL_FIELDS = ['ManyToManyRel',]

class Action:
    
    def __init__(self,name,help_text):
        pass
    

class _default_form:
    def __init__(self, registry_model: Model, default_fields="__all__") -> None:
        class DefaultForm(ModelForm):
            class Meta:
                model = registry_model
                fields = default_fields

        self.form = DefaultForm

    def get_form(self) -> ModelForm:
        return self.form


class ModelAdmin:
    def __init__(
        self,
        model: Model,
        form=None,
        readonly_fields: list[str] = [],
        display_fields: list[str] = [],
        search_fields: list[str] = [],
    ) -> None:
        # Code
        if form is None:
            default_fields = []

            for field in model._meta.get_fields():
                if field.editable:
                    default_fields.append(field.name)

            form = _default_form(model, default_fields)

        if display_fields == []:
            display_fields = []
            
            for field in model._meta.get_fields():
                display_fields.append(field.name)
            
        
        self.form = form.get_form()
        self.readonly_fields = readonly_fields
        self.display_fields = display_fields
        self.search_fields = search_fields


class ModelUrlPattern:
    views = [
        {"view": "list", "pk_required": False},
        {"view": "create", "pk_required": False},
        {"view": "update", "pk_required": True},
        {"view": "detail", "pk_required": True},
        {"view": "delete", "pk_required": True},
    ]

    def __init__(self, model: Model) -> None:
        app_label = model._meta.app_label.lower()
        model_name = model._meta.model_name.lower()
        self.map = {}

        for view_object in self.views:
            pk = "<int:pk>/" if view_object.get("pk_required") == True else ""
            route = f'{app_label}/{model_name}/{view_object.get("view")}/' + pk
            view_name = f'{model_name}-{view_object.get("view")}'
            self.map[view_object.get("view")] = {"route": route, "view_name": view_name}

    def get_pattern_for_(self, view_name):
        assert {"view": view_name, "pk_required": True} in self.views or {
            "view": view_name,
            "pk_required": False,
        } in self.views

        return self.map.get(view_name)


class RegistryObject:
    def __init__(self, model: Model, admin: ModelAdmin) -> None:
        self.id = self.get_id(model)
        self.name = model._meta.model_name
        self.model = model
        self.admin = admin
        self.url_pattern = ModelUrlPattern(model)
        self.config = ModelConfig.objects.get_or_create(model=self.name)[0]
        
    @classmethod
    def get_id(self,model:Model):
        return model._meta.app_label + '_' + model._meta.model_name
    # Get model log entries { use this after the apps are  loaded }
    @property
    def logs(self):
        content_type = ContentType.objects.get_for_model(self.model)

        return LogEntry.objects.filter(content_type=content_type).all()


class Registry:
    def __init__(self) -> None:
        self._registry = []

    @property
    def get_registry(self):
        return self._registry

    @classmethod
    def get_registry_object(self, model):
        id = model._meta.app_label + "_" + model._meta.model_name

        for registry_object in self.get_registry:
            if registry_object.id == id:
                return registry_object

        return None

    def get_registry_object(self, model:Model) -> RegistryObject | None:
        id = RegistryObject.get_id(model)
        for object in self.get_registry:
            if object.id == id:
                return object
        
        return None

    def group_registry_by_apps(self):
        result = {}

        for object in self.get_registry:
            app_lable = object.model._meta.app_label.lower()

            if not result.get(app_lable):
                result[app_lable] = {"app": app_lable, "registry_objects": [object],"view_name":app_lable}
            else:
                result[app_lable]["registry_objects"].append(object)

        return result

    def register(self, registry_object: RegistryObject):
        if not registry_object in self.get_registry:
            self._registry.append(registry_object)


model_registry = Registry()
