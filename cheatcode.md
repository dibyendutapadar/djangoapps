
# Django Commands

# SETUP

## Start a New Project

```
django-admin startproject <projectname> .

```

#### Django myproject files

Here's a brief description of each file's purpose in a Django project:

| File | Description |
| -------- | ------- |
| manage.py | A command-line utility that lets you interact with your Django project. It's used for tasks like starting a server, creating apps, and running migrations. |
| project/__init__.py | An empty file that tells Python that the directory should be considered a Python package. |
| project/asgi.py | Provides a hook for ASGI-compatible web servers to serve your project. ASGI is the standard interface between web servers and async Python web apps or frameworks. |
| project/settings.py | Contains all the configuration for your Django project. This includes database configurations, security settings, and application-specific settings. |
| project/urls.py | Defines the URL declarations for your Django project; it's a table of contents for your Django-powered site. It tells Django how to route web requests to the appropriate view based on the request URL. |
| project/wsgi.py | Provides a hook for WSGI-compatible web servers to serve your project. WSGI is the standard interface between web servers and Python web applications or frameworks. |


### ASGI vs WSGI server

The main difference between WSGI (Web Server Gateway Interface) and ASGI (Asynchronous Server Gateway Interface) servers lies in their handling of synchronous and asynchronous code.

**WSGI (Web Server Gateway Interface):**
- **Synchronous:** WSGI is designed for synchronous processing. It handles one request at a time per process, which means it waits for a response to be ready before moving on to the next request. This can lead to inefficiencies when dealing with long I/O operations.
- **Standard:** It has been the standard interface between web servers and Python web applications or frameworks for many years. Most Python web frameworks (like Django and Flask) initially built their compatibility around WSGI.
- **Limitations:** The synchronous nature of WSGI makes it less suitable for real-time applications, long polling, or applications that require long-lived connections, such as WebSockets.

**ASGI (Asynchronous Server Gateway Interface):**
- **Asynchronous:** ASGI is designed to support asynchronous processing. It can handle multiple requests simultaneously, allowing for more efficient use of resources, especially for I/O-bound operations. This makes it well-suited for real-time applications, long polling, and WebSockets.
- **Newer Standard:** ASGI is a relatively newer standard compared to WSGI, designed to extend the capabilities of WSGI to include asynchronous processing as well as backwards compatibility with WSGI applications.
- **Flexibility:** ASGI supports both synchronous and asynchronous applications, giving developers the flexibility to choose the best approach based on their application's requirements.

In summary, the key difference is how they handle requests: WSGI is synchronous and processes requests one at a time, making it simpler but potentially less efficient for certain types of applications. ASGI is asynchronous, capable of handling multiple requests concurrently, which can lead to better performance for I/O-bound applications and enables support for WebSockets and other real-time features.

## Run Server

```
python3 manage.py runserver  
```


## create new app

```
python3 manage.py startapp <appname>
```

#### app files

| File | Description |
| -------- | ------- |
| app/ migrations/init.py |  An empty file that tells Python that the migrations directory should be considered a Python package. This is where migration files are stored, which are used to manage changes to the database schema.|
| app/init.py | An empty file that tells Python that the app directory should be considered a Python package. This is necessary for Python to recognize the app and its components. |
| app/admin.py | Used to register your app's models with the Django admin site. By registering your models, you make them accessible and manageable through the Django admin interface, allowing for easy creation, reading, updating, and deletion of records. |
| app/apps.py |  Contains the configuration for the app itself. This includes settings like the name of the app and can be used to configure app-specific behaviors. |
| app/models.py | Defines the data models for your application. A model is a Python class that defines the structure of an application's data, and translates that data into a database format. |
| app/views.py | Contains the views for your application. A view is a Python function or class that takes a web request and returns a web response. Views access the data needed to satisfy requests through models and delegate formatting to the templates.|
| app/tests.py | Contains test cases for your application. This file is used to write unit tests that can automatically test the functionality of your app's models, views, and other components to ensure they work as expected.|


# Views and urls

## views.py

on the views.py file under the app, create the functions for the view

each function would take a request.

```
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('Project Home')

```

## urls.py 

in the Project folder
1. import views
2. add the paths

or alternatively
you can add a urls.py file to the app folder
and direct the urls.py in project folder to import

#### project/urls.py

```
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name='index'), #this imports views from the project folder
    path('foodmenu/',include('foodmenu.urls')),
]
```

#### app/urls.py

```
from django.urls import path
from . import views

urlpatterns =[
    path('',views.index,name='index'),
    path('items',views.items,name='items')
]

```

# Models and Databases

## migrate

all the apps listed under INSTALLED_APPS =[], in project/settings.py are migrated

```
python3 manage.py migrate

```


## app/models.py

Define models (db.tables) here as class
this will be migrated and tables will be created based on these classes

```
class Item(models.Model):
    item_name=models.CharField(max_length=200)
    item_desc=models.CharField(max_length=200)
    item_price=models.IntegerField()

    def __str__(self):
        return(self.Item_name)
```

show string represenetation of of the model.

Defining a model means we have a blueprint for table called as Item

Don't forget to add the app in settings
<name>.app.<class name>

this are available in the application/app.py file

```
INSTALLED_APPS = [
    'foodmenu.apps.FoodmenuConfig',
    ...
    ]
```

inform django that you need to make changes to db
```
python3 manage.py makemigrations <appname>
```

and run migrate
```
python3 manage.py migrate
```


## superuser
```
python manage.py createsuperuser
```

## register app/model in app/admin.py to access from /admin

```
from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Item)
```

## manage.py shell

```
python3 manage.py shell

from app.models import modelName

>>> modelName.objects.all()
>>> a = modelName(field="value",field="value")
>>> a.save
>>> a.id
>>> a.pk

```

## Fetch data from db
```
from django.shortcuts import render
from django.http import HttpResponse
from .models import Item

# Create your views here.
def index(request):
    return HttpResponse('FoodApp')


def items(request):
    item_list = Item.objects.all()
    return HttpResponse(item_list)
```

# templates

- add new folder templates inside the app folder
- create the html file

- send context to the html file
```
from django.shortcuts import render
from django.http import HttpResponse
from .models import Item

def items(request):
    item_list = Item.objects.all()
    context={
        'item_list':item_list,
    }
    return render(request,'items.html',context)
```


#### get from model
```
#views.py
def item_detail(request,item_id):
    item=Item.objects.get(pk=item_id)
    context={
        'item':item,
    }
    return render(request,'item_detail.html',context)

#urls.py
path('<int:item_id>/',views.item_detail,name='item_detail')
```