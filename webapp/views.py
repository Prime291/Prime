from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Customer, Flower, Order, OrderItem, Review
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from .forms import CustomerForm, CustomerPasswordChangeForm, CustomerEmailChangeForm, CustomerEditForm, UserRegisterForm, FlowerForm, OrderItemForm, OrderForm, PurchaseFlowerForm, ReviewForm

def edit_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('review_list')
    else:
        form = ReviewForm(instance=review)

    return render(request, 'CRUD/edit_review.html', {'form': form, 'review': review})

def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    
    if request.method == 'POST':
        review.delete()
        return redirect('review_list')

    return render(request, 'CRUD/delete_review.html', {'review': review})

def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.save()
            return redirect('review_list',)
    else:
        form = ReviewForm()

    return render(request, 'CRUD/add_review.html', {'form': form})

def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'pages/review.html', {'reviews': reviews})

def add_order_item(request):
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)

            # Determine the order dynamically, for example, get the latest order
            order = Order.objects.latest('id')

            order_item.order = order
            order_item.save()
            return redirect('order_item_list')  # Redirect to a success page or another appropriate view
    else:
        form = OrderItemForm()

    return render(request, 'CRUD/add_orderitem.html', {'form': form})

def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different username.')
                return render(request, 'add_customer.html', {'form': form})

            # Create a new User instance
            user = form.save(commit=False)
            user.save()

            # Create a new Customer instance and link it to the user
            customer = Customer(user=user)
            customer.phone_number = form.cleaned_data['phone_number']
            customer.address = form.cleaned_data['address']
            customer.profile_picture = form.cleaned_data['profile_picture']
            customer.birthday = form.cleaned_data['birthday']
            customer.age = form.cleaned_data['age']
            customer.gender = form.cleaned_data['gender']
            customer.save()

            messages.success(request, 'Customer added successfully.')
            return redirect('customer_page')  # Redirect to a success page
    else:
        form = CustomerForm()

    return render(request, 'CRUD/add_customer.html', {'form': form})

def purchase_flower(request, flower_id):
    flower = Flower.objects.get(pk=flower_id)

    if request.method == 'POST':
        form = PurchaseFlowerForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            if quantity > 0 and quantity <= flower.quantity_available:
                order_item = OrderItem.objects.create(
                    order=create_or_get_order(request.user),
                    flower=flower,
                    quantity=quantity
                )
                return redirect('my_orders')  # Redirect to the My orders list page
            else:
                form.add_error('quantity', 'Invalid quantity')
    else:
        form = PurchaseFlowerForm()

    return render(request, 'pages/purchase_flower.html', {'form': form, 'flower': flower})

def create_or_get_order(user):
    return user.order_set.filter(status='Pending').first() or user.order_set.create()

def orders_list(request):
    orders = Order.objects.all()
    return render(request, 'pages/orders.html', {'orders': orders})

def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('orders_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'CRUD/edit_order.html', {'form': form, 'order': order})

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('orders_list')

def edit_order_item(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)

    if request.method == 'POST':
        form = OrderItemForm(request.POST, instance=order_item)
        if form.is_valid():
            # Update the quantity
            order_item.quantity = form.cleaned_data['quantity']

            # Update the subtotal
            order_item.update_subtotal()
            order_item.save()
        return redirect('order_item_list')
            # Redirect or do whatever you need to do after editing
    else:
        form = OrderItemForm(instance=order_item)

    return render(request, 'CRUD/edit_orderitem.html', {'form': form})

def delete_order_item(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)

    if request.method == 'POST':
        order_item.delete()
        return redirect('order_item_list')

    return render(request, 'CRUD/delete_orderitem.html', {'order_item': order_item})

def my_orders(request):
    user = request.user
    orders = Order.objects.filter(customer=user).order_by('-date_ordered')
    return render(request, 'pages/myorder.html', {'orders': orders})
 
def order_item_list(request):
    
    error_message = None
    
    try:
        order_items = OrderItem.objects.all()
        total = sum(order_item.subtotal for order_item in order_items)
    except ValidationError as e:
        error_message = str(e)
        total = None

    return render(request, 'pages/1orderitem.html', {'error_message': error_message, 'order_items': order_items, 'total': total})
def edit_flower_modal(request, flower_id):
    flower = get_object_or_404(Flower, id=flower_id)

    if request.method == 'POST':
        form = FlowerForm(request.POST, instance=flower)
        if form.is_valid():
            form.save()
            return redirect('flower')  # Adjust the redirect URL

    else:
        form = FlowerForm(instance=flower)

    return render(request, 'CRUD/edit_flower_modal.html', {'form': form, 'flower': flower})

def delete_flower_modal(request, flower_id):
    flower = get_object_or_404(Flower, id=flower_id)

    if request.method == 'POST':
        flower.delete()
        return redirect('flower')
   
    return render(request, 'CRUD/delete_flower_modal.html', {'flower': flower})

def add_flower_modal(request):
    form = FlowerForm()

    if request.method == 'POST':
        form = FlowerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('flower')

    return render(request, 'CRUD/add_flower_modal.html', {'form': form})

def customer_edit(request, pk):
    
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        form = CustomerEditForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_page')  # Redirect to customer list page
    else:
        form = CustomerEditForm(instance=customer)

    return render(request, 'CRUD/customer_edit.html', {'form': form, 'customer': customer})
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        customer.delete()
        return redirect('customer_page')

    return render(request, 'CRUD/customer_delete.html', {'customer': customer}) 

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create a Customer instance for the registered user
            Customer.objects.create(user=user)

            messages.success(request, f'Hi {user.username}, your account was created successfully')
            return redirect('login')  # Redirect to the login page

    else:
        form = UserRegisterForm()

    return render(request, 'pages/register.html', {'form': form})

def CustomAdminPanelView(request):
   return render(request, 'pages/adminpanel.html')

def profile(request):
     customer = Customer.objects.get(user=request.user)

     if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('profile')

     else:
        form = CustomerForm(instance=customer)

     return render(request, 'pages/profile.html', {'customer': customer, 'form': form})

def home_page(request):
    return render(request, 'pages/home.html')

def customer_page(request):
    customers = Customer.objects.all()
    total_customers = customers.count()  # Calculate the total number of customers
    return render(request, 'pages/1customer.html', {'customers': customers, 'total_customers': total_customers})

def about(request):
    return render(request, 'pages/about.html')

def flower1(request):
    flowers = Flower.objects.all()
    return render(request, 'pages/1flower.html', {'flowers': flowers})

def product(request):
     flowers = Flower.objects.all()
     return render(request, 'pages/product.html', {'flowers': flowers})

def services(request):
    return render(request, 'pages/services.html')

@login_required
def update_profile(request):
    customer = Customer.objects.get(user=request.user)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = CustomerForm(instance=customer)

    return render(request, 'pages/update_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomerPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('homePage')  # Change 'home' to your desired URL
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomerPasswordChangeForm(request.user)
    return render(request, 'pages/change_password.html', {'form': form})

@login_required
def change_email(request):
    if request.method == 'POST':
        form = CustomerEmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your email was successfully updated!')
            return redirect('profile')  # Change 'home' to your desired URL
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomerEmailChangeForm(instance=request.user)
    return render(request, 'pages/change_email.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homePage')  # Replace 'home' with the URL name for your home page
    else:
        form = AuthenticationForm()

    return render(request, 'pages/login.html', {'form': form})

