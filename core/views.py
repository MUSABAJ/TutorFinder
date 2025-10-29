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
from chat.models import Chat
def index(request):
     return render(request,'index/index.html')
    

def get_tutor_dashboard_context(user):
    """Returns all common tutor dashboard context data."""
    today = timezone.now()
    tutor = TutorProfile.objects.filter(user=user).first()
    sessions = BookedSession.objects.all()
    bookings = BaseSession.objects.filter(tutor=user)
    earning = Payment.objects.filter(tutor=user)
    feedback = FeedBack.objects.filter(tutor=user)
    upcoming_sessions = sessions.filter(start_time__gt=today)
    avg_rating = FeedBack.get_tutor_average(user)
    chats = Chat.objects.filter(participants=user).order_by('-created_at')

    return {
        'user': user,
        'tutor': tutor,
        'sessions': sessions,
        'upcoming_sessions': upcoming_sessions,
        'avg_rating': avg_rating,
        'bookings': bookings,
        'earning': earning,
        'feedback': feedback,
        'chats': chats,
    }

@login_required(login_url='/user/login/')
def tutor_dashbord(request):
     if not request.user.role == 'tutor':
          return HttpResponseBadRequest('Please contact the Admin 9858')
     context = get_tutor_dashboard_context(request.user)
     return render(request, 'dashboard/dashboard.html',context)

 
@login_required(login_url='/user/login/')
def manage_session(request):
     context = get_tutor_dashboard_context(request.user)
     return render(request,'common/session_manager.html',context)


@login_required(login_url='/user/login/')
def my_students(request):
     context = get_tutor_dashboard_context(request.user)
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
def notification(request): 
        tutor = request.user
        packages = TutorPackage.objects.filter(tutor=tutor)         
 
        context = {
            'packages':packages, 
            'tutor':tutor,}
        context.update(get_tutor_dashboard_context(request.user))
        return render(request, 'tutor/pages/notifications.html/',context)

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
     return render(request, 'common/profile_settings.html',context)



'''-----------------------------------------------Student VIew seciton--------------------------------------'''


@login_required(login_url='/user/login/')
def student_dashbord(request):
     if not request.user.role == 'student':
          return HttpResponseBadRequest('Please contact the Admin 9858')
     context = get_tutor_dashboard_context(request.user)
     return render(request, 'dashboard/dashboard.html',context)


@login_required(login_url='/user/login/')
def my_tutors(request):
     user = request.user
     exolore_tutor = TutorProfile.objects.all()
     ctx = {'exp_tutors':exolore_tutor}
     context = get_tutor_dashboard_context(request.user)
     context.update(ctx)
     return render(request,'student/pages/tutors.html',context)
# 
# Redundunt function , combine it with the session manager view and commonn html template
@login_required(login_url='/user/login/')
def my_sessions(request):
     context = get_tutor_dashboard_context(request.user)
     return render(request,'common/session_manager.html',context)

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


 