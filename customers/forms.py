from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer, Order

class CustomerRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            customer = Customer.objects.create(
                user=user,
                name=self.cleaned_data['name'],
            )
        return user

class CustomerLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class CheckoutForm(forms.ModelForm):
    delivery_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=True,
        help_text="Please provide your delivery address"
    )
    payment_method = forms.ChoiceField(
        choices=[
            ('cash', 'Cash on Delivery'),
            ('card', 'Credit/Debit Card'),
            ('gcash', 'GCash'),
            ('paymaya', 'PayMaya'),
        ],
        required=True
    )
    special_instructions = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        required=False,
        help_text="Any special instructions for your order"
    )

    class Meta:
        model = Order
        fields = ['delivery_address', 'payment_method', 'special_instructions'] 