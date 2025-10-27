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
from django.contrib import messages
from .forms import BookingForm
import uuid
from django.utils import timezone
import json
from users.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from payments.chapa import ChapaPayment 

@login_required
def list_session(request):
    if (request.user.role == 'tutor'):
        sessions = BookedSession.objects.filter(base_session__tutor=request.user)
    else:
        sessions = BookedSession.objects.filter(base_session__tutor=request.session)
    return render(request,'session/session_list.html', {"sessions":sessions})

@login_required
def list_BaseSession(request):
    
    if (request.user.role == 'tutor'):
        base_session = BaseSession.objects.all()
    else:
        base_session = BaseSession.objects.filter(studet=request.tutor)
    return render(request,'session/base_session.html', {"base_sessions":base_session})

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
        request = BaseSession.objects.create(
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
        request.save()
        return JsonResponse('success page', safe=False)
     
    return JsonResponse( 'error', safe=False)

@login_required
def session_requests(request):
    
    if not request.user.role == 'tutor':
        return HttpResponseForbidden(request.user,'You are not allow hear')
    requests = BaseSession.objects.filter(status='pending')
    
    return render(request, 'tutor/pages/requests.html', {'requests':requests})

@csrf_exempt   
def handle_request(request, req_id):    
    if not request.user.role == 'tutor':
        return HttpResponseForbidden('You are not allowed here')
    requestd_session = get_object_or_404(BaseSession, id=req_id)

    action = request.POST.get("action")
    if action == "accept":
        requestd_session.status = 'confirmed' 
        requestd_session.save()

        message = f"<div class='session-request'>✅ Request {req_id} accepted!</div>"
    elif action == "decline":
        requestd_session.status = 'decline' 
        requestd_session.save()
        message = f"<div class='session-request'>❌ Request {req_id} declined!</div>"
    
    return HttpResponse(message)


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

            # Create booked session
            booked_session = BookedSession.objects.create(
                base_session=base_session,
                start_time=start,
                end_time=end,
                schedule_date=start
            )

            # Create payment
            tx_ref = f"tutor_escrow_{uuid.uuid4().hex[:16]}"
            callback_url = request.build_absolute_uri(f'/sessions/payment/verify/{tx_ref}/')
            payment = Payment.objects.create(
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
                # Don’t mark success yet! Wait for callback verification
                checkout_url = response['data']['checkout_url']
                return redirect(checkout_url)
            else:
                # Payment initialization failed
                payment.status = "failed"
                payment.save()
                return HttpResponse("Failed to initialize payment. Please try again later.", status=500)

        except Exception as e:
            print("Booking error:", e)
            return JsonResponse({'error': str(e)}, status=500)

    context = {     
        'tutor': tutor,
        'availablity_json': json.dumps(availablity),
        'booked_json': json.dumps(booked_events)
    }
    return render(request, 'student/pages/buy_package.html', context)


@login_required
def check_in_out(request, session_id):
    session = get_object_or_404(BaseSession, id=session_id) 
    user = request.user
    if user not in [session.student,session.tutor]:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    button = 'Rate Your Session'
    if session.status == 'confirmed' or session.status == 'ongoing':
        session.start_session()
        button = 'End Session'
    elif session.status == 'active':
        session.end_session()
        button = 'Start Session'

    context = {'session': session, 'button':button}
    return render(request, 'session/session_detail.html', context)

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

            return redirect('check_in_out')

    context = {
        'tutor': tutor,
        'availablity_json': json.dumps(availablity),
        'booked_json': json.dumps(booked_events),
    }
    return render(request, 'session/reschedule.html', context)

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

