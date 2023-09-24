from django import forms
from .models import Contact,CreditCard

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'phone_number', 'email', 'message')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }
class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ['card_number', 'exp_month', 'exp_year', 'cvc']
        widgets = {
            'card_number': forms.TextInput(attrs={'placeholder': '1234 5678 9012 3456', 'class': 'form-control'}),
            'exp_month': forms.TextInput(attrs={'placeholder': 'MM', 'class': 'form-control'}),
            'exp_year': forms.TextInput(attrs={'placeholder': 'YYYY', 'class': 'form-control'}),
            'cvc': forms.TextInput(attrs={'placeholder': '123', 'class': 'form-control'}),
        }
