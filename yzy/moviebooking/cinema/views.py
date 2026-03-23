from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from .models import Movie,Category
from .models import Booking
from django.contrib.auth.decorators import login_required

def home(request):

    search = request.GET.get('search')
    category_id = request.GET.get('category')

    movies = Movie.objects.all()

    # 🔍 ค้นหา
    if search:
        movies = movies.filter(title__icontains=search)

    # 🎬 filter ประเภท
    if category_id:
        movies = movies.filter(category=category_id)

    categories = Category.objects.all()

    return render(request,'home.html',{
        'movies':movies,
        'categories':categories
    })

from django.shortcuts import render, get_object_or_404
from .models import Movie

def movie_detail(request, id):

    movie = get_object_or_404(Movie, id=id)

    trailer = get_youtube_embed(movie.trailer)

    return render(request, 'movie.html', {
        'movie': movie,
        'trailer': trailer
    })

def seat(request,id):

    movie = Movie.objects.get(id=id)

    booked = Booking.objects.filter(movie=movie).values_list('seat',flat=True)

    numbers = [str(i) for i in range(1,11)]

    if request.method == "POST":
        seats = request.POST.get("seats")  # ✅ ใช้ POST

        return redirect(f"/payment/{id}/?seats={seats}")

    return render(request,"seat.html",{
        "movie":movie,
        "booked":list(booked),
        "numbers":numbers
    })


def payment(request,id):

    seats = request.GET.get("seats")

    movie = Movie.objects.get(id=id)

    return render(request,"payment.html",{
        "seats":seats,
        "movie":movie,
        "movie_id":id
    })

def ticket(request,id):

    seats = request.GET.get("seats")  # ✅ หลายที่นั่ง

    movie = Movie.objects.get(id=id)

    seat_list = seats.split(",") if seats else []

    if request.user.is_authenticated:

        for s in seat_list:
            Booking.objects.create(
                user=request.user,
                movie=movie,
                seat=s
            )

    return render(request,"ticket.html",{
        "movie":movie,
        "seats":seat_list
    })


def admin_dashboard(request):

    movies = Movie.objects.all()

    return render(request,'admin/dashboard.html',{'movies':movies})


def add_movie(request):

    categories = Category.objects.all()

    if request.method == "POST":

        title = request.POST['title']
        description = request.POST['description']
        age = request.POST['age']
        poster = request.POST['poster']
        banner = request.POST['banner']
        trailer = request.POST['trailer']

        actors = request.POST['actors']
        director = request.POST['director']
        duration = request.POST['duration']

        category_ids = request.POST.getlist('category')  # ✅ หลายค่า

        movie = Movie.objects.create(
            title=title,
            description=description,
            age_rating=age,
            poster=poster,
            banner=banner,
            trailer=trailer,
            actors=actors,
            director=director,
            duration=duration
        )

        movie.category.set(category_ids)  # ✅ set manytomany

        return redirect('/admin-dashboard')

    return render(request,'admin/add_movie.html',{'categories':categories})


def edit_movie(request,id):

    movie = get_object_or_404(Movie,id=id)
    categories = Category.objects.all()

    if request.method == "POST":

        movie.title = request.POST.get('title')
        movie.description = request.POST.get('description')
        movie.age_rating = request.POST.get('age')
        movie.trailer = request.POST.get('trailer')

        movie.actors = request.POST.get('actors', '')
        movie.director = request.POST.get('director', '')
        movie.duration = int(request.POST.get('duration', 0))

        movie.poster = request.POST.get('poster', movie.poster)
        movie.banner = request.POST.get('banner', movie.banner)

        movie.save()

        category_ids = request.POST.getlist('category')
        movie.category.set(category_ids)
        return redirect('/admin-dashboard')

    return render(request,'admin/edit_movie.html',{
        'movie':movie,
        'categories':categories
    })


def delete_movie(request,id):

    movie = Movie.objects.get(id=id)

    movie.delete()

    return redirect('/admin-dashboard')

def login_user(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)

    return redirect('/')

@staff_member_required
def admin_dashboard(request):

    movies = Movie.objects.all()

    return render(request,'admin/dashboard.html',{'movies':movies})

def logout_user(request):
    logout(request)
    return redirect('/')


@login_required
def mytickets(request):

    tickets = Booking.objects.filter(user=request.user)

    return render(request,"mytickets.html",{
        "tickets":tickets
    })

def get_youtube_embed(url):
    if "watch?v=" in url:
        return url.replace("watch?v=", "embed/")
    return url

def rate_movie(request,id):

    movie = Movie.objects.get(id=id)
    score = request.POST.get('score')

    Rating.objects.update_or_create(
        user=request.user,
        movie=movie,
        defaults={'score':score}
    )

    return redirect(f'/movie/{id}')

def toggle_favorite(request,id):

    movie = Movie.objects.get(id=id)

    fav,created = Favorite.objects.get_or_create(
        user=request.user,
        movie=movie
    )

    if not created:
        fav.delete()

    return redirect(f'/movie/{id}')