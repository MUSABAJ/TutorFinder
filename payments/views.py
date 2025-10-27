from django.shortcuts import render, get_object_or_404
from .models import Payment

# @login_required
def payment_success(request, tx_ref):
    payment = get_object_or_404(Payment, refrence_id=tx_ref)
    
    context = {
        "payment": payment,
        "title": "Payment Successful 💚"
    }
    return render(request, "payment/success.html", context)

# @login_required
def payment_failed(request, tx_ref=None):
    payment = None
    if tx_ref:
        payment = Payment.objects.filter(refrence_id=tx_ref).first()

    context = {
        "payment": payment,
        "title": "Payment Failed 💔"
    }
    return render(request, "payment/failed.html", context)
