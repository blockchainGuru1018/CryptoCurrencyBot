from django.contrib import admin

from .models import Exchange, Spread, Tri_Spread

# Register your models here.

admin.site.register(Exchange)
admin.site.register(Spread)
admin.site.register(Tri_Spread)
