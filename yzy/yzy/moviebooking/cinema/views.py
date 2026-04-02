from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Movie, Category, Booking, Favorite, Ticket, Rating
import random
from django.db.models import Q

def home(request):
    search = request.GET.get('search')
    category_id = request.GET.get('category')

    movies = Movie.objects.all()

    if search:
        movies = movies.filter(
            Q(title__icontains=search) |
            Q(category__name__icontains=search)
        ).distinct()

    if category_id:
        movies = movies.filter(category=category_id)

    for m in movies:
        m.fake_score = round(random.uniform(6.5, 9.5), 1)

    categories = Category.objects.all()

    return render(request, 'home.html', {
        'movies': movies,
        'categories': categories
    })

from django.db.models import Avg

def movie_detail(request, id):
    movie = Movie.objects.get(id=id)

    avg_rating = Rating.objects.filter(movie=movie).aggregate(avg=Avg('score'))['avg']

    return render(request, 'movie.html', {
        'movie': movie,
        'avg_rating': avg_rating
    })

from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Movie, Booking


# 🎬 เลือกที่นั่ง
@login_required(login_url='/login/')
def seat(request, id):
    movie = get_object_or_404(Movie, id=id)
    numbers = [str(i) for i in range(1, 11)]

    # ✅ ใช้ showtime อย่างเดียว
    showtime = request.GET.get("showtime")

    booked = []

    if showtime:
        bookings = Booking.objects.filter(
            movie=movie,
            showtime=showtime
        )
        booked = [b.seat for b in bookings]

    # ==========================
    # 🔥 ตอนกด submit
    # ==========================
    if request.method == "POST":
        seats = request.POST.get("seats")
        showtime = request.POST.get("showtime")

        if not seats or not showtime:
            messages.error(request, "กรุณาเลือกรอบเวลาและที่นั่ง")
            return redirect('seat', id=id)

        return redirect(f"/payment/{id}/?seats={seats}&time={showtime}")

    return render(request, "seat.html", {
        "movie": movie,
        "booked": booked,
        "numbers": numbers,
        "showtime": showtime
    })

# 💳 หน้าจ่ายเงิน
@login_required(login_url='/login/')
def payment(request, id):
    movie = get_object_or_404(Movie, id=id)

    seats = request.GET.get("seats", "")
    showtime = request.GET.get("showtime", "")

    seat_list = seats.split(",") if seats else []

    # ✅ คำนวณราคาใหม่ตามโซน
    total_price = 0
    for s in seat_list:
        row = s[0]

        if row in ["A", "B", "C"]:
            total_price += 120
        elif row in ["D", "E", "F"]:
            total_price += 150
        else:
            total_price += 180

    # 🔥 POST
    if request.method == "POST":
        seats = request.POST.get("seats")
        showtime = request.POST.get("showtime")

        seat_list = seats.split(",")

        for seat in seat_list:
            Booking.objects.create(
                user=request.user,
                movie=movie,
                seat=seat,
                showtime=showtime
            )

        return redirect(f"/ticket/{id}/?seats={seats}&showtime={showtime}")

    return render(request, "payment.html", {
        "movie": movie,
        "seats": seats,
        "showtime": showtime,
        "total_price": total_price,
        "movie_id": id
    })
    
# 🎟 หน้าตั๋ว
@login_required(login_url='/login/')
def ticket(request, id):
    movie = get_object_or_404(Movie, id=id)

    seats = request.GET.get("seats")
    showtime = request.GET.get("showtime")

    seat_list = seats.split(",")

    tickets = Booking.objects.filter(
        user=request.user,
        movie=movie,
        showtime=showtime,
        seat__in=seat_list
    )

    if not tickets:
        return redirect('seat', id=id)

    # 🔥 QR
    import qrcode
    import base64
    from io import BytesIO

    data = f"{movie.title} | {seats} | {showtime}"
    qr = qrcode.make(data)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_code = base64.b64encode(buffer.getvalue()).decode()

    return render(request, "ticket.html", {
        "movie": movie,
        "tickets": tickets,
        "qr_code": qr_code
    })

from django.contrib.auth.decorators import login_required

@login_required
def mytickets(request):
    user = request.user
    tickets = Booking.objects.filter(user=user)

    price_per_seat = 100
    total = tickets.count() * price_per_seat

    return render(request, 'mytickets.html', {
        'tickets': tickets,
        'user': user,
        'total': total
    })

# --- ส่วนของแอดมิน (Admin Side) ---

@staff_member_required
def admin_dashboard(request):
    movies = Movie.objects.all()
    return render(request, 'admin/dashboard.html', {'movies': movies})

@staff_member_required
def admin_users(request):
    users = User.objects.all()
    return render(request, 'admin/users.html', {
        'users': users,
        'total_users': users.count()
    })

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

from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def add_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('admin_users')

    return render(request, 'admin/add_user.html')

from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

def edit_user(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        user.username = request.POST.get('username')
        user.save()
        return redirect('admin_users')

    return render(request, 'admin/edit_user.html', {'u': user})


def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect('admin_users')

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
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username หรือ Password ผิด")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/')

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "รหัสผ่านไม่ตรงกัน")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "มี username นี้แล้ว")
            return redirect('register')

        # 🔥 สร้าง user
        user = User.objects.create_user(
            username=username,
            password=password1
        )

        messages.success(request, "สมัครสำเร็จ!")
        return redirect('login')

    return render(request, 'register.html')

from django.db.models import Q

def search_movies(request):
    query = request.GET.get('q')
    genre = request.GET.get('genre')

    results = Movie.objects.all()

    if query:
        results = results.filter(
            Q(title__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()

    if genre:
        results = results.filter(category=genre)

    return render(request, 'search_results.html', {'results': results})

from django.contrib.auth.decorators import login_required
@login_required
def add_favorite(request, id):
    movie = get_object_or_404(Movie, id=id)

    Favorite.objects.get_or_create(
        user=request.user,
        movie=movie
    )

    return redirect('movie_detail', id=id)

from .models import Favorite

def my_favorites(request):
    favs = Favorite.objects.filter(user=request.user)
    return render(request, 'favorites.html', {'favs': favs})

@login_required
def rate_movie(request, id):
    if request.method == 'POST':
        score = request.POST['score']
        movie = Movie.objects.get(id=id)

        Rating.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={'score': score}
        )

    return redirect('movie_detail', id=id)

