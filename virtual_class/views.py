from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from tutor_sessions.models import BaseSession
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from notifications.utils import create_notification
from tutor_sessions.models import BookedSession, VirtualClass
import uuid




@login_required
def check_in_out(request, session_id):
    current_session = get_object_or_404(BookedSession, id=session_id) 
    session = BaseSession.objects.get(sessions=current_session)
    user = request.user
    if user not in [session.student,session.tutor]:
        return HttpResponseForbidden("Unauthorized action")

    button = 'Rate Your Session'
    with transaction.atomic():

        if session.status == 'confirmed' or session.status == 'ongoing':
            session.start_session()
            current_session.status='active'
            button = 'End Session'
            
            create_notification(
            recipient=session.tutor,
            user=request.user,
            type='session_started',
            link= "{% url 'base_session_list' %}")
            
            create_notification(
            recipient=session.student,
            user=request.user,
            type='session_started',
            link= "{% url 'base_session_list' %}")

        elif session.status == 'active':
            session.end_session()
            create_notification(
            recipient=session.tutor,
            user=request.user,
            type='session_ended',
            link= "{% url 'base_session_list' %}")
            
            create_notification(
            recipient=session.student,
            user=request.user,
            type='session_ended',
            link= "{% url 'base_session_list' %}")
            current_session.status='completed'
            button = 'Start Session'

    percentage = (session.remaining_sessions/ session.total_session)*100

    context = {'session': session, 'button':button, 'percentage':percentage}
    return render(request,"virtualclass/in_person_checkin.html", context)

@login_required
def create_virtual_class(request, session_id):
    """Tutor creates or accesses the virtual classroom for a given session."""
    session = get_object_or_404(BookedSession, id=session_id)

    if request.user != session.base_session.tutor:
        messages.error(request, "You are not authorized to create this virtual class.")
        return redirect("session_list")

    room, created = VirtualClass.objects.get_or_create(
        session=session,
        defaults={"room_name": f"VCRoom-{uuid.uuid4().hex[:10]}"}
    )

    if created or not session.room_name:
        session.room_name = room.room_name
        session.save()
        create_notification(
                recipient= session.base_session.student,
                user=request.user,
                type='five_min_session_reminder',
                link= "{% url 'session_list' %}"
                )
    return redirect('join_virtual_class', session_id=session.id)


@login_required
def join_virtual_class(request, session_id):
    """Allow tutor or student to join the virtual classroom."""
    session = get_object_or_404(BookedSession, id=session_id)


    if request.user not in [session.base_session.tutor, session.base_session.student]:
        messages.error(request, "You are not enrolled in this class.")
        return redirect("session_list")

    if not session.room_name:
        messages.error(request, "This class does not have an active virtual room yet.")
        return redirect("session_list")


    jitsi_config = {
        'domain': getattr(settings, 'JITSI_DOMAIN', 'meet.jit.si'),
        'room_name': session.room_name,
        'userInfo': {'displayName': request.user.username},
        'configOverwrite': {
            'startWithAudioMuted': True,
            'startWithVideoMuted': False,
            'prejoinPageEnabled': getattr(settings, 'JITSI_PREJOIN_ENABLED', False),
        }
    }

    return render(
        request,
        "virtualclass/classRoom.html",
        {
            "session": session,
            "jitsi_config": jitsi_config,
            "whiteboard": getattr(settings, 'JITSI_WHITEBOARD_ENABLED', False),
            "username": request.user.username,
        },
    )
