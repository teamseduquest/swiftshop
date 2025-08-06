from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Product, Category

@login_required
def products_lst(request):
    selected_category = request.GET.get('category')
    query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'name')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    in_stock = request.GET.get('in_stock')

    products = Product.objects.all()

    # 🔍 Search query
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # 🧭 Filter by category
    if selected_category:
        products = products.filter(category__name=selected_category)

    # 💰 Price filters
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # 📦 In stock filter
    if in_stock == '1':
        products = products.filter(stock__gt=0)

    # ↕️ Sorting
    if sort_by == 'price':
        products = products.order_by('price')
    elif sort_by == 'latest':
        products = products.order_by('-id')
    else:
        products = products.order_by('name')

    # 📄 Pagination
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    categories = Category.objects.all()

    return render(request, 'products/products_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'sort': sort_by,
    })
