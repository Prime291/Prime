# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import User, Customer, Flower, OrderItem, Order, Review

class PurchaseFlowerForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label='Quantity')
        
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']  # Include the fields you want to include in the form

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'flower', 'quantity']

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        flower = self.cleaned_data.get('flower')

        if flower and quantity > flower.quantity_available:
            raise forms.ValidationError("Quantity exceeds available quantity for this flower.")
        
        return quantity


class FlowerForm(forms.ModelForm):
    class Meta:
        model = Flower
        fields = ['name', 'description', 'price', 'image', 'quantity_available', 'category']

class CustomerEditForm(forms.ModelForm):
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    class Meta:
        model = Customer
        
        fields = ['profile_picture','phone_number', 'address', 'birthday', 'age', 'gender' ]

class CustomerForm(UserCreationForm):
    phone_number = forms.CharField(max_length=11)
    address = forms.CharField(widget=forms.Textarea)
    profile_picture = forms.ImageField(required=False)
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    age = forms.IntegerField(required=False)
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], required=False)

    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2', 'phone_number', 'address', 'profile_picture', 'birthday', 'age', 'gender']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class CustomerPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['old_password', 'new_password1', 'new_password2']

class CustomerEmailChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['email']
        
class ReviewForm(forms.ModelForm):
    # Define choice fields for customer and flower
    customer = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    flower = forms.ModelChoiceField(queryset=Flower.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Review
        fields = ['customer', 'flower', 'rating', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add additional attributes or customize the form if needed
        self.fields['rating'].widget.attrs['class'] = 'form-control'
        self.fields['comment'].widget.attrs['class'] = 'form-control'
