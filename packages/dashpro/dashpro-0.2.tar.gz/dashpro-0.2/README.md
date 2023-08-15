# Dashpro: Django Dynamic Dashboard


Dashpro is a dynamic dashboard app for Django that enhances your data visualization experience with a modern and accessible user interface. It's designed to provide you with a comprehensive set of features to create interactive and insightful dashboards for your data analysis needs.

## Key Features

- **Enhanced UI**: Dashpro comes with a visually appealing and user-friendly interface, making it easy for users to interact with data.

- **Custom Actions**: Empower your users with custom actions, allowing them to perform specific tasks directly from the dashboard.

- **Custom Widgets**: Tailor your dashboard with custom widgets, providing flexibility to display various types of data in unique ways.

- **Data Analysis**: Conduct thorough data analysis using Dashpro's built-in tools, helping you uncover insights and patterns.

- **Accessibility**: Dashpro is designed with accessibility in mind, ensuring that your dashboards can be used by a wide range of users.

## Installation

Install Dashpro using pip:

1. install the app or from [github](https://github.com/ehusseinnaim/dashpro.git) 

```bash
pip install dashpro

```

2. add to ==INSTALLED_APPS== 

```python

INSTALLED_APPS = [
    # .... your apps
    "dashpro.apps.DashproConfig",
]

```

3. add context_processors 

```python

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            
            # You're templates 
            
            ],
        "APP_DIRS": True # make sure to enable APP_DIRS ,
        "OPTIONS": {
            "context_processors": [
                # Default context processors 

                "dashpro.context.global.registry"
            ],
        },
    },
]

```

4. add dashpro static files to ==STATICFILES_DIRS== 

```python

STATICFILES_DIRS = [
    # Your're static files 

    BASE_DIR / "dashpro/static"
]

```

5. run migrations 

```bash


python manage.py runserver

```

6. include dashpro urls 

```python

# Note : the login path is /login not /dashpro/login make sure to not change the login route


from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # Dashpro urls
    path("",include("dashpro.urls"))
] 


 ```


7. Register you models 

> RegistryObject 

a registry object  class  takes two arguments first. model:Model , second. admin:ModelAdmin to control you model display_fields,readonly_fields,search_fields ,etc.



```python

from dashpro.registry import RegistryObject 
from your_app.models import Post 

admin = None
registry_object = RegistryObject(Post)


```

> ModelAdmin

ModelAdmin class control your fields,forms,custom_actions,analysis pages ,etc 

```python

from dashpro.registry import RegistryObject 
from your_app.models import Post 

admin = ModelAdmin(Post,form=None,display_fields=[],readonly_fields=[],search_fields=[])
registry_object = RegistryObject(Post,admin=admin)


```


> model_registry : object

model_registry as the name says it's a models registry to register you models to create views , UI pages , actions , etec 

model_registry.register takes one argument which is registry_object

```python

from dashpro.registry import RegistryObject 
from your_app.models import Post 

admin = ModelAdmin(Post,form=None,display_fields=[],readonly_fields=[],search_fields=[])
registry_object = RegistryObject(Post,admin=admin)

model_registry.register(registry_object)

```

8. open your local host and you'll see this strucutre in the sidebar 


* your app name example: blog
    * the model your registered Post



# Join the Dashpro Project 

🌟 **Help me make it better** 🌟

Are you passionate about Django and data visualization? We invite you to be part of the **Dashpro** project!

## About Dashpro

**Dashpro** is a dynamic dashboard app for Django, designed to enhance data visualization experiences. As an individual contributor, I'm excited to welcome fellow developers to collaborate on this project.

## How You Can Contribute

No matter your level of experience, your contributions are valued! Here's how you can get involved:

- **Code Enhancements**: Add new features or enhance existing ones.
- **UI/UX**: Improve the user interface and overall user experience.
- **Testing**: Help ensure the app's functionality is robust and reliable.
- **Documentation**: Contribute clear and helpful documentation.

## Get Involved

- **GitHub Repository**: [https://github.com/ehusseinnaim/Dashpro.git](https://github.com/ehusseinnaim/Dashpro.git)
- **Clone the Repository**: `git clone https://github.com/ehusseinnaim/Dashpro.git`
- **Fork & Contribute**: Fork the repository, make changes, and submit pull requests!

Your contributions can make a significant impact on making **Dashpro** a more powerful and user-friendly tool.

Thank you for considering contributing to the project and being part of this journey!

**Hussein Naim**
