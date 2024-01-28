from django.urls import path
from . import views 
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path ('', views.home_page, name="homePage"),
    
    # Review
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('flowers/add_review/', views.add_review, name='add_review'),
    path('reviews/', views.review_list, name='review_list'),
    
    # OrderItem
    path('add_order_item/', views.add_order_item, name='add_order_item'),
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/<int:order_id>/edit/', views.edit_order, name='edit_order'),
    path('orders/<int:order_id>/delete/', views.delete_order, name='delete_order'),
    
    # Customer
    path('add_customer/', views.add_customer, name='add_customer'),
    path('customer/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customer/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path ('customer/', views.customer_page, name="customer_page"),
    
    # Purchase
    path('purchase_flower/<int:flower_id>/', views.purchase_flower, name='purchase_flower'),
    
    # Order
    path('order-item/<int:order_item_id>/edit/', views.edit_order_item, name='edit_order_item'),
    path('order-item/<int:order_item_id>/delete/', views.delete_order_item, name='delete_order_item'),
    path('myorders/', views.my_orders, name='my_orders'),
    path('order_items/', views.order_item_list, name='order_item_list'),
    
    # Flower
    path('flower/<int:flower_id>/edit/', views.edit_flower_modal, name='edit_flower_modal'),
    path('flower/<int:flower_id>/delete/', views.delete_flower_modal, name='delete_flower_modal'),
    path('flower/add/', views.add_flower_modal, name='add_flower_modal'),
    path('flower/', views.flower1, name='flower'), 
    
    # Pages
    path ('about/', views.about, name="about"),
    path('accounts/profile/', views.profile, name='profile'),
    path('adminpanel/', views.CustomAdminPanelView, name='admin_panel'),
    path('accounts/profile/update/', views.update_profile, name='update_profile'),
    path('product/', views.product, name="product"),
    path ('services/', views.services, name="services"),
    path('register/', views.register, name='register'),
    
    # User Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='pages/logout.html'), name="logout"),
    path('change-password/', views.change_password, name='change_password'),
    path('change-email/', views.change_email, name='change_email'),
    
]+  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)