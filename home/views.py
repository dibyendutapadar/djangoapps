from django.shortcuts import render,redirect
from django.http import HttpResponse



products = [
    {
        "title": "Intelligent Traffic Management System",
        "description": "A state-of-the-art system to optimize traffic flow and reduce congestion.",
        "image": "static/traffic.png",  # Replace with actual image path
        "link": "/traffic"
    },
    {
        "title": "Auto Test Generator",
        "description": "An innovative tool for educators to automatically generate questions papers for students",
        "image": "static/auto_test.png",  # Replace with actual image path
        "link": "/testGenerator"
    },
    {
        "title": "Skill Development",
        "description": "A tool to enhance skill for students",
        "image": "static/auto_test.png",  # Replace with actual image path
        "link": "/skillDevelopment"
    },
        {
        "title": "Recipe Finder",
        "description": "Transform the contents of your fridge into culinary masterpieces!",
        "image": "static/recipe.png",  # Replace with actual image path
        "link": "/recipeFinder"
    },
        {
        "title": "World in Data",
        "description": "Creating meaning out of key parameters and indices of countries",
        "image": "static/world_data.png",  # Replace with actual image path
        "link": "/worldData"
    }
]


# Create your views here.
def home(request):
    context={
        'products':products,
    }
    return render(request,'home.html',context)