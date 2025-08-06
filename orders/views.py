from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.cart import Cart
from .models import Order, OrderItem
from django.utils import timezone
import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_approve_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        decision = request.POST.get('decision')

        if decision == 'approved':
            order.status = 'approved'  # ✅ Match model status value
        elif decision == 'rejected':
            order.status = 'rejected'
        else:
            messages.error(request, "❌ Invalid decision.")
            return redirect('admin_dashboard')
        send_mail(
        subject=f"Order Update: #{order.order_id}",
        message=(
        f"Hello {order.user.first_name},\n\n"
        f"We’ve reviewed your order placed on {order.created_at.strftime('%B %d, %Y at %I:%M %p')}.\n\n"
        f"📦 Order ID: {order.order_id}\n"
        f"📅 Date: {order.created_at.strftime('%B %d, %Y')}\n"
        f"📌 Status: {order.status.title()}\n\n"
        "Thank you for shopping with us.\n\n"
        "Best regards,\n"
        "SwiftShop Team"
    ),
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[order.user.email],
    fail_silently=False,
)
        order.save()
        messages.success(request, f'Order #{order.order_id} marked as {order.status.capitalize()}.')
        return redirect('admin_dashboard')

    return render(request, 'orders/approve_order.html', {'order': order})

@login_required
def checkout(request):
    cart = Cart(request)

    if request.method == 'POST':
        # 1. Create Order
        order = Order.objects.create(
            user=request.user,
            total_price=cart.get_total_price(),
            created_at=timezone.now()
        )

        # 2. Create OrderItems
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        # 3. Clear cart
        cart.clear()

        # 4. Generate approval link AFTER order is created
        approval_url = request.build_absolute_uri(reverse('admin_approve_order', args=[order.id]))

        # 5. Send email to admin
        send_mail(
            subject='🛒 New Order Placed',
            message=(
                f"New order placed by {request.user.username}\n"
                f"Full Name: {request.user.first_name} {request.user.last_name}\n"
                f"Order ID: {order.order_id}\n"
                f"Total Price: $ {order.total_price:,}, Ksh. {order.total_price * 129:,.2f}\n"
                f"Date: {datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}\n"
                f"\nClick below to approve or reject the order:\n{approval_url}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['team.eduquestm.com@gmail.com'],
            fail_silently=False,
        )

        messages.success(request, '✅ Order placed successfully!')
        return redirect('order_detail', order_id=order.id)

    return render(request, 'orders/checkout.html', {'cart': cart})




@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    for item in order.items.all():
        item.total_price = item.price * item.quantity
    return render(request, 'orders/order_detail.html', {'order': order})
