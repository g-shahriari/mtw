from django import forms
from django.contrib.auth.models import User
from first_app.models import Customer,Seller,Comments


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields= ('username','email','password')

class CustomerForm(forms.ModelForm):
    class Meta():
        model = Customer
        fields = ('phone','Gender','Address','Image','History')


class SellerForm(forms.ModelForm):

    class Meta():
        model = Seller
        fields = ('Category_type','phone','address','goods')

class PollForm(forms.ModelForm):
    class Meta():
        model = Comments
        fields = ('name','Search_cost_geo','Search_cost_sim','Best_decision_geo','Best_decision_sim')
