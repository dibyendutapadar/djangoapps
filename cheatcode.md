
1. Django Commands
2. SETUP
   1. Start a New Project
         1. Django myproject files
      1. ASGI vs WSGI server
   2. Run Server
3. create new app
         1. app files
   1. register app in settings.py
4. Views and urls
   1. views.py
   2. urls.py
         1. project/urls.py
         2. app/urls.py
5. Models and Databases
   1. migrate
   2. app/models.py
   3. superuser
   4. register app/model in app/admin.py to access from /admin
   5. manage.py shell
   6. Fetch data from db
6. templates
         1. get from model
7. Static Files
      1. Step 1: Configure Your Project for Static Files
      2. Step 2: Use Static Files in Your Templates
      3. Step 3: Organizing Static Files
      4. Step 4: Collecting Static Files
      5. Step 5: Serving Static Files in Development
      6. Step 6: Serving Static Files in Production
      7. Conclusion
8. Forms
      1. Step 1: Creating a Form
      2. Step 2: Displaying a Form in a View
      3. Step 3: Rendering the Form in a Template
      4. Step 4: Handling Submitted Form Data
      5. Step 5: Customizing Form Validation
      6. Step 1: Define Your Model
      7. Step 2: Create a ModelForm
      8. Step 3: Use the Form in a View
      9. Step 4: Render the Form in a Template
9. User Upload media/image files
      1. Step 1: Update Django Settings
      2. Step 2: Create a Django Model for File Uploads
      3. Step 3: Create a Form for File Upload
      4. Step 4: Create a View to Handle Uploads
      5. Step 5: Create a Template for the Upload Form
      6. Step 6: Configure URLs
      7. Step 7: Serve Media Files During Development
      8. Step 8: Testing
10. Django Rest Framework
       1. Step 1: Install Django Rest Framework
       2. Step 2: Add DRF to Your Installed Apps
       3. Step 3: Create a Model
       4. Step 4: Create a Serializer
       5. Step 5: Create a View
       6. Step 6: Register with a Router
       7. Step 7: Run Your Server
       8. Conclusion
11. End points in APIs
       1. Step 1: Create a New Model
       2. Step 2: Create Serializers
       3. Step 3: Update Views
       4. Step 4: Update URL Router
       5. Step 5: Test Your API
       6. Conclusion
12. POST API
       1. Step 1: Define Your Model
       2. Step 2: Create a Serializer
       3. Step 3: Update Your View to Handle Parameters
       4. Step 4: Accepting Parameters from the Frontend
       5. Step 5: Handling Data in the Request Body
       6. Step 6: Testing
       7. Conclusion
13. User Registration
       1. Step 1: Configure Django's Authentication System
       2. Step 2: Create a User Registration Form
       3. Step 3: Create Views for Registration and Login
       4. Step 4: Configure URLs
       5. Step 5: Create Templates for Registration and Login
       6. Step 6: Handling User Sessions
       7. Conclusion
14. decouple config secret keys
       1. Step 1: Install `python-decouple`
       2. Step 2: Create a `.env` File
       3. Step 3: Configure `settings.py`
       4. Step 4: Access Configuration Variables
       5. Step 5: Managing Different Environments
       6. Conclusion



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


# create new app

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


## register app in settings.py
```python
INSTALLED_APPS = [
    'foodmenu.apps.FoodmenuConfig',
    ...
    ]
```


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
```python
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
```python
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
```python
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



# Static Files

Managing static files (CSS, JavaScript, images) in Django is a crucial part of developing web applications to ensure they are accessible in your templates. Django provides a robust system for handling these files. This tutorial will guide you through the process of setting up and using static files in a Django project.

### Step 1: Configure Your Project for Static Files

Django comes with a default configuration for static files. You may need to add or update these settings in your `settings.py` file to suit your project's needs:

```python
# settings.py

# Base directory where static files are collected
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# URL to use when referring to static files located in STATIC_ROOT
STATIC_URL = '/static/'

# Optional: specify additional directories where Django will search for static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'myapp/static'),
]
```

- `STATIC_ROOT` is the directory where static files will be stored after running `collectstatic` command.
- `STATIC_URL` is the URL to use when referring to static files.
- `STATICFILES_DIRS` is a list of filesystem directories to check when loading static files; it's optional and used for additional directories outside of your apps.

### Step 2: Use Static Files in Your Templates

To use static files in your templates, you'll need to load Django's static files template tag library at the top of your template file:

```html
{% load static %}
```

Then, use the `{% static %}` template tag to generate the correct URL for a given static file:

```html
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/script.js' %}"></script>
<img src="{% static 'images/logo.png' %}" alt="Logo">
```

Replace `'css/style.css'`, `'js/script.js'`, and `'images/logo.png'` with the correct paths to your static files within your static directories.

### Step 3: Organizing Static Files

It's a good practice to organize your static files within each Django app by creating a `static` directory. For instance, if your app's name is `myapp`, the directory structure should look like this:

```
myapp/
    static/
        myapp/
            css/
                style.css
            js/
                script.js
            images/
                logo.png
```

This organization ensures that static files are correctly namespaced by app, which prevents name clashes when collecting static files from different apps.

### Step 4: Collecting Static Files

Before deploying your Django project, you need to collect all of your static files into the `STATIC_ROOT` directory. This can be achieved by running the `collectstatic` management command:

```sh
python manage.py collectstatic
```

This command copies static files from your apps and other directories into the `STATIC_ROOT` directory.

### Step 5: Serving Static Files in Development

During development, Django automatically serves static files found in each of your application's `static` directories and the directories specified in `STATICFILES_DIRS` when you use the `runserver` command.

### Step 6: Serving Static Files in Production

For production environments, Django does not serve static files itself; it must be configured in your web server (e.g., Nginx, Apache). A common approach is to configure your web server to serve files from your `STATIC_ROOT` directory at the `STATIC_URL` path.

### Conclusion

Managing static files is essential for adding CSS, JavaScript, and images to your Django web applications. By following the steps outlined in this tutorial, you'll be able to correctly configure your Django project to handle static files both in development and in production environments. Remember, the key to efficiently managing static files in Django lies in understanding the settings and organizing files within your project's structure.


# Forms
Django forms provide a powerful and flexible way to generate forms for data input and validation. They handle the rendering of HTML forms, the reception of form data, and the validation of that data. Here's a short tutorial on how to use Django forms:

### Step 1: Creating a Form

First, you need to define a form. You can create a form by creating a class that inherits from `django.forms.Form` or `django.forms.ModelForm`. The former is used for forms that are not directly tied to models, while the latter is used for forms that are directly linked to models for creating or updating instances.

**Example of a simple form:**

```python
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
```

### Step 2: Displaying a Form in a View

To display a form, you need to create a view that renders the form. This view should instantiate your form class and pass it to a template.

**Example view:**

```python
from django.shortcuts import render
from .forms import ContactForm

def contact_view(request):
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            # For example, send an email or save the data
            pass

    return render(request, 'contact.html', {'form': form})
```

### Step 3: Rendering the Form in a Template

To render the form in a template, you can use the `{{ form.as_p }}` method, which wraps each field in paragraph tags. There are other methods like `{{ form.as_table }}` and `{{ form.as_ul }}` depending on how you want to structure your form in HTML.

**Example template (contact.html):**

```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Send</button>
</form>
```

### Step 4: Handling Submitted Form Data

After the form is submitted, you should check if it is valid in your view by calling `form.is_valid()`. This method performs all the validations for your fields. If the form is valid, you can then process the cleaned data.

**Example processing in a view:**

```python
if request.method == 'POST':
    form = ContactForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        # Process the data, such as sending an email
```

### Step 5: Customizing Form Validation

You can add custom validation to your form fields by defining clean_<fieldname>() methods in your form class.

**Example of custom validation:**

```python
class ContactForm(forms.Form):
    ...
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if "example.com" not in email:
            raise forms.ValidationError("Please use a valid 'example.com' email address")
        return email
```

This tutorial covers the basics of Django forms, including creating a form, displaying it in a view, rendering it in a template, handling submitted form data, and adding custom validation. Django's form system is highly extensible, allowing for more complex scenarios and interactions.



Yes, you can create a form from an existing model in Django by using `ModelForm`. A `ModelForm` is a convenient way to create a form that is directly tied to a model. It automatically generates form fields for the model fields specified, handles form validation, and can save the form data back to the database. Here’s how you can do it:

### Step 1: Define Your Model

First, ensure you have a model from which you want to create a form. For example, consider a simple `Book` model:

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pages = models.IntegerField()
    publish_date = models.DateField()
```

### Step 2: Create a ModelForm

Next, create a `ModelForm` for the `Book` model. In your app's `forms.py`, import your model and `ModelForm`, then define a class that inherits from `ModelForm`:

```python
from django.forms import ModelForm
from .models import Book

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'pages', 'publish_date']
        # You can also exclude some fields if you want
        # exclude = ['publish_date']
```

The `Meta` class inside your form class tells Django which model should be used to create the form (`model = Book`). You can specify which fields you want to include in your form with the `fields` attribute or which fields you want to exclude with the `exclude` attribute.

### Step 3: Use the Form in a View

In your views, you can instantiate your `BookForm` with no parameters to create a blank form or pass in an instance of the `Book` model to populate the form with existing data. Here's how you might use the form in a view for creating and updating a book:

```python
from django.shortcuts import render, redirect
from .forms import BookForm

# View to create a new book
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form})

# View to edit an existing book
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'book_form.html', {'form': form})
```

### Step 4: Render the Form in a Template

Finally, you can render the form in a template as you would with a regular `Form`:

```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
</form>
```

This method simplifies the process of creating forms for data entry and editing, as it automatically generates the appropriate form fields and handles validation based on your model's definition.


# User Upload media/image files


Creating a feature in your Django application that allows users to upload files (such as media, images, and documents) and store them efficiently involves several steps. This tutorial assumes you have a basic Django project set up. If not, refer to the Django documentation to create one. Let's get started:

### Step 1: Update Django Settings

First, configure your Django settings to handle media files:

1. In your `settings.py` file, add or update the following settings:

```python
# settings.py

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

- `MEDIA_URL` is the URL that serves the media files.
- `MEDIA_ROOT` is the filesystem path where these files are stored.

### Step 2: Create a Django Model for File Uploads

Define a model that includes a `FileField` (or `ImageField` for images) to handle file uploads:

1. Create a new app if you haven't already (`python manage.py startapp uploads`).
2. Define a model with a file field:

```python
# uploads/models.py

from django.db import models

class UploadedFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
```

- `upload_to` specifies a subdirectory of `MEDIA_ROOT` for storing the files.

### Step 3: Create a Form for File Upload

Create a Django form to handle the file upload:

```python
# uploads/forms.py

from django import forms
from .models import UploadedFile

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ('title', 'file',)
```

### Step 4: Create a View to Handle Uploads

Implement a view that processes the file upload form:

```python
# uploads/views.py

from django.shortcuts import render
from .forms import FileUploadForm

def file_upload_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Redirect to a new URL
    else:
        form = FileUploadForm()
    return render(request, 'uploads/file_upload_form.html', {'form': form})
```

### Step 5: Create a Template for the Upload Form

Create an HTML template for the form:

```html
<!-- templates/uploads/file_upload_form.html -->

<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Upload</button>
</form>
```

- The `enctype="multipart/form-data"` attribute is crucial for file upload to work.

### Step 6: Configure URLs

Set up a URL pattern for the upload view:

```python
# urls.py (project or app level)

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.file_upload_view, name='file_upload'),
]
```

### Step 7: Serve Media Files During Development

During development, you'll want Django to serve media files:

1. Update your project's main `urls.py` to include media URL configurations:

```python
# urls.py (project level)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your url patterns
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Step 8: Testing

Run your Django project and navigate to the `/upload/` URL to see the upload form. After uploading a file, it should be stored in the `media/uploads/` directory within your project.

Remember, serving media files with Django in a production environment requires additional configuration, such as using a dedicated web server (e.g., Nginx) to serve media files. This setup ensures efficient handling of static and media files and better performance of your Django application.



# Django Rest Framework

Django Rest Framework (DRF) is a powerful and flexible toolkit for building Web APIs in Django. It simplifies the process of creating RESTful web services with Django by providing a range of tools and functionalities. This tutorial assumes you have Django installed and a basic project set up. If not, refer to the Django documentation to get started. Let's dive into creating a simple API using Django Rest Framework.

### Step 1: Install Django Rest Framework

First, you need to install Django Rest Framework. You can do this using pip:

```sh
pip install djangorestframework
```

### Step 2: Add DRF to Your Installed Apps

Open your `settings.py` file and add `'rest_framework'` to your `INSTALLED_APPS` list:

```python
# settings.py

INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

### Step 3: Create a Model

For this tutorial, let's create a simple `Item` model in one of your apps (create an app if you haven't already with `python manage.py startapp myapp`).

```python
# myapp/models.py

from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name
```

Don't forget to migrate your changes:

```sh
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create a Serializer

Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into JSON, XML, or other content types. Create a file named `serializers.py` in your app directory and define a serializer for the `Item` model.

```python
# myapp/serializers.py

from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price']
```

### Step 5: Create a View

DRF provides several views that you can use to create a CRUD API. Here, we'll use the `ModelViewSet` for simplicity as it automatically provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.

```python
# myapp/views.py

from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
```

### Step 6: Register with a Router

DRF routers provide an easy way of automatically determining the URL conf for your API.

Update your app's `urls.py` (or create one inside your app if it doesn't exist) to include the viewset's routes:

```python
# myapp/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

And then include this `urls.py` in your project's main `urls.py`:

```python
# project's urls.py

from django.urls import path, include

urlpatterns = [
    path('api/', include('myapp.urls')),
]
```

### Step 7: Run Your Server

Start the Django development server:

```sh
python manage.py runserver
```

Navigate to `http://localhost:8000/api/items/` to see your API in action. You can use tools like Postman or Curl to test the API endpoints for creating, retrieving, updating, and deleting items.

### Conclusion

You've just created a simple CRUD API using Django Rest Framework. DRF offers a lot of powerful features like authentication, permissions, pagination, and more to build complex web APIs. Explore the [official DRF documentation](https://www.django-rest-framework.org/) for more advanced features and best practices.


# End points in APIs
Handling multiple endpoints in a Django Rest Framework (DRF) API involves organizing your viewsets and routers to accommodate different resources in your application. In the context of our previous tutorial, let's expand the API to include a new `Category` model, which will relate to the `Item` model. This demonstrates how to work with multiple models and endpoints.

### Step 1: Create a New Model

Let's add a `Category` model that our `Item` model can relate to. Update your models in `myapp/models.py`:

```python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
```

Don't forget to migrate your changes:

```sh
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Create Serializers

Create serializers for both `Category` and `Item`. Update or create a `serializers.py` in your app directory:

```python
from rest_framework import serializers
from .models import Item, Category

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price', 'category']

class CategorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'items']
```

### Step 3: Update Views

Create viewsets for both `Category` and `Item`. Update or create a `views.py` in your app directory:

```python
from rest_framework import viewsets
from .models import Item, Category
from .serializers import ItemSerializer, CategorySerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
```

### Step 4: Update URL Router

DRF routers allow you to easily manage multiple endpoints. Update your `urls.py` to register new routes for `Category`:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

### Step 5: Test Your API

Run your Django development server:

```sh
python manage.py runserver
```

You now have endpoints for both items and categories:

- Categories: `http://localhost:8000/api/categories/`
- Items: `http://localhost:8000/api/items/`

These endpoints support CRUD operations. For example, you can create a new category through the `/api/categories/` endpoint and then associate items with that category using the `/api/items/` endpoint.

### Conclusion

By following these steps, you've expanded your Django Rest Framework API to handle multiple models and endpoints. This structure is scalable and can be extended to include as many resources and relationships as your application requires. As your API grows, consider using nested routers (with the help of third-party packages like `drf-nested-routers`) for more complex data relationships and endpoint structures. Always refer to the [official DRF documentation](https://www.django-rest-framework.org/) for best practices and additional functionalities.


# POST API
Handling cases where the frontend sends parameters with the API request for the backend to consume and potentially add to the database is a common scenario in web development. These parameters can be part of the URL, query string, or body of a POST request. Django Rest Framework (DRF) provides a structured way to handle these parameters through serializers and views. Below is a step-by-step guide on how to achieve this:

### Step 1: Define Your Model

First, ensure your Django model is defined to include the fields you expect to receive from the frontend. For this example, let's use the `Item` model with an added `category` field as defined in the previous tutorials.

### Step 2: Create a Serializer

Your serializer will validate and deserialize input data to complex types. Update your `ItemSerializer` to handle new input data:

```python
# myapp/serializers.py
from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price', 'category']
```

### Step 3: Update Your View to Handle Parameters

Assuming you're using a `ModelViewSet`, it automatically handles the create (POST) action. However, you might want to customize how data is saved, especially if you're dealing with nested objects or need to perform additional operations. Here's how to override the `create` method in your viewset:

```python
# myapp/views.py
from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # Custom logic before saving an instance
        # e.g., modify data, add additional fields, etc.
        serializer.save()
```

### Step 4: Accepting Parameters from the Frontend

When the frontend sends a request, it can include parameters in various ways:

- **In the URL Path**: Handled by your URLconf, for example, `path('items/<int:category>/', views.ItemList.as_view())`.
- **As Query Parameters**: Accessible in your view via `self.request.query_params`, for example, `?price=19.99`.
- **In the Request Body**: For `POST` requests, data sent in the body of the request is accessible through `request.data`.

### Step 5: Handling Data in the Request Body

For a `POST` request where data is included in the request body (common for creating new resources), ensure your frontend sends data in a format that matches your serializer's fields. For instance, when creating a new `Item`, the request body might look like:

```json
{
  "name": "Sample Item",
  "description": "This is a sample item.",
  "price": 19.99,
  "category": 1
}
```

Your DRF backend will parse this JSON and use your serializer to validate and save a new `Item` instance.

### Step 6: Testing

You can test this setup using tools like Postman or cURL. Here's an example cURL command to create a new `Item`:

```sh
curl -X POST http://localhost:8000/api/items/ \
     -H 'Content-Type: application/json' \
     -d '{"name": "Sample Item", "description": "This is a sample item.", "price": 19.99, "category": 1}'
```

### Conclusion

This guide has walked you through handling frontend parameters in a Django Rest Framework application, from receiving parameters in your viewset to validating and saving them with serializers. Always ensure your data is validated before saving to the database to maintain data integrity and security. DRF's serialization and view layers provide a powerful and flexible way to handle complex data structures and interactions in your web applications.


# User Registration
Implementing user registration, login, and session management is a fundamental aspect of web application development with Django. Django's built-in `auth` app provides a robust framework for handling user accounts, authentication, and sessions. This tutorial guides you through setting up user registration, login, and maintaining user sessions in a Django project.

### Step 1: Configure Django's Authentication System

Ensure Django's `auth` app is included in your `INSTALLED_APPS` in the `settings.py` file. Django projects created using the `startproject` command include this by default:

```python
INSTALLED_APPS = [
    ...
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    ...
]
```

Also, make sure you have the authentication middleware and session middleware enabled:

```python
MIDDLEWARE = [
    ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    ...
]
```

### Step 2: Create a User Registration Form

You can use Django's built-in `UserCreationForm` or create a custom form for user registration. Here's how to use `UserCreationForm`:

1. In your app (let's call it `accounts`), create a file named `forms.py`.
2. Import `UserCreationForm` and create a form class:

```python
# accounts/forms.py

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
```

### Step 3: Create Views for Registration and Login

Create views for handling registration and login. You can use Django's built-in views for login and extend `UserCreationForm` for registration:

1. In `accounts/views.py`, import necessary classes and create your views:

```python
# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})
```

### Step 4: Configure URLs

Configure URLs for your views in `accounts/urls.py`:

```python
# accounts/urls.py

from django.urls import path
from .views import register, user_login

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
]
```

And include them in your project's main `urls.py` file:

```python
# project/urls.py

from django.urls import path, include

urlpatterns = [
    ...
    path('accounts/', include('accounts.urls')),
    ...
]
```

### Step 5: Create Templates for Registration and Login

Create HTML templates for your registration and login views. For example, `accounts/templates/accounts/register.html`:

```html
<!-- accounts/templates/accounts/register.html -->

<h2>Register</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Register</button>
</form>
```

And `accounts/templates/accounts/login.html`:

```html
<!-- accounts/templates/accounts/login.html -->

<h2>Login</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Login</button>
</form>
```

### Step 6: Handling User Sessions

Django automatically handles user sessions. When a user logs in using the `login()` function, Django creates a session for the user. You can access the user in your views with `request.user` and in your templates with `{{ user }}`. To log out a user, you can use the `logout()` function:

```python
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')
```

### Conclusion

This tutorial covered setting up user registration, login, and session management in Django. By leveraging Django's built-in `auth` app, you can implement a secure and efficient authentication system. Remember to customize the user experience according to your application's


# decouple config secret keys
Using `python-decouple` to manage secret keys and other configurations in Django projects is a best practice for keeping sensitive information secure. `python-decouple` separates the configuration of settings from your source code, allowing you to change settings without altering the code base. This approach is particularly useful for managing different configurations across development, testing, and production environments. This tutorial will guide you through the process of integrating `python-decouple` into a Django project.

### Step 1: Install `python-decouple`

First, you need to install `python-decouple`. You can do this by running the following command in your virtual environment:

```sh
pip install python-decouple
```

### Step 2: Create a `.env` File

Create a `.env` file in the root directory of your Django project. This file will store your configuration variables, such as secret keys, database credentials, API keys, etc. For example:

```
DEBUG=True
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgres://user:password@localhost:5432/your_db_name
```

It's important to add `.env` to your `.gitignore` file to prevent it from being checked into version control, keeping your secrets safe.

### Step 3: Configure `settings.py`

In your Django project's `settings.py`, import `config` from `decouple` and use it to set your configuration variables. Replace the Django settings that should be kept secret or that may vary between environments with calls to `config`:

```python
# settings.py

from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

For the `DATABASES` setting, you can use `config` to parse the database URL:

```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.parse(config('DATABASE_URL'))
}
```

This method allows you to easily switch your database backend by just changing the `DATABASE_URL` in your `.env` file.

### Step 4: Access Configuration Variables

Anywhere in your Django project where you need to access a configuration variable, you can use `config` to retrieve it from the `.env` file:

```python
from decouple import config

some_api_key = config('SOME_API_KEY')
```

This approach keeps your sensitive information out of your source code and makes it easy to update your configuration without touching the code itself.

### Step 5: Managing Different Environments

`python-decouple` makes it straightforward to manage settings for different environments (e.g., development, testing, production). You can create different `.env` files for each environment, like `.env.production` and `.env.development`, each with environment-specific variables. When deploying or running your project, ensure the correct `.env` file is used.

### Conclusion

Using `python-decouple` with `.env` files in your Django projects is an effective way to manage sensitive information and configuration settings, keeping them out of your source code. This setup enhances the security of your project by preventing accidental exposure of secret keys and other sensitive information. Additionally, it simplifies the management of different configurations across various environments, making your Django project more flexible and maintainable.