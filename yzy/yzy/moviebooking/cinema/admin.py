from django.contrib import admin
from .models import Movie, Category, Booking, Profile

admin.site.register(Movie)
admin.site.register(Category)
admin.site.register(Booking)
admin.site.register(Profile)