from django.shortcuts import render, get_object_or_404
from .models import Cat, Toy
from .forms import FeedingForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView # add these 


class ToyList(ListView):
    model = Toy

class ToyDetail(DetailView):
    model = Toy

from django.http import HttpResponse
from django.shortcuts import render, redirect


# Simulate some Cat data
# class Cat:
#     def __init__(self, name, breed, description, age):
#         self.name = name
#         self.breed = breed
#         self.description = description
#         self.age = age

# # List of mock cats
# cats = [
#     Cat('Lolo', 'tabby', 'Kinda rude.', 3),
#     Cat('Sachi', 'tortoiseshell', 'Looks like a turtle.', 0),
#     Cat('Fancy', 'bombay', 'Happy fluff ball.', 4),
#     Cat('Bonk', 'selkirk rex', 'Meows loudly.', 6)
# ]

# This expects a template in the format of 
# templates/<app_name>/<model_name>_form.html
# templates/main_app/cat_form.html

class CatCreate(CreateView):
    model = Cat
    fields = '__all__'
# Go to the models.py file for the cat model

class CatUpdate(UpdateView):
    model = Cat
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'
    
class ToyCreate(CreateView):
    model = Toy
    fields = ['name', 'color']
   
class ToyDetail(DetailView):
    model = Toy
    
class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'

def cat_detail(request, cat_id):
    cat = get_object_or_404(Cat, id=cat_id)

    # Only get toys the cat does not already have
    toys_cat_doesnt_have = Toy.objects.exclude(id__in=cat.toys.all().values_list('id'))

    feeding_form = FeedingForm()
    return render(request, 'cats/detail.html', {
        'cat': cat,
        'feeding_form': feeding_form,
        'toys': toys_cat_doesnt_have,  # Pass available toys
    })

    
def add_feeding(request, cat_id):
    # create a ModelForm instance using the data in request.POST
    form = FeedingForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the cat_id assigned
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect('cat-detail', cat_id=cat_id)
  
# View function for cat index
def cat_index(request):
    cats = Cat.objects.all()  # look familiar?
    return render(request, 'cats/index.html', {'cats': cats})

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

    
def give_toy(request, cat_id, toy_id):
    cat = get_object_or_404(Cat, id=cat_id)
    toy = get_object_or_404(Toy, id=toy_id)
    
    # Check if the toy is already added to avoid duplicates
    if not cat.toys.filter(id=toy.id).exists():
        cat.toys.add(toy)
    
    # Redirect back to the cat's detail page
    return redirect('cat-detail', cat_id=cat.id)
def associate_toy(request, cat_id, toy_id):
    # Note that you can pass a toy's id instead of the whole object
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('cat-detail', cat_id=cat_id)

def remove_toy(request, cat_id, toy_id):
    cat = get_object_or_404(Cat, id=cat_id)
    toy = get_object_or_404(Toy, id=toy_id)
    
    # Remove the toy from the cat's toys
    cat.toys.remove(toy)
    
    # Redirect back to the cat's detail page
    return redirect('cat-detail', cat_id=cat.id)






