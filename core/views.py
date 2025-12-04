from django.contrib.auth.decorators import login_required
from django.http import request, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from users.forms import TutorProfileEditForm,StudentProfileEditForm, UserProfileEditForm, AvatarForm
from tutor_sessions.models import BaseSession, BookedSession
from notifications.models import Notification
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
    if user.role== 'studetn':
       sessions = BookedSession.objects.filter(base_session__student=user)
    else:
       sessions = BookedSession.objects.filter(base_session__student=user)
    upcoming_sessions = sessions.filter(start_time__gt=today).filter(start_time__lt=tomorrow)
    chats = Chat.objects.filter(participants=user).order_by('-created_at')
     
    return {
        'user': user,
        'sessions': sessions,
        'upcoming_sessions': upcoming_sessions,
        'chats': chats,
    }

@login_required(login_url='/user/login/')
def tutor_dashbord(request):
     if request.user.role == 'student':
          return redirect('student_dashboard')
     
     if request.user.role == 'admin':
          return redirect("/admin")
     
 
     avg_rating = FeedBack.get_tutor_average(request.user)
     total_earnings = Payment.total_earnings(self=request.user)
     pending_balance = Payment.pending_balance(self=request.user)
     ctx = {'total_earning':total_earnings, 'pending_balance':pending_balance,'avg_rating':avg_rating}
     context = get_tutor_dashboard_context(request.user)
     context.update(ctx)
     return render(request, 'dashboard/dashboard.html',context)



@login_required(login_url='/user/login/')
def my_students(request):
     
     if request.user.role != 'tutor':
          return HttpResponseBadRequest('Very Bad Reqeuest')
     context = get_tutor_dashboard_context(request.user)
     my_students = User.objects.filter(chats__participants=request.user, role='student').distinct()
     context.update( {'my_students':my_students})
     return render(request,'tutor/pages/my_students.html',context)

@login_required(login_url='/user/login/')
def manage_package(request): 
     
     if request.user.role != 'tutor':
          return HttpResponseBadRequest('Very Bad Reqeuest')
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
     if request.user.role != 'tutor':
          return HttpResponseBadRequest('Very Bad Reqeuest')
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
     
     if request.user.role != 'tutor':
          return HttpResponseBadRequest('Very Bad Reqeuest')
     student = get_object_or_404(StudentProfile, id=student_id)
     context = {'student':student}
     return render(request, 'tutor/pages/student_view.html',context)



'''-----------------------------------------------Student VIew seciton--------------------------------------'''


@login_required(login_url='/user/login/')
def student_dashbord(request):
     if request.user.role == 'tutor':
          return redirect('tutor_dashbord')
     if request.user.role == 'admin':
          return redirect('/admin')
     next_session = BookedSession.objects.filter(base_session__student=request.user).order_by('-start_time')[:1]
     notif = Notification.objects.filter(recipient=request.user).count
     accepted_sess = BaseSession.objects.filter(student=request.user).filter(status='confirmed')
     declined_sess = BaseSession.objects.filter(student=request.user).filter(status='decline')
     suggested_tutors = TutorProfile.objects.filter(rating__gte=3.0)[:10] if TutorProfile.objects.filter(rating__gte=3.0) else  TutorProfile.objects.all()[:10]

     context = get_tutor_dashboard_context(request.user)
     ctx = {'suggested_tutors':suggested_tutors,
            'next_session':next_session,
            'accepted_sess':accepted_sess, 
            'notif':notif, 
            'declined_sess':declined_sess}
     context.update(ctx)
     return render(request, 'dashboard/dashboard.html',context)

from chat.models import Message
@login_required(login_url='/user/login/')
def my_tutors(request):
     
     if request.user.role != 'student':
          return HttpResponseBadRequest('Very Bad Reqeuest')
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
     
     if request.user.role != 'student':
          return HttpResponseBadRequest('Very Bad Reqeuest')
     tutor = get_object_or_404(TutorProfile, id=tutor_id)
     packages = TutorPackage.objects.filter(tutor=tutor.user)
     tutor_profile = TutorProfile.objects.get(user=tutor.user)
     subjects = tutor_profile.subjects.split(',') # assumig for now subjects are comma separated
     subjects = [s.strip() for s in subjects] 

     context = {'tutor':tutor
                ,'packages':packages
                ,'subjects':subjects}
     return render(request, 'student/pages/tutor_view.html',context)

def payment_history(request):
     
     if request.user.role != 'student':
          return HttpResponseBadRequest('Very Bad Reqeuest')
     student = request.user
     sessions = BaseSession.objects.filter(student=student)
     payments = Payment.objects.filter(student=student)
     
     status_totals_qs = payments.values('status').annotate(total=Sum('amount'))
     status_totals = {item['status']: item['total'] or 0 for item in status_totals_qs}

     held_payment = status_totals.get('held', 0)
     total_spent = payments.aggregate(total=Sum('amount'))['total'] or 0

     transactions = payments.order_by('-created_at')

     context = {
          'held_payment': held_payment,
           'total_spent': total_spent,
          'transactions': transactions,
          'sessions': sessions,
           'student': student,
     }
     context.update(get_tutor_dashboard_context(request.user))
     return render(request, 'student/pages/payment_history.html', context)
#---------------------------------- Ssearch and filters-----------------------------------#



def main_serach(request):
     
     if request.user.role != 'student':
          return HttpResponseBadRequest('Very Bad Reqeuest')
     search_text = request.GET.get("search_text", "")
     search_text = urllib.parse.unquote(search_text).strip()


     if search_text:         

          tutors = TutorProfile.objects.filter(
               Q(user__first_name__icontains=search_text)
               | Q(user__last_name__icontains=search_text)
               | Q(user__username__icontains=search_text)
          )
          context = {'tutors':tutors}
          return render(request, 'search/_results.html',context)

def tutor_serach(request):
     
     if request.user.role != 'student':
          return HttpResponseBadRequest('Very Bad Reqeuest')
     tutors_profile = TutorProfile.objects.all()
     search_text = request.GET.get("search_text", "")
     search_text = urllib.parse.unquote(search_text).strip()
     subject = request.GET.get("subject","")
     gender = request.GET.get("gender_filter","")
     rating = request.GET.get("rating","")
     language = request.GET.get("rating","")
     hr_rate = request.GET.get("hr_rate","")
     expirience = request.GET.get("expirience","")
     avail = request.GET.get("avail", "")
     tutors = tutors_profile
     if search_text:         

          tutors = tutors_profile.filter(
               Q(user__first_name__icontains=search_text)
               | Q(user__last_name__icontains=search_text)
               | Q(user__username__icontains=search_text)
          )

     if subject:
          tutors = tutors_profile.filter(subjects__icontains=subject)
     # if avail:
     #      tutors = tutors_profile.filter(available=True)

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
     
     if request.user.role != 'student':
          return HttpResponseBadRequest('Very Bad Reqeuest')
     search_text = request.GET.get("search_text","")
     my_tutors = User.objects.filter(
     chats__participants=request.user,    
     role='tutor'                        
     ).distinct()   

     if search_text:
          my_tutors = my_tutors.filter(
          Q( first_name__icontains=search_text)
          | Q( last_name__icontains=search_text)
          | Q(username__icontains=search_text)
     )
     context = {'my_tutors':my_tutors}
          
     return render(request, 'student/partials/_myTtutor_serach.html', context)
