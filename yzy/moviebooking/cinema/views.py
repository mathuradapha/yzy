from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Movie, Category, Booking

# --- ส่วนของหน้าบ้าน (User Side) ---

def home(request):
    search = request.GET.get('search')
    category_id = request.GET.get('category')
    movies = Movie.objects.all()
    if search:
        movies = movies.filter(title__icontains=search)
    if category_id:
        movies = movies.filter(category=category_id)
    categories = Category.objects.all()
    return render(request, 'home.html', {'movies': movies, 'categories': categories})

def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    return render(request, 'movie.html', {'movie': movie})

@login_required(login_url='/login/')
def seat(request, id):
    movie = get_object_or_404(Movie, id=id)
    booked = Booking.objects.filter(movie=movie).values_list('seat', flat=True)
    numbers = [str(i) for i in range(1, 11)]
    if request.method == "POST":
        seats = request.POST.get("seats")
        return redirect(f"/payment/{id}/?seats={seats}")
    return render(request, "seat.html", {"movie": movie, "booked": list(booked), "numbers": numbers})

@login_required(login_url='/login/')
def payment(request, id):
    seats = request.GET.get("seats")
    movie = get_object_or_404(Movie, id=id)
    return render(request, "payment.html", {"seats": seats, "movie": movie, "movie_id": id})

@login_required(login_url='/login/')
def ticket(request, id):
    seats = request.GET.get("seats")
    movie = get_object_or_404(Movie, id=id)
    seat_list = seats.split(",") if seats else []
    for s in seat_list:
        Booking.objects.create(user=request.user, movie=movie, seat=s)
    return render(request, "ticket.html", {"movie": movie, "seats": seat_list})

@login_required(login_url='/login/')
def mytickets(request):
    tickets = Booking.objects.filter(user=request.user).order_by('-id')
    return render(request, "mytickets.html", {"tickets": tickets})

# --- ส่วนของระบบสมาชิก ---

def login_user(request):
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user:
            login(request, user)
            return redirect('/')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

# --- ส่วนของแอดมิน (Admin Side) ---

@staff_member_required
def admin_dashboard(request):
    movies = Movie.objects.all()
    return render(request, 'admin/dashboard.html', {'movies': movies})

@staff_member_required
def add_movie(request):
    categories = Category.objects.all()
    if request.method == "POST":
        movie = Movie.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            age_rating=request.POST['age'],
            poster=request.POST['poster'],
            banner=request.POST['banner'],
            trailer=request.POST['trailer'],
            actors=request.POST['actors'],
            director=request.POST['director'],
            duration=request.POST['duration']
        )
        movie.category.set(request.POST.getlist('category'))
        return redirect('/admin-dashboard/')
    return render(request, 'admin/add_movie.html', {'categories': categories})

@staff_member_required
def edit_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    categories = Category.objects.all()
    if request.method == "POST":
        movie.title = request.POST.get('title')
        movie.description = request.POST.get('description')
        movie.age_rating = request.POST.get('age')
        movie.trailer = request.POST.get('trailer')
        movie.actors = request.POST.get('actors', '')
        movie.director = request.POST.get('director', '')
        movie.duration = int(request.POST.get('duration', 0))
        movie.save()
        movie.category.set(request.POST.getlist('category'))
        return redirect('/admin-dashboard/')
    return render(request, 'admin/edit_movie.html', {'movie': movie, 'categories': categories})

@staff_member_required
def delete_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    movie.delete()
    return redirect('/admin-dashboard/')

# cinema/views.py
from django.contrib import messages # เพิ่มไว้ด้านบนสุดของไฟล์

def register_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "ชื่อผู้ใช้นี้มีคนใช้แล้ว!")
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, "สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ")
    
    return redirect('/')  # กลับหน้าแรก (ใช้ modal)


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('/')
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password1']
            )
            return redirect('login')
    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('login')