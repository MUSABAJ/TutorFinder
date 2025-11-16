from django.contrib.auth.decorators import login_required
from django.http import request, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from users.forms import TutorProfileEditForm,StudentProfileEditForm, UserProfileEditForm, AvatarForm
from tutor_sessions.models import BaseSession, BookedSession
from feedback.models import FeedBack
from availablity.models import TutorPackage
from availablity.forms import PackageForm
from users.models import User, TutorProfile, StudentProfile
from payments.models import Payment
from payments.chapa import ChapaPayment
from django.utils import timezone 
from django.db.models import Q
from django.db.models import Sum
import datetime
import urllib
from chat.models import Chat
def index(request):
     return render(request,'index/index.html')
    

def get_tutor_dashboard_context(user):
    """Returns all common tutor dashboard context data."""
    today = timezone.now()
    tomorrow = timezone.now() + datetime.timedelta(days=1)
#     tutor = TutorProfile.objects.filter(user=user).first()
#     bookings = BaseSession.objects.filter(tutor=user)
#     earning = Payment.objects.filter(tutor=user)
#     feedback = FeedBack.objects.filter(tutor=user)
    sessions = BookedSession.objects.all()
    upcoming_sessions = sessions.filter(start_time__gt=today).filter(start_time__lt=tomorrow)
    chats = Chat.objects.filter(participants=user).order_by('-created_at')
     
    return {
        'user': user,
     #    'tutor': tutor,
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

     sessions = BookedSession.objects.all()
     earning = Payment.objects.filter(tutor=request.user)

     avg_rating = FeedBack.get_tutor_average(request.user)
     total_earnings = Payment.total_earnings(self=request.user)
     pending_balance = Payment.pending_balance(self=request.user)
     ctx = {'total_earning':total_earnings, 'pending_balance':pending_balance,'avg_rating':avg_rating}
     context = get_tutor_dashboard_context(request.user)
     context.update(ctx)
     return render(request, 'dashboard/dashboard.html',context)

 
# @login_required(login_url='/user/login/')
# def manage_session(request):
#      context = get_tutor_dashboard_context(request.user)
#      return render(request,'sessions/session_manager.html',context)


@login_required(login_url='/user/login/')
def my_students(request):
     
     context = get_tutor_dashboard_context(request.user)
     my_students = User.objects.filter(chats__participants=request.user, role='student').distinct()
     context.update( {'my_students':my_students})
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
     payments = Payment.objects.filter(tutor=tutor)
     
     status_totals_qs = payments.values('status').annotate(total=Sum('amount'))
     # convert to dict for easy access in template
     status_totals = {item['status']: item['total'] or 0 for item in status_totals_qs}

     held_payment = status_totals.get('held', 0)
     available_balance = status_totals.get('released', 0)
     total_earning = payments.aggregate(total=Sum('amount'))['total'] or 0

     transactions = payments.order_by('-created_at')

     context = {
          'held_payment': held_payment,
          'available_balance': available_balance,
          'total_earning': total_earning,
          'transactions': transactions,
          'status_totals': status_totals,
          'packages': packages,
          'tutor': tutor,
     }
     context.update(get_tutor_dashboard_context(request.user))
     return render(request, 'tutor/pages/earning.html', context)

@login_required(login_url='/user/login/')
def my_profile(request): 
     user = request.user
     avatar_form = AvatarForm(request.POST,request.FILES,instance=request.user)
     user_form = UserProfileEditForm(request.POST or None, instance=user)
     tutor_form = None
     student_form  = None

     if user.role == 'tutor':
        bank_list = ChapaPayment().bank_list()
        tutor_data = get_object_or_404(TutorProfile, user=user)
        tutor_form = TutorProfileEditForm(request.POST or None,request.FILES or None,   instance=tutor_data)
        ctx = {'tutor':tutor_data, 'bank_list':bank_list}
     elif user.role == 'student':
          student_data = get_object_or_404(StudentProfile, user=user)
          student_form = StudentProfileEditForm(request.POST or None, instance=student_data)
          ctx = {'student':student_data}
       
         
     if request.method == 'POST':
          if user_form.is_valid():
               user_form.save()
               
               if tutor_form and tutor_form.is_valid():
                    tutor_form.save()

               if student_form and student_form.is_valid():
                    student_form.save()
          if avatar_form.is_valid():
               avatar_form.save()
               return redirect('my_profile')

     context = {
        'user_form': user_form,
        'tutor_form': tutor_form,
        'student_form': student_form,
          'avatar_form':avatar_form

     }
     context.update(ctx)
     return render(request, 'sessions/profile_settings.html',context)


def view_student(request, student_id):
     student = get_object_or_404(StudentProfile, id=student_id)
     context = {'student':student}
     return render(request, 'tutor/pages/student_view.html',context)



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
