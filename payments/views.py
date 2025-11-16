from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from decimal import Decimal, InvalidOperation
from django.db.models import Sum
from notifications.models import Notification
from .models import Payment
from .chapa import ChapaPayment
from users.models import TutorProfile
from notifications.utils import send_telegram_message, create_notification
import time


# @login_required
def payment_success(request, tx_ref):
    payment = get_object_or_404(Payment, refrence_id=tx_ref)
    
    context = {
        "payment": payment,
        "title": "Payment Successful "
    }
    return render(request, "payment/success.html", context)

# @login_required
def payment_failed(request, tx_ref=None):
    payment = None
    if tx_ref:
        payment = Payment.objects.filter(refrence_id=tx_ref).first()

    context = {
        "payment": payment,
        "title": "Payment Failed "
    }
    return render(request, "payment/failed.html", context)

@login_required(login_url='/user/login/')
def withdraw_request(request):
   
    user = request.user
    if not getattr(user, 'role', None) == 'tutor':
        return HttpResponseBadRequest('Only tutors can request withdrawals')

    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')

    amount_raw = request.POST.get('amount') 
    if not amount_raw:
        return JsonResponse({'error': 'Missing amount parameter'}, status=400)

    try:
        amount = Decimal(str(amount_raw))
    except (InvalidOperation, TypeError, ValueError):
        return JsonResponse({'error': 'Invalid amount'}, status=400)

    if amount <= 0:
        return JsonResponse({'error': 'Amount must be greater than zero'}, status=400)

    # compute available released balance for the tutor
    released_total = Payment.objects.filter(tutor=user, status='released').aggregate(total=Sum('amount'))['total'] or Decimal('0')

    if amount > released_total:
        return JsonResponse({'error': 'Insufficient released balance'}, status=400)

    # build chapa payload from tutor profile
    tutor_profile = get_object_or_404(TutorProfile, user=user)
    account_type = (tutor_profile.account_type or '').lower()
    account_number = tutor_profile.account_number
    bank_code = tutor_profile.bank_code

    reference = f"withdraw_{user.id}_{int(time.time())}"

    chapa = ChapaPayment()

    try:
        
        chapa_resp = chapa.transfer_to_bank(account_number=account_number, amount=amount, bank_code=bank_code)
    except Exception as e:
        chapa_resp = None
        print(f"Chapa transfer exception: {e}")

    # basic success detection (Chapa responses vary; be defensive)
    success = False
    if chapa_resp and isinstance(chapa_resp, dict):
        # common keys: 'status' or 'success' or 'data'
        status_val = chapa_resp.get('status') or chapa_resp.get('status_code') or chapa_resp.get('success')
        if isinstance(status_val, str) and status_val.lower() in ('success', 'ok', 'completed'):
            success = True
        elif isinstance(status_val, (int,)) and status_val == 200:
            success = True
        elif chapa_resp.get('data') and chapa_resp.get('data').get('status') == 'success':
            success = True

    message = ''
    if success:
        released_total = Payment.objects.filter(tutor=user, status='released')
        for released in released_total:
            if released.amount <= amount:
                released.amount -= released.amount
                amount-= released.amount
            if released.amount > amount:
                released.amount -= amount
            if amount==0:
                break

            released.save()
        message = f"Your withdrawal request of {amount} ETB has been submitted. Reference: {reference}."
        n = Notification.objects.create(recipient=user, message=message)
        send_telegram_message(getattr(user, 'telegram_id', None), message)
        return render(request,'status/page.html',{
            'success': True,
            'message': message
        })     
    else:
        # failure path
        message = f"Withdrawal of {amount} ETB failed to initiate. Please try again later."
        n = Notification.objects.create(recipient=user, message=message)
        send_telegram_message(getattr(user, 'telegram_id', None), message)
        return render(request,'status/page.html',{
                    'success': False,
                    'message': message
        })  