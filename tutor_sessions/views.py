from django.db.transaction import commit
from django.shortcuts import render,redirect,  get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from users.models import User, TutorProfile 
from .models import BaseSession, BookedSession
from payments.models import Payment
from availablity.models import Availablity
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from availablity.models import TutorPackage
import uuid
from django.utils import timezone
import json
from users.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from notifications.utils import create_notification
import datetime
from django.utils import timezone
from payments.chapa import ChapaPayment 
from django.db import transaction

@login_required
def list_session(request):
    today = timezone.now()
    tomorrow = today + datetime.timedelta(days=1)
    if (request.user.role == 'tutor'):
        sessions = BookedSession.objects.filter(base_session__tutor=request.user)
        canceld_sessions = BookedSession.objects.filter(base_session__tutor=request.user).filter(status='cancelled')
        completed_sessions = BookedSession.objects.filter(base_session__tutor=request.user).filter(status='completed')
    else:
        sessions = BookedSession.objects.filter(base_session__student=request.user)
    upcoming_sessions = sessions.filter(start_time__gt=today).filter(start_time__lt=tomorrow)
    canceld_sessions = sessions.filter(status='cancelled')
    completed_sessions = sessions.filter(status='completed')

    up =upcoming_sessions.filter().first()
    if up:
        up.status='up_comming'
    return render(request,'sessions/session_manager.html', {"sessions":sessions,
                                                            'completed_sessions':completed_sessions,
                                                            'upcoming_sessions':upcoming_sessions,
                                                            'canceld_sessions':canceld_sessions})

@csrf_exempt
@login_required
def base_session_manager(request):
    user = request.user
    if (user.role == 'tutor'):
        base_session = BaseSession.objects.filter(tutor=user)
        booked_session = BookedSession.objects.filter(base_session__tutor=user)
    elif (user.role == 'student'):
        base_session = BaseSession.objects.filter(student=user)
        booked_session = BookedSession.objects.filter(base_session__student=user)

    context = {
        'base_session':base_session,
        'booked_session':booked_session,
        }
    if request.method == 'POST':
        id = request.POST.get('id')
        requestd_session = get_object_or_404(BaseSession,id=id )
        action = request.POST.get("action")


        if action == "accept":
            requestd_session.status = 'confirmed' 
            requestd_session.save()
        
            create_notification(
            recipient=requestd_session.student,
            user=requestd_session.student,
            type='session_confirmed',
            link= "{% url 'base_session_list' %}"
            )
        elif action == "decline":
            requestd_session.status = 'decline' 
            requestd_session.save()
            create_notification(
            recipient=requestd_session.student,
            user=requestd_session.student,
            type='session_declined',
            link= "{% url 'base_session_list' %}"
            )
        elif action == "cancel":
            requestd_session.status = 'cancel' 
            trailing_sessions = BookedSession.objects.filter(base_session=requestd_session)
            for ts in trailing_sessions:
                ts.status='cancelled'
                ts.save()
            requestd_session.save()

            create_notification(
            recipient=requestd_session.student,
            user=requestd_session.student,
            type='session_cancel',
            link= "{% url 'base_session_list' %}"
            )
    
    return render(request, 'sessions/base_session_manage.html',context)

@login_required
def base_session_detail(request, bs_id):
    bs = get_object_or_404(BaseSession, id=bs_id)
    booked_session = BookedSession.objects.filter(base_session=bs)
    context = {
        'bs':bs,
        'booked_session':booked_session
    }
    return render(request, 'sessions/_base_session_detail.html',context)


@login_required
def list_BaseSession(request):
    
    if (request.user.role == 'tutor'):
        base_session = BaseSession.objects.all() 
    else:
        base_session = BaseSession.objects.filter(student=request.user)
         
    return render(request,'student/pages/session_requests.html', {"base_session":base_session})

@login_required
def request_session(request, pkg_id):
    if request.user == 'tutor':
        return HttpResponseForbidden('login as a student to access students functonalities')
    pkg = get_object_or_404(TutorPackage, id=pkg_id)
    tutor = pkg.tutor
    tutor = get_object_or_404(User, id=pkg.tutor.id, role= 'tutor')
    tutor_profile = TutorProfile.objects.get(user=tutor)
    subjects = tutor_profile.subjects.split(',') # assumig for now subjects are comma separated
    print(subjects)
    if request.method=='POST':
        pkg_request = BaseSession.objects.create(
            student = request.user,
            tutor = tutor,
            subject_name =  request.POST.get('selected_subject',''),
            price = pkg.price,
            total_session = pkg.total_session,
            remaining_sessions =  pkg.total_session,
            session_duration = pkg.session_duration,
            total_hours = pkg.total_session*pkg.session_duration/60, # in hour
            remaining_hours = pkg.total_session*pkg.session_duration/60,
        )
        pkg_request.save()
        create_notification(
        recipient=tutor,
        user=request.user,
        type='session_request',
        link= "{% url 'base_session_list' %}"
    )
        return render(request,'status/page.html',{
            'success': True,
            'message': f"Your request has been sent. You will be notified with ${tutor}'s response ."
        })     
    return render(request,'status/page.html',{
                'error': True,
                'message': f'You Request submission has failed . '
            })
@login_required
def session_requests(request):
    
    if not request.user.role == 'tutor':
        return HttpResponseForbidden(request.user,'You are not allowd hear')
    requests = BaseSession.objects.filter(status='pending')
    
    return render(request, 'tutor/pages/requests.html', {'requests':requests})

# @csrf_exempt   
# def handle_request(request, req_id):    
#     if not request.user.role == 'tutor':
#         return HttpResponseForbidden('You are not allowed here')
#     requestd_session = get_object_or_404(BaseSession, id=req_id)

#     action = request.POST.get("action")
#     if action == "accept":
#         requestd_session.status = 'confirmed' 
#         requestd_session.save()
    
#         create_notification(
#         recipient=requestd_session.student,
#         user=request_session.student,
#         type='session_confirmed',
#         link= "{% url 'base_session_list' %}"
#         )
#         message = f"<div class='session-request'>✅ Request {req_id} accepted!</div>"
#     elif action == "decline":
#         requestd_session.status = 'decline' 
#         requestd_session.save()
#         message = f"<div class='session-request'>❌ Request {req_id} declined!</div>"
    
#     return HttpResponse(message)


@login_required
def book_sessions(request, base_id):
    # Check if the user is a tutor
    if getattr(request.user, 'role', '').lower() == 'tutor':
        return HttpResponseForbidden("Tutors cannot book sessions. Nice try though 😏")

    base_session = get_object_or_404(BaseSession, id=base_id)
    tutor = base_session.tutor
    student = base_session.student or request.user  # fallback if not assigned yet

    # Get availability safely
    avail_obj = Availablity.objects.filter(tutor=tutor).first()
    availablity = avail_obj.availablity if avail_obj and avail_obj.availablity else []

    # Generate booked slots (for rendering)
    booked_slots = BookedSession.objects.filter(base_session__tutor=tutor).values('start_time', 'end_time')
    booked_events = [
        {
            'start': slot['start_time'],
            'end': slot['end_time'],
            'title': 'Booked',
            'backgroundColor': '#dc3545',
            'borderColor': '#dc3545',
            'display': 'block'
        }
        for slot in booked_slots
    ]

    # Handle booking submission
    if request.method == 'POST':
        if base_session.status in ['Pending', 'Denied']:
            return HttpResponse("No active package found, please purchase one.", status=400)

        try:
            slot = json.loads(request.POST.get('selected_slot', '{}'))
            start, end = slot.get('start'), slot.get('end')
            if not start or not end:
                return JsonResponse({'error': 'Invalid slot data.'}, status=400)
    
            with transaction.atomic():
                # Create payment
                tx_ref = f"tutor_escrow_{uuid.uuid4().hex[:16]}"
                callback_url = request.build_absolute_uri(f'/sessions/payment/verify/{tx_ref}/')
                obj, payment = Payment.objects.get_or_create(
                    student=student,
                    tutor=tutor,
                    session=base_session,
                    amount=base_session.price,
                    status="pending",
                    refrence_id=tx_ref
                )

                # Initialize Chapa payment
                chapa = ChapaPayment()
                response = chapa.initialize_transaction(
                    email=request.user.email,
                    amount=base_session.price,
                    tx_ref=tx_ref,
                    first_name=request.user.first_name,
                    last_name=request.user.last_name,
                    callback_url=callback_url
                )

                if response and response.get('status') == 'success':
        # Create booked session
                    obj, booked_session = BookedSession.objects.get_or_create(
                        base_session=base_session,
                        start_time=start,
                        end_time=end,
                        schedule_date=start
                    )
                    obj, payment = Payment.objects.get_or_create(
                        student=student,
                        tutor=tutor,
                        session=base_session,
                        amount=base_session.price,
                        status="pending",
                        refrence_id=tx_ref
                    )

                    checkout_url = response['data']['checkout_url']
                    
                    create_notification(
                    recipient=tutor,
                    user=request.user,
                    type='payment_confirmed',
                    link= "{% url 'base_session_list' %}")
                    return render(request, 'payment/redirect.html' ,{'checkout_url':checkout_url,'booked_session':booked_session})
                    
                else:
                    # Payment initialization failed
                    # payment.status = "failed"
                    # payment.save()
                    
                    return HttpResponse("Failed to initialize payment. Please try again later.", status=500)

        except Exception as e:
            return render(request,'status/page.html',{
                        'error': True,
                        'message': f'Failed Booking Process, Please Start again'
        })
    context = {     
        'tutor': tutor,
        'availablity_json': json.dumps(availablity),
        'booked_json': json.dumps(booked_events)
    }
    return render(request, 'student/pages/book.html', context)



@login_required 
def session_reschedule(request, session_id):
    booked_session = get_object_or_404(BookedSession, id=session_id)
    tutor = booked_session.base_session.tutor

    # Fetch tutor's availability safely
    avail_obj = Availablity.objects.filter(tutor=tutor).first()
    availablity = avail_obj.availablity if avail_obj and avail_obj.availablity else []

    # Get all booked sessions for this tutor (exclude current one if you want)
    booked_slots = BookedSession.objects.filter(base_session__tutor=tutor).values(
        'start_time', 'end_time'
    )

    booked_events = [
        {
            'start': slot['start_time'],
            'end': slot['end_time'],
            'title': 'Booked',
            'backgroundColor': '#dc3545',
            'borderColor': '#dc3545',
            'display': 'block'
        }
        for slot in booked_slots
    ]

    user = request.user
    if user not in [booked_session.base_session.student, booked_session.base_session.tutor]:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        with transaction.atomic():
            if booked_session.status in ['scheduled', 'rescheduled']:
                slot = json.loads(request.POST.get('selected_slot', '{}'))
                start = slot.get('start')
                end = slot.get('end')

                if not start or not end:
                    return JsonResponse({'error': 'Invalid slot data'}, status=400)

                booked_session.start_time = start
                booked_session.end_time = end
                booked_session.schedule_date = start
                booked_session.status = 'rescheduled'
                
                booked_session.save()
                recipient = booked_session.base_session.student if request.user == booked_session.base_session.tutor else booked_session.base_session.student
                create_notification(
                recipient=recipient,
                user=request.user,
                type='session_confirmed',
                link= "{% url 'base_session_list' %}")
                return redirect('session_list')

    context = {
        'tutor': tutor,
        'availablity_json': json.dumps(availablity),
        'booked_json': json.dumps(booked_events),
    }
    return render(request, 'sessions/reschedule.html', context)

def cancel_schedule(request, session_id):
    booked_session = get_object_or_404(BookedSession, id=session_id)
    user = request.user
    if user not in [booked_session.base_session.student, booked_session.base_session.tutor]:
        return HttpResponse("You're not supposed to do that 😒", status=403)


    if request.method:
        booked_session.status = 'cancelled'
        booked_session.start_time=''
        booked_session.end_time=''
        booked_session.save()

        recipient = booked_session.base_session.student if request.user == booked_session.base_session.tutor else booked_session.base_session.student
        create_notification(
        recipient=recipient,
        user=request.user,
        type='session_cancel',
        link= "{% url 'base_session_list' %}")
        return redirect('check_in_out')

    return render(request, 'session/session_detail.html',{'session':booked_session})
        
@csrf_exempt
def payment_verification(request, tx_ref):
    """Handle payment verification after Chapa redirect"""
    payment = get_object_or_404(Payment, refrence_id=tx_ref)
    
    # Verify payment with Chapa
    chapa = ChapaPayment()
    verification = chapa.verify_transaction(tx_ref)
    
    if verification and verification.get('status') == 'success':
        payment_data = verification['data']
        payment.transaction_id = payment_data.get('id')
        payment.status = 'success'  # Funds now held by platform
        payment.save()
        
        # Update booking status
        payment.session.is_payed = True
        payment.session.save()
        
        return redirect("payment_success", tx_ref=tx_ref)
    else:
        # Payment failed
        payment.status = 'failed'
        payment.save()
        payment.booking.status = 'cancelled'
        payment.booking.save()
        
        return redirect("payment_failed", tx_ref=tx_ref)

 
# @csrf_exempt
# @require_POST
# def chapa_webhook(request):
#     """Handle Chapa webhook for payment status updates"""
#     try:
#         data = json.loads(request.body)
#         tx_ref = data.get('tx_ref')
#         status = data.get('status')
        
#         if not tx_ref or not status:
#             return JsonResponse({'status': 'error', 'message': 'Missing parameters'}, status=400)
        
#         # Get payment and virtual account records
#         payment = get_object_or_404(Payment, tx_ref=tx_ref)
         
#         if status == 'successful':
#             # Verify transaction with Chapa
#             chapa = ChapaPayment()
#             verification = chapa.verify_transaction(tx_ref)
            
#             if verification and verification.get('status') == 'success':
#                 payment_data = verification['data']
#                 payment.chapa_transaction_id = payment_data.get('id')
#                 payment.status = 'held_in_escrow'  # Funds are held in virtual account
#                 payment.save()
                
#                 # Update booking status
#                 payment.booking.status = 'confirmed'
#                 payment.booking.save()
                
#                 return JsonResponse({'status': 'success'})
        
#         # Handle failed transactions
#         payment.status = 'failed'
#         payment.save()
#         payment.booking.status = 'cancelled'
#         payment.booking.save()
        
#         return JsonResponse({'status': 'success'})
    
#     except Exception as e:
#         print(f"Webhook error: {e}")
#         return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
# #start of sesion check_In and End of session check_Out View

