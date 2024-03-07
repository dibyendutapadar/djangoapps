from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Item
from .forms import AddItemForm


# Create your views here.
def index(request):
    return HttpResponse('<h1>index')



def items(request):
    item_list = Item.objects.all()
    context={
        'item_list':item_list,
    }
    return render(request,'items.html',context)

def item_detail(request,item_id):
    item=Item.objects.get(pk=item_id)
    context={
        'item':item,
    }
    return render(request,'item_detail.html',context)

def add_item(request):
    form = AddItemForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('items.html')
    return render(request,'AddItemForm.html',{'form':form})
