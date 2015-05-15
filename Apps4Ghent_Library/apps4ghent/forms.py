from django import forms

#This form is used for the purpose of the REC, here a form is created where you can choose your birth year (decade) and sex (M/F)
DECADE_CHOICES = [(1940,'1940'),(1950,'1950'),(1960,'1960'),(1970,'1970'),(1980,'1980'),(1990,'1990'),(2000,'2000')]
SEX_CHOICES = [('M','Male'),('V','Female')]
CATEGORY_CHOICES = [('fictie','Fiction'),('non-fictie', 'Non-fiction')]
class booksform(forms.Form):
    decade = forms.ChoiceField(required=True, choices=DECADE_CHOICES)
    sex = forms.ChoiceField(required=True, choices=SEX_CHOICES)
    category = forms.ChoiceField(required=True, choices=CATEGORY_CHOICES)
