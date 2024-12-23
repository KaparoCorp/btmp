from django import forms
from .models import Item, Appraisal, Exchange, Rating, Profile, Category


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location','profile_picture']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['photo', 'estimated_value', 'suggestions' , 'category' , 'status' , 'description' , 'appraisal_amount']
        

class AppraisalForm(forms.ModelForm):
    class Meta:
        model = Appraisal
        fields = ['market_trend_value', 'community_votes', 'admin_input']

class ExchangeForm(forms.ModelForm):
    class Meta:
        model = Exchange
        fields = ['proposed_value']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score', 'comment']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']