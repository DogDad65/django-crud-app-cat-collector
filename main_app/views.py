from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Cat, Toy
from .forms import FeedingForm


# Home and About Views
class Home(LoginView):
    template_name = 'home.html'


def about(request):
    return render(request, 'about.html')


# Cat Views (CRUD and Details)
class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age']

    def form_valid(self, form):
        # Associate the logged-in user with the new cat entry
        form.instance.user = self.request.user
        return super().form_v


class CatUpdate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = ['breed', 'description', 'age']


class CatDelete(LoginRequiredMixin, CreateView):
    model = Cat
    success_url = '/cats/'


@login_required
def cat_index(request):
    # Show only the cats owned by the logged-in user
    cats = Cat.objects.filter(user=request.user)
    return render(request, 'cats/index.html', {'cats': cats})


@login_required
def cat_detail(request, cat_id):
    # Display cat details and available toys not yet owned by the cat
    cat = get_object_or_404(Cat, id=cat_id)
    toys_cat_doesnt_have = Toy.objects.exclude(id__in=cat.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'cats/detail.html', {
        'cat': cat,
        'feeding_form': feeding_form,
        'toys': toys_cat_doesnt_have,
    })


@login_required
def add_feeding(request, cat_id):
    # Add feeding data for a specific cat
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect('cat-detail', cat_id=cat_id)


# Toy Views (CRUD and List/Details)
class ToyList(ListView):
    model = Toy


class ToyDetail(DetailView):
    model = Toy


class ToyCreate(CreateView):
    model = Toy
    fields = ['name', 'color']


class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']


class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'


# Toy Association Functions
@login_required
def give_toy(request, cat_id, toy_id):
    # Associate a toy with a specific cat if not already owned
    cat = get_object_or_404(Cat, id=cat_id)
    toy = get_object_or_404(Toy, id=toy_id)
    if not cat.toys.filter(id=toy.id).exists():
        cat.toys.add(toy)
    return redirect('cat-detail', cat_id=cat.id)


@login_required
def associate_toy(request, cat_id, toy_id):
    # Add a toy to a cat's collection
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('cat-detail', cat_id=cat_id)


@login_required
def remove_toy(request, cat_id, toy_id):
    # Remove a toy from a cat's collection
    cat = get_object_or_404(Cat, id=cat_id)
    toy = get_object_or_404(Toy, id=toy_id)
    cat.toys.remove(toy)
    return redirect('cat-detail', cat_id=cat.id)


# User Signup
def signup(request):
    # Handle user signup and login process
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cat-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
