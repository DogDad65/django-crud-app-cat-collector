from django.contrib import admin

from .models import Cat, Feeding, Toy  

admin.site.register(Cat)
admin.site.register(Feeding)
# Add the Toy model
admin.site.register(Toy)
