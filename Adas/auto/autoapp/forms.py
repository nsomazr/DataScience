from django import forms


class registerForm(forms.Form):
    fname=forms.CharField(max_length=20,widget=(forms.TextInput(attrs={'class':'form-control','placeholeder':'First Name'})))
    lname = forms.CharField(max_length=20,widget=(forms.TextInput(attrs={'class': 'form-control', 'placeholeder': 'Last Name'})))
    email = forms.EmailField(max_length=20, widget=(forms.EmailInput(attrs={'class': 'form-control', 'placeholeder': 'Email'})))
    uname = forms.CharField(max_length=20, widget=(forms.TextInput(attrs={'class': 'form-control', 'placeholeder': 'Username'})))
    pwd = forms.CharField(max_length=20, widget=(forms.PasswordInput(attrs={'class': 'form-control', 'placeholeder': 'Password'})))
    cpwd = forms.CharField(max_length=20, widget=(forms.PasswordInput(attrs={'class': 'form-control', 'placeholeder': 'Re-enter Password'})))


class loginForm(forms.Form):
    emailuname = forms.CharField(max_length=20, widget=(forms.TextInput(attrs={'class': 'form-control', 'placeholedr': 'Emai or Username','id':'fi'})))
    pwd = forms.CharField(max_length=20, widget=(forms.PasswordInput(attrs={'class': 'form-control', 'placeholedr': 'Password','id':'si'})))


class uploadForm(forms.Form):
    filename = forms.FileField(max_length=200,widget=(forms.FileInput(attrs={'class':'form-control','placeholder':'Choose a file'})))

