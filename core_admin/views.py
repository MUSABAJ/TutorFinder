from django.contrib.admin.views.decorators import staff_member_required
from tutor_sessions.models import BookedSession
from django.utils.timezone import now
from django.shortcuts import render
from datetime import timedelta
from users.models import User
#send  Broadcast view //all user, only student, only tutor
# compose messagess
# send it


@staff_member_required
def admin_stats_view(request): 
    today = now().date()
    this_month = today.replace(day=1)

    # Count stats
    total_students = User.objects.filter(role='student').count()
    total_tutors = User.objects.filter(role='tutor').count()
    verified_tutors = User.objects.filter(role='tutor', tutor__is_verified=True).count()
    sessions_this_month = BookedSession.objects.filter(schedule_date__gte=this_month).count()
 
    # Prepare chart data
    chart_data = {
        'labels': ['Students', 'Tutors', 'Verified Tutors'],
        'data': [total_students, total_tutors, verified_tutors]
    }

    context = {
        'chart_data': chart_data,
        'sessions_this_month': sessions_this_month,
     }

    return render(request, 'admin/stats.html', context)