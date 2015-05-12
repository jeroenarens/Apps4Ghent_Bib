__author__ = 'jeroen'
from django import forms

DECADE_CHOICES = [(1940,'1940'),(1950,'1950'),(1960,'1960'),(1970,'1970'),(1980,'1980'),(1990,'1990'),(2000,'2000')]
SEX_CHOICES = [('M','Male'),('V','Female')]
class booksform(forms.Form):
    decade = forms.ChoiceField(required=True, choices=DECADE_CHOICES)
    sex = forms.ChoiceField(required=True, choices=SEX_CHOICES)
