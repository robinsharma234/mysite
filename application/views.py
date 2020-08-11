from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,logout,login
from django.shortcuts import render,redirect
from .models import Blog,Personal
from django.db import connection, transaction
from django.views.generic.base import View
from datetime import datetime

# Create your views here.

#index page
def index(request):
    data=Blog.objects.all()
    data=reversed(data) 
    context={'all_blog':data} 
    return render(request,'index.html',context)

#home user profile page...
def profile(request):
    #check if user is anonymous...
    if request.user.is_anonymous:
        return redirect('/')
    #to show all blogs in profile 
    # cursor = connection.cursor()
    # # cursor.execute("SELECT * FROM application_blog WHERE user_id=1")
    # cursor.execute("SELECT application_blog.text, application_blog.title,auth_user.username FROM auth_user INNER JOIN application_blog ON auth_user.id=application_blog.user_id WHERE application_blog.user_id=request.user.id;")
    # data = cursor.fetchall()
    
    data=Blog.objects.filter(user_id=request.user.id)
    data=reversed(data)
    pic_bio=Personal.objects.filter(uname=request.user.username)
    context={'all_blog':data,'pic_bio':pic_bio} 
    return render(request,'profile.html',context)

#to add new blog...
def add_blog(request):
    #to submit a new blog..
    if request.method=='POST':     
        title=request.POST.get('title')
        text=request.POST.get('desc')
        blog=Blog.objects.create(title=title,text=text,user_id=request.user.id,uname=request.user.username,date=datetime.now())
        blog.save()
        return redirect('/')
    else:
        return render(request,'add_blog.html')

def anotheruser(request,blog_uname=None):
    data=Blog.objects.filter(uname=blog_uname)
    userx=User.objects.get(username=blog_uname)
    try:
        userp=Personal.objects.get(uname=blog_uname)
    except:
        userp=None
    
    
    context={'all_blog':data,'userx':userx,'userp':userp}
    return render(request,'anotheruser.html',context)
#to delete current user post...
def delete_post(request,post_id=None):
    ids=Blog.objects.filter(pk=post_id)   
    ids.delete()
    return redirect('profile')

def delete_bio(request,pic_bio=None):
    
    ids=Personal.objects.filter(bio=pic_bio)
    ids.delete()
    return redirect('edit')
        
    return redirect('edit')
def edit(request):
    if request.method=='POST':
        picture=request.FILES['user_pic']
        bios=request.POST['user_bio']
        userp=request.user.username
        userx=Personal.objects.create(uname=userp,bio=bios,pic=picture)
        userx.save()
        return redirect('edit')

    uedit=Personal.objects.filter(uname=request.user.username)
    context={'y':uedit}
    return render(request,'edit.html',context)


#login is for login existing user...
def LoginUser(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        #check user is valid or not
        if user is not None:              
            login(request,user)
            return redirect('profile')
        else:
            return render(request,'login.html')
    
    else:
        return render(request,'login.html')


#signup to create new account....
def signup(request):
    if request.method=='POST':
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        if User.objects.filter(username=username).exists():
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            return redirect('signup')
        else:
            x=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
            x.save()
            return redirect('profile')
    return render(request,'signup.html')


#logout function....
def LogoutUser(request):
    logout(request)
    return redirect('/')

#this is about page 
def about(request):
    return render(request,'about.html')

#this is base template..
def base(request):
    return render(request,'base.html')
