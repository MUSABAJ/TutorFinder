from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from notifications.utils import create_notification
from django.db.models import Avg
from .models import FeedBack
from .forms import FeedbackForm
from users.models import TutorProfile
from tutor_sessions.models import BaseSession
from django.contrib.auth.decorators import login_required


@login_required
def give_feedback(request, session_id):
    session = get_object_or_404(BaseSession, id=session_id)


    if session.student != request.user:
        return redirect('tutor_dashbord')


    if FeedBack.objects.filter(session=session, student=request.user).exists():
        return render(request,'status/page.html',{
            'error': True,
            'message': f'You already submitted feedback for this session. '
        })

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.rating = request.POST.get("rating","")
            feedback.session = session
            feedback.student = session.student
            feedback.tutor = session.tutor
            feedback.save()
                
            create_notification(
            recipient= session.tutor,
            user=request.user,
            type='session_feedback',
            link= "{% url 'base_session_list' %}")


            avg_rating = FeedBack.get_tutor_average(session.tutor)
            TutorProfile.objects.filter(user=session.tutor).update(rating=avg_rating)
            return  render(request,'status/page.html',{
            'success': True,
            'message': f'thank you for your feedback!'})
    else:
        form = FeedbackForm()

    return render(request, 'feedback/form.html', {'form': form, 'session': session})


@login_required
def feedback_list(request):
    """Tutor view to see all received feedback"""
    if request.user.role != 'tutor':
        return HttpResponseForbidden("Only tutors can view this page.")

    feedbacks = FeedBack.objects.filter(tutor=request.user)
    avg_rating = FeedBack.get_tutor_average(request.user)

    return render(request, 'feedback/list.html', {
        'feedbacks': feedbacks,
        'avg_rating': avg_rating
    })


@login_required
def feedback_detail(request, feedback_id):
    feedback = get_object_or_404(FeedBack, id=feedback_id)
    if feedback.tutor != request.user and feedback.student != request.user:
        return HttpResponseForbidden("You are not allowed to view this feedback.")
    return render(request, 'feedback/feedback_detail.html', {'feedback': feedback})
