from django.shortcuts import render

# Simulate some Cat data
class Cat:
    def __init__(self, name, breed, description, age):
        self.name = name
        self.breed = breed
        self.description = description
        self.age = age

# List of mock cats
cats = [
    Cat('Lolo', 'tabby', 'Kinda rude.', 3),
    Cat('Sachi', 'tortoiseshell', 'Looks like a turtle.', 0),
    Cat('Fancy', 'bombay', 'Happy fluff ball.', 4),
    Cat('Bonk', 'selkirk rex', 'Meows loudly.', 6)
]

# View function for cat index
def cat_index(request):
    return render(request, 'cats/index.html', {'cats': cats})

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')
