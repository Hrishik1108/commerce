from django import forms
from .models import auction_listing,User
class create_listings(forms.ModelForm):
    
   
    class Meta: 
        model = auction_listing 
        fields = ("name","price","images","categories")
      