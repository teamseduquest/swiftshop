from accounts.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from orders.models import Order
from products.models import Product
from django.db.models import Sum

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            # Send email to admin
            send_mail(
                subject='🧑‍💻 New User Registration',
                message=f"""A new user has registered:

Username: {user.username}
Full Name: {user.first_name} {user.last_name}
Email: {user.email}
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['team.eduquestm.com@gmail.com'],
                fail_silently=False,
            )

            messages.success(request, "Registration successful. Please log in.")
            return redirect('login-user')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and not user.is_staff:
            login(request, user)
            return redirect('products_list')
        else:
            messages.error(request, "Invalid credentials or not a regular user.")
    return render(request, 'accounts/user_login.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        admin_user = authenticate(request, username=username, password=password)
        if admin_user is not None and admin_user.is_staff:
            login(request, admin_user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid admin credentials.")
    return render(request, 'accounts/admin_login.html')


def logout_user(request):
    logout(request)
    return redirect('login-user')


from django.db.models.functions import TruncMonth
from django.db.models import Sum
from collections import OrderedDict
import calendar

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_sales = Order.objects.filter(status="approved").aggregate(total=Sum("total_price"))["total"] or 0
    pending_orders = Order.objects.filter(status="pending").count()

    # Group sales by month
    monthly_sales = (
        Order.objects.filter(status="approved")
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("total_price"))
        .order_by("month")
    )

    # Format the results
    sales_labels = []
    sales_data = []
    for entry in monthly_sales:
        month_name = calendar.month_name[entry["month"].month]
        sales_labels.append(month_name)
        sales_data.append(float(entry["total"]))

    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_sales': total_sales,
        'pending_orders': pending_orders,
        'sales_labels': sales_labels,
        'sales_data': sales_data,
    }
    return render(request, 'accounts/admin_dashboard.html', context)



@login_required
def user_dashboard(request):
    return render(request, 'accounts/user_dashboard.html')


@login_required
def dashboard_redirect(request):
    if request.user.is_superuser or request.user.is_staff:
        return redirect('admin_dashboard')
    else:
        return redirect('user_dashboard')


# accounts/views.py

from django.contrib.auth import get_user_model
from django.http import HttpResponse

def create_superuser(request):
    User = get_user_model()
    username = "admin"
    email = "admin@example.com"
    password = "StrongPassword123"

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        return HttpResponse("✅ Superuser created!")
    else:
        return HttpResponse("⚠️ Superuser already exists.")
