from django.shortcuts import render,redirect,get_object_or_404

from store.models import *
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.conf import settings
from store.email_messages import (
    cod_order_message,
    upi_order_message,
)

from django.db.models import Q

def category_products(request, slug):

    category = get_object_or_404(
        Category,
        slug=slug
    )

    products = Product.objects.filter(
        category=category
    )

    search = request.GET.get('search')

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    categories = Category.objects.all()

    cart_count = 0

    if request.user.is_authenticated:

        cart = Cart.objects.filter(
            user=request.user
        ).first()

        if cart:
            cart_count = sum(
                item.quantity
                for item in cart.items.all()
            )

    return render(
        request,
        'home.html',
        {
            'data': products,
            'categories': categories,
            'cart_count': cart_count,
            'selected_category': category
        }
    )

def home(request):
    products = Product.objects.all()

    search = request.GET.get('search')

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    categories = Category.objects.all()

    cart_count = 0

    if request.user.is_authenticated:
        cart = Cart.objects.filter(
            user=request.user
        ).first()

        if cart:
            cart_count = sum(
                item.quantity
                for item in cart.items.all()
            )

    return render(request, 'home.html', {
        'data': products,
        'categories': categories,
        'cart_count': cart_count,
    })



@login_required(login_url='login_page')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if not request.user.is_authenticated:

        messages.warning(
            request,
            "Please login to add items to your cart."
        )

        return redirect('login_page')

    if product.stock <= 0:
        return redirect('home_page')

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    item, created = Cartitem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        if item.quantity < product.stock:
            item.quantity += 1
            item.save()

    return redirect('home_page')

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    context = {
        "cart": cart
    }
    return render(request, "cart.html", context)

@login_required
def increase_quantity(request, product_id):
    item = get_object_or_404(Cartitem, id=product_id)

    if item.quantity < item.product.stock:
        item.quantity += 1
        item.save()

    return redirect('cart')


@login_required
def decreate_quantity(request,product_id):
    item=get_object_or_404(Cartitem,id=product_id)

    if item.quantity>1:
        item.quantity-=1
        item.save()
    else:
        item.delete()
    
    return redirect('cart')


@login_required
def remove_item(request,product_id):
    item=get_object_or_404(Cartitem,id=product_id)

    item.delete()

    return redirect('cart')

@login_required
def address_page(request):

    if request.method == 'POST':

        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        house = request.POST.get('house')
        area = request.POST.get('area')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        Address.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            mobile=mobile,
            address_line=f"{house}, {area}",
            city=city,
            state=state,
            pincode=pincode
        )

        return redirect('checkout')

    return render(request, 'address.html')



@login_required
def edit_address(request, id):

    address = get_object_or_404(
        Address,
        id=id,
        user=request.user
    )

    if request.method == 'POST':

        address.full_name = request.POST.get('full_name')
        address.email = request.POST.get('email')
        address.mobile = request.POST.get('mobile')
        address.address_line = request.POST.get('address_line')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.pincode = request.POST.get('pincode')

        address.save()

        return redirect('checkout')

    return render(
        request,
        'edit_address.html',
        {
            'address': address
        }
    )



def register_form(request):
    message=''
    if request.method == 'POST':
        username=request.POST.get('username','')
        email=request.POST.get('email','')
        password=request.POST.get('password','')
        confirm_password=request.POST.get('confirm_password','')

        if User.objects.filter(username=username).exists():
            message='username already exists Try another Email'
        elif User.objects.filter(email=email).exists():
            message='email already exists Try another Email'
        elif not username or not email or not password or not confirm_password:
            message='all fields should fill to register'
        elif password!=confirm_password:
            message='password mismatch Try Again'
        else:
            user=User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            user.save()
            return redirect('login_page')
    
    return render(request,'register.html',{'message':message})

def login_form(request):
    message=''
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)

            return redirect('home_page')
        
        else:
            message='invalid credentials'

    return render(request,'login.html',{'message':message})

def logout_page(request):
    logout(request)
    return redirect('home_page')



@login_required
def checkout(request):

    cart = Cart.objects.get(user=request.user)

    address = Address.objects.filter(
        user=request.user
    ).last()

    if not address:
        return redirect('address_page')

    if request.method == 'POST':

        payment_method = request.POST.get(
            'payment_method'
        )

        transaction_id = request.POST.get(
            'transaction_id'
        )

        if (
            payment_method == 'upi'
            and
            not transaction_id
        ):
            return render(
                request,
                'checkout.html',
                {
                    'cart': cart,
                    'address': address,
                    'error':
                    'Please enter UPI Transaction ID'
                }
            )
        
        # Check duplicate transaction id

        if payment_method == 'upi':

            if Payment.objects.filter(
                transaction_id=transaction_id
            ).exists():

                return render(
                    request,
                    'checkout.html',
                    {
                        'cart': cart,
                        'address': address,
                        'error':
                        'Transaction ID already exists. Please enter a valid transaction ID.'
                    }
                )

        order = Order.objects.create(
            user=request.user,
            totalamount=cart.total,
            address=address,
            status='pending'
        )

        for item in cart.items.all():

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        Payment.objects.create(
            order=order,
            totalamount=cart.total,
            method=payment_method,
            status='pending',
            transaction_id=
            transaction_id
            if payment_method == 'upi'
            else None
        )


        if payment_method == "cod":
            message = cod_order_message(
                request.user,
                order
            )

        else:
            message = upi_order_message(
                request.user,
                order,
                transaction_id
            )
        send_mail(
            "Order Confirmation",
            message,
            settings.EMAIL_HOST_USER,
            [address.email],
            fail_silently=False
        )

        cart.items.all().delete()

        return redirect('order_success',id=order.id)

    return render(
        request,
        'checkout.html',
        {
            'cart': cart,
            'address': address
        }
    )

@login_required
def order_success(request, id):

    order = get_object_or_404(
        Order,
        id=id,
        user=request.user
    )

    return render(
        request,
        'order_success.html',
        {
            'order': order
        }
    )

@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request,"myorders.html",{'orders':orders})


