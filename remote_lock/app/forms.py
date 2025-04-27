from django import forms

from .models import Folders

from django.contrib.auth.models import User

class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                             'required':'required'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                             'required':'required'}))

class ForgotPasswordForm(forms.Form):

    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                             'required':'required',
                                                             'placeholder':'Enter your registered email'}))
    def clean(self):

        cleaned_data = super().clean()

        email = cleaned_data.get('email')

        host = email.split('@')[1]

        if host not in ['gmail.com','outlook.com','hotmail.com','mailinator.com','yahoo.com']:

            self.add_error('email','not a valid domain')   

        elif email not in User.objects.filter().values_list('username',flat=True):
        
            self.add_error('email','not a registered email')  

        return cleaned_data 
    
class OTPForm(forms.Form):

    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                             'readonly':'readonly'}))  
    
    otp = forms.CharField(widget=forms.TextInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                             'required':'required',
                                                             'maxlength': '6' })) 

class ChangePasswordForm(forms.Form):

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                             'required':'required'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                             'required':'required'}))
    
    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')

        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:

            self.add_error('confirm_password','password mismatch')
         
        return cleaned_data  

class KeyPasswordForm(forms.Form):

    key = forms.CharField(widget=forms.PasswordInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                             'required':'required',
                                                             'placeholder':'Enter Key'}))  
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                             'required':'required',
                                                             'placeholder':'Enter Password'}))    
    

class RegisterForm(forms.Form):
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                             'required':'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                             'required':'required'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                             'required':'required'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                             'required':'required'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                             'required':'required'}))
    
    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')

        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:

            self.add_error('confirm_password','password mismatch')

        email = cleaned_data.get('email')

        host = email.split('@')[1]

        if host not in ['gmail.com','outlook.com','hotmail.com','mailinator.com','yahoo.com']:

            self.add_error('email','not a valid domain')    

        return cleaned_data 