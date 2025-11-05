from django.contrib.auth.decorators import login_required
from django.http import request, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from users.forms import TutorProfileEditForm,StudentProfileEditForm, UserProfileEditForm, AvatarForm
from tutor_sessions.models import BaseSession, BookedSession
from feedback.models import FeedBack
from resources.models import Resource
from availablity.models import TutorPackage
from availablity.forms import PackageForm
from users.models import User, TutorProfile, StudentProfile
from payments.models import Payment
from django.utils import timezone 
from django.db.models import Q
import datetime
import urllib
from chat.models import Chat
def index(request):
     return render(request,'index/index.html')
    

def get_tutor_dashboard_context(user):
    """Returns all common tutor dashboard context data."""
    today = timezone.now()
    tomorrow = timezone.now() + datetime.timedelta(days=1)
    tutor = TutorProfile.objects.filter(user=user).first()
    sessions = BookedSession.objects.all()
    bookings = BaseSession.objects.filter(tutor=user)
    earning = Payment.objects.filter(tutor=user)
    feedback = FeedBack.objects.filter(tutor=user)
    upcoming_sessions = sessions.filter(start_time__gt=today).filter(start_time__lt=tomorrow)
    avg_rating = FeedBack.get_tutor_average(user)
    chats = Chat.objects.filter(participants=user).order_by('-created_at')
     
    return {
        'user': user,
        'tutor': tutor,
        'sessions': sessions,
        'upcoming_sessions': upcoming_sessions,
     #    'avg_rating': avg_rating,
     #    'bookings': bookings,
     #    'earning': earning,
     #    'feedback': feedback,
        'chats': chats,
    }

@login_required(login_url='/user/login/')
def tutor_dashbord(request):
     if not request.user.role == 'tutor':
          return HttpResponseBadRequest('Please contact the Admin 9858')
     context = get_tutor_dashboard_context(request.user)
     return render(request, 'dashboard/dashboard.html',context)

 
# @login_required(login_url='/user/login/')
# def manage_session(request):
#      context = get_tutor_dashboard_context(request.user)
#      return render(request,'sessions/session_manager.html',context)


@login_required(login_url='/user/login/')
def my_students(request):
     

     context = get_tutor_dashboard_context(request.user)
     context.update({'sessions' :BaseSession.objects.filter(tutor=request.user)})
     # use chats and join with base session to eliminate redundunt students with multiple BaseSession
     return render(request,'tutor/pages/my_students.html',context)

@login_required(login_url='/user/login/')
def manage_package(request): 
     tutor = request.user
     packages = TutorPackage.objects.filter(tutor=tutor)         
     if request.method == 'POST':
          form = PackageForm(request.POST)
          if form.is_valid():

               pkg = form.save(commit=False)
               pkg.tutor = request.user
               pkg.save()
               
     form = PackageForm()
     context = {
          'packages':packages, 
          'form':form,
          'tutor':tutor,}
     context.update(get_tutor_dashboard_context(request.user))
     return render(request, 'tutor/pages/manage_package.html/',context)

 
@login_required(login_url='/user/login/')
def earning(request): 
        tutor = request.user
        packages = TutorPackage.objects.filter(tutor=tutor)         
 
        context = {
            'packages':packages, 
            'tutor':tutor,}
        context.update(get_tutor_dashboard_context(request.user))
        return render(request, 'tutor/pages/earning.html/',context)

@login_required(login_url='/user/login/')
def tutor_profile(request): 
     user = request.user
    
     user_form = UserProfileEditForm(request.POST or None, instance=user)
     tutor_form = None
     student_form  = None
     if user.role == 'tutor':
        tutor_data = get_object_or_404(TutorProfile, user=user)
        tutor_form = TutorProfileEditForm(request.POST or None, request.FILES or None, instance=tutor_data)

     elif user.role == 'student':
          student_data = get_object_or_404(StudentProfile, user=user)
          student_form = StudentProfileEditForm(request.POST or None, instance=student_data)
       
        

     if request.method == 'POST':
        if user_form.is_valid():
            user_form.save()

            if tutor_form and tutor_form.is_valid():
                tutor_form.save()

            if student_form and student_form.is_valid():
                student_form.save()
                return redirect('tutor_profile')
     context = {
        'user_form': user_form,
        'tutor_form': tutor_form,
        'student_form': student_form,
    }
     return render(request, 'sessions/profile_settings.html',context)



'''-----------------------------------------------Student VIew seciton--------------------------------------'''


@login_required(login_url='/user/login/')
def student_dashbord(request):
     if not request.user.role == 'student':
          return HttpResponseBadRequest('Please contact the Admin 9858')
     context = get_tutor_dashboard_context(request.user)
     return render(request, 'dashboard/dashboard.html',context)

from chat.models import Message
@login_required(login_url='/user/login/')
def my_tutors(request):
     exolore_tutor = TutorProfile.objects.all()
     my_tutors = User.objects.filter(
     chats__participants=request.user,    
     role='tutor'                        
     ).distinct()      

     ctx = {'exp_tutors':exolore_tutor,'my_tutors':my_tutors}
     context = get_tutor_dashboard_context(request.user)
     context.update(ctx)
     return render(request,'student/pages/tutors.html',context)
# 
# Redundunt function , combine it with the session manager view and commonn html template
# @login_required(login_url='/user/login/')
# def my_sessions(request):
#      context = get_tutor_dashboard_context(request.user)
#      return render(request,'sessions/session_manager.html',context)

def view_tutor(request, tutor_id):
     tutor = get_object_or_404(TutorProfile, id=tutor_id)
     packages = TutorPackage.objects.filter(tutor=tutor.user)
     tutor_profile = TutorProfile.objects.get(user=tutor.user)
     subjects = tutor_profile.subjects.split(',') # assumig for now subjects are comma separated
     print(subjects)
     context = {'tutor':tutor
                ,'packages':packages
                ,'subjects':subjects}
     return render(request, 'student/pages/tutor_view.html',context)


#---------------------------------- Ssearch and filters-----------------------------------#



def main_serach(request):

     search_text = request.GET.get("search_text", "")
     search_text = urllib.parse.unquote(search_text).strip()
     print(search_text)
     print(request.GET.get)

     if search_text:         

          tutors = TutorProfile.objects.filter(
               Q(user__first_name__icontains=search_text)
               | Q(user__last_name__icontains=search_text)
               | Q(user__username__icontains=search_text)
          )
          context = {'tutors':tutors}
          return render(request, 'search/_results.html',context)

def tutor_serach(request):
     tutors_profile = TutorProfile.objects.all()
     search_text = request.GET.get("search_text", "")
     search_text = urllib.parse.unquote(search_text).strip()
     subject = request.GET.get("subject","")
     gender = request.GET.get("gender_filter","")
     rating = request.GET.get("rating","")
     language = request.GET.get("rating","")
     hr_rate = request.GET.get("hr_rate","")
     expirience = request.GET.get("expirience","")
     tutors = tutors_profile
     if search_text:         

          tutors = tutors_profile.filter(
               Q(user__first_name__icontains=search_text)
               | Q(user__last_name__icontains=search_text)
               | Q(user__username__icontains=search_text)
          )

     if subject:
          tutors = tutors_profile.filter(subjects__icontains=subject)
 
     if gender:
          tutors = tutors_profile.filter(user__gender=gender)
     if expirience:
          tutors = tutors_profile.filter(experience__gte=rating)
     if hr_rate:
          tutors = tutors_profile.filter(horuly_rate__gte=hr_rate)
     if rating:
          tutors = tutors_profile.filter(rating__gte=rating)
     if language:
          tutors = tutors_profile.filter(language__icontains=language)

     context = {'tutors':tutors}
     return render(request, 'student/partials/_tutor_search.html',context)
 
          
def my_tutor_search(request):
     search_text = request.GET.get("search_text","")
     my_tutors = User.objects.filter(
     chats__participants=request.user,    
     role='tutor'                        
     ).distinct() 
     print('----------------------------------------------------')     
     print(search_text)     

     if search_text:
          my_tutors = my_tutors.filter(
          Q( first_name__icontains=search_text)
          | Q( last_name__icontains=search_text)
          | Q(username__icontains=search_text)
     )
     context = {'my_tutors':my_tutors}
          
     return render(request, 'student/partials/_myTtutor_serach.html', context)
