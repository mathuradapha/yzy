from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver



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

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat = models.CharField(max_length=255)
    price = models.IntegerField(default=100)
    showtime = models.CharField(max_length=50, default="18:00")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['movie', 'showtime', 'seat']

    def __str__(self):  # ✅ ถูกที่แล้ว
        return f"{self.movie.title} | {self.seat} | {self.showtime}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.movie.title} - {self.score}"



class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    price = models.IntegerField(default=150)
    created_at = models.DateTimeField(default=timezone.now)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)