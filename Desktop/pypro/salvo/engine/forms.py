from django import forms

class url_form(forms.Form):
    your_name = forms.CharField(label="",max_length=500,)
    your_name.widget = forms.TextInput(attrs={'class':'form-control','placeholder':' paste a youtube video url',})

