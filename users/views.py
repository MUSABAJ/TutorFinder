import re
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import TutorProfile, StudentProfile, User
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.hashers import check_password

#---------------------- USER CRUD VIEW  ------------------------------
         
      
def tutor_register(request):
    if request.user.is_authenticated:
        if request.user.role == 'tutor':
            return redirect('tutor_dashbord')
        else:
            return redirect('student_dashboard')
    if request.method=='POST':
        form = TutorRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'tutor'
            user.save() 

            TutorProfile.objects.create(
                user = user, 
                horuly_rate = form.cleaned_data['horuly_rate'],
                qualification = form.cleaned_data['qualification'],
                experience =  form.cleaned_data['experience'],
               teaching_prefrence =  form.cleaned_data['teaching_prefrence'],
                subjects =  form.cleaned_data['subjects'],                 
            )
            return redirect('tutor_dashbord')
        
    else:
        form = TutorRegisterForm()
        context = {'form': form, 'role':User.role}

    return render(request, 'auth/tutor_reg.html', {'tutor_form': form})


def student_register(request):
    if request.user.is_authenticated:
        if request.user.role == 'tutor':
            return redirect('tutor_dashbord')
        else:
            return redirect('student_dashboard')
    
    if request.method=='POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student'
            user.save()

            StudentProfile.objects.create(
                user = user,
                favorite = 'something'
            )
 
            # login(request,user)
            return redirect ('student_dashboard')
    else:
        form = StudentRegisterForm()
    return render(request, 'auth/student_reg.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'tutor':
            return redirect('tutor_dashbord')
        else:
            return redirect('student_dashboard')
    if request.method=='POST':
        form = loginForm(request.POST, data=request.POST)
        username = request.POST.get('username')
        pwd = request.POST.get('password')
         
        user = authenticate(request, username=username, password=pwd)
        if user is not None:
            login(request, user)
            if request.user.role == 'tutor':
                 return redirect('tutor_dashbord')
            else:
                return redirect('student_dashboard')
    else:
 
        form =loginForm()
        context = {'form': form}
    return render(request, 'auth/auth.html', {'form': form})
    


def logout_view(request):
    logout(request)
    return redirect('login')


def avatar_update(request):
    if request.method == 'POST':
        avatar_form = AvatarForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    form = AvatarForm(instance=request.user)
    return render(request, 'include/_avartar_form.html',{'avatar_form':form})


# def add_certificate(request):
#     tutor = TutorProfile.objects.get(user=request.user)
#     if request.method == 'POST':
#         form = CertificateForm(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     form = CertificateForm()  
#     return render(request,'profile_update_html',{'form':form})

# def change_password(request):
#     user = request.user
#     if request.method == 'POST':
#             passwordForm = ChangePasswordForm(request.POST, instance=user)
#             passwordForm.is_valid()
#             passwordForm.save()
#             return redirect('profile')
#     passwordForm = change_password(instance=user)
#     return render(request,'/profile.html',{'passwordForm':passwordForm})

def delete_account(request):
    if request.method == 'POST':
        pwd = request.POST.get('password','')
        if check_password(pwd,request.user.password):
            request.user.delete()
            return redirect('index')
        # messages.error(request,"password incorect")
    return render(request,'user/setting_delete_account_html')

def profile_view(request, id):
    user = get_object_or_404(User, id=id)
    context = {'user':user} 
    if user.role == 'tutor':
        tutor = TutorProfile.objects.get(user=user)
        context = {'user':user,
                   'tutor':tutor} 
    return render(request, 'profile_view.html', context)

def payment_info_form(request):
    if request.method == 'POST':
        user = TutorProfile.objects.get(user=request.user)
        user.account_type = request.POST.get('method_type')
        if user.account_type == 'bank':
            user.bank_code = request.POST.get('bank_code')
            user.account_number = request.POST.get('account_number')
        if user.account_type == 'mobile':
            user.bank_code = request.POST.get('mobile_provider')
            user.account_number = request.POST.get('phone_number')
        if user.account_type == 'card':
            user.bank_code = request.POST.get('card_name')
            user.account_number = request.POST.get('card_number')
            # user.bank_code = request.POST.get('card_expiry')
            # user.account_number = request.POST.get('card_cvc')

        user.save()
        return redirect('my_profile')
 