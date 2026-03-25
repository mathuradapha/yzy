from django.db import models
from django.contrib.auth.models import User

banner = models.URLField()
poster = models.URLField()

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    category = models.ManyToManyField(Category)  # ✅ หลายประเภท

    age_rating = models.CharField(max_length=10)

    duration = models.IntegerField()  # ✅ นาที

    actors = models.TextField()  # ✅ นักแสดง
    director = models.CharField(max_length=100)  # ✅ ผู้กำกับ

    poster = models.URLField()
    banner = models.URLField()
    trailer = models.URLField()

    def __str__(self):
        return self.title


# cinema/models.py
from django.contrib.auth.models import User

class Booking(models.Model):
    # เชื่อมการจองกับผู้ใช้งาน (User) ที่ Login อยู่
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    score = models.IntegerField()

class Favorite(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
