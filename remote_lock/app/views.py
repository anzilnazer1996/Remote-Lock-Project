from django.shortcuts import render

# Create your views here.

from django.shortcuts import render,redirect

from django.views import View

from .forms import LoginForm,KeyPasswordForm,RegisterForm

from django.contrib.auth import authenticate,logout,login

from django.db import transaction

from .models import Folders,Files,Reports

from .utility import get_password,password_encrypting,password_decrypting

from .utility import key_from_binary_to_hex,key_from_hex_to_binary,send_email

import threading

import os

import zipfile

from django.http import HttpResponse

from django.conf import settings

from django.contrib.auth.models import User



class LoginView(View):

    def get(self,request,*args,**kwargs):

        form = LoginForm()

        data = {'form':form}

        return render(request,'login.html',context=data)
    
    def post(self,request,*args,**kwargs):

        form = LoginForm(request.POST)

        error = None

        if form.is_valid():

            email = form.cleaned_data.get('email')

            password = form.cleaned_data.get('password')

            user = authenticate(username=email, password=password)

            if user:

                login(request,user)

                return redirect('home')
            
            else:

                error = 'user does not exists '

                print(error)       
            
        data = {'form':form,'error':error}

        return render(request,'login.html',context=data)


class LogoutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect('login')
    
class HomeView(View):
    def get(self,request,*args,**kwargs):

        folders = Folders.objects.filter(user=request.user)
        query = request.GET.get('query')

        if query:

            folders = folders.filter(name__icontains=query)

        data = {'folders':folders,'page':'home','query':query}

        return render(request, 'home.html',context=data)    

class AddFolderView(View):
    def get(self,request,*args,**kwargs):

        return render(request, 'add-folder.html')

    def post(self,request,*args,**kwargs):

        with transaction.atomic():

            files=request.FILES.getlist('files')

            name = request.POST.get('name')

            if name and files:

                user = request.user

                folder = Folders.objects.create(user=user,name=name)

                for file in files:

                    Files.objects.create(folder=folder, file=file)

                Reports.objects.create(user=user,folder_name=folder.name,action='Added')   

                return redirect('home')

            return render(request, 'add-folder.html', {'error': 'name and files are required'})    


class UnlockingView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        folder = Folders.objects.get(uuid=uuid, user=request.user)

        password = get_password()

        key,nonce,encrypted_password = password_encrypting(password)

        key = key_from_binary_to_hex(key)

        folder.folder_nonce = nonce

        folder.folder_password = encrypted_password

        folder.save()

        subject = 'Request For Unlock Folder'

        recepient = request.user.email

        template = 'unlock-email.html'

        context = {'name':f'{request.user.first_name} {request.user.last_name}','folder_name':folder.name,'key':key,'password':password,'email_for':'unlock'}

        thread = threading.Thread(target=send_email,args=(subject,recepient,template,context))

        thread.start()

        form = KeyPasswordForm() 

        return render(request,'unlock.html',context={'form':form})
    
    def post(self,request,*args,**kwargs):

        form = KeyPasswordForm(request.POST)

        if form.is_valid():

            uuid = kwargs.get('uuid')

            folder = Folders.objects.get(uuid=uuid, user=request.user)

            key = form.cleaned_data.get('key')

            

            password = form.cleaned_data.get('password')

            encrypted_password = folder.folder_password

            nonce = folder.folder_nonce
            try:
                key = key_from_hex_to_binary(key)

                decrypted_password = password_decrypting(key,nonce,encrypted_password)

            except:

                return render(request,'unlock.html',context={'form':form,'error':'Incorrect Key or Password'})    

            if decrypted_password == password:

                folder.folder_locked = False

                folder.save()

                Reports.objects.create(user=request.user,folder_name=folder.name,action='Unlocked')
            
                return redirect('home')
            
            return render(request,'unlock.html',context={'form':form,'error':'Incorrect Key or Password'})
        
        return render(request,'unlock.html',context={'form':form})


class LockView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        folder = Folders.objects.get(uuid=uuid, user=request.user)

        folder.folder_locked = True

        folder.save()

        Reports.objects.create(user=request.user,folder_name=folder.name,action='Locked')

        return redirect('home') 

class DeleteView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        folder = Folders.objects.get(uuid=uuid, user=request.user)

        password = get_password()

        key,nonce,encrypted_password = password_encrypting(password)

        key = key_from_binary_to_hex(key)

        folder.folder_nonce = nonce

        folder.folder_password = encrypted_password

        folder.save()

        subject = 'Request For Delete Folder'

        recepient = request.user.email

        template = 'unlock-email.html'

        context = {'name':f'{request.user.first_name} {request.user.last_name}','folder_name':folder.name,'key':key,'password':password,'email_for':'delete'}

        thread = threading.Thread(target=send_email,args=(subject,recepient,template,context))

        thread.start()

        form = KeyPasswordForm() 

        return render(request,'unlock.html',context={'form':form})         

    def post(self,request,*args,**kwargs):

        form = KeyPasswordForm(request.POST)

        if form.is_valid():

            uuid = kwargs.get('uuid')

            folder = Folders.objects.get(uuid=uuid, user=request.user)

            key = form.cleaned_data.get('key')

            password = form.cleaned_data.get('password')

            encrypted_password = folder.folder_password

            nonce = folder.folder_nonce

            try:
                key = key_from_hex_to_binary(key)

                decrypted_password = password_decrypting(key,nonce,encrypted_password)

            except:

                return render(request,'unlock.html',context={'form':form,'error':'Incorrect Key or Password'})    

            if decrypted_password == password:

                folder_name= folder.name

                folder.delete()

                Reports.objects.create(user=request.user,folder_name=folder_name,action='Deleted')
            
                return redirect('home')
            
            return render(request,'unlock.html',context={'form':form,'error':'Incorrect Key or Password'})
        
        return render(request,'unlock.html',context={'form':form})


class FolderFilesView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        folder = Folders.objects.get(uuid=uuid, user=request.user)

        Reports.objects.create(user=request.user,folder_name=folder.name,action='Viewed')

        return render(request,'folder-with-files.html',context={'folder':folder})

class DownloadFolderView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        folder = Folders.objects.get(uuid=uuid, user=request.user)

        files = folder.files.all()

        # Create a temporary ZIP file
        zip_filename = f"{folder.name}.zip"
        zip_path = os.path.join(settings.MEDIA_ROOT, zip_filename)
    
        # Create and write to the ZIP file
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file in files:
                arcname = os.path.basename(file.file.name)
                # Add each file to the ZIP archive, preserving the folder structure
                zip_file.write(file.file.path, arcname=arcname)
    
        # Open the ZIP file to send as HTTP response
        with open(zip_path, 'rb') as zip_file:
            response = HttpResponse(zip_file.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename={zip_filename}'
    
        # Optionally, you can delete the ZIP file after sending it to the user
        os.remove(zip_path)

        Reports.objects.create(user=request.user,folder_name=folder.name,action='Downloaded')

        return response
    

class RegisterView(View):

    def get(self,request,*args,**kwargs):

        form = RegisterForm()

        data = {'form':form}

        return render(request,'register.html',context=data)
    
    def post(self,request,*args,**kwargs):

        form = RegisterForm(request.POST)

        if form.is_valid():

            first_name = form.cleaned_data.get('first_name')

            last_name = form.cleaned_data.get('last_name')

            email = form.cleaned_data.get('email')

            password = form.cleaned_data.get('password')

            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email,username=email, password=password)

            return redirect('login')
                 
        data = {'form':form}

        return render(request,'register.html',context=data)


class ReportsListView(View):

    def get(self,request,*args,**kwargs):

        user = request.user

        reports = Reports.objects.filter(user=user).order_by('-action_date_time')

        data = {'reports':reports}

        return render(request,'reports.html',context=data)