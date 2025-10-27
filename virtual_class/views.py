from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from tutor_sessions.models import BookedSession, VirtualClass
import uuid


@login_required
def create_virtual_class(request, session_id):
    """Tutor creates or accesses the virtual classroom for a given session."""
    session = get_object_or_404(BookedSession, id=session_id)

    # Ensure only the tutor can create the room...
    if request.user != session.parent.tutor:
        messages.error(request, "You are not authorized to create this virtual class.")
        return redirect("session_list")

    # Create or get the room
    room, created = VirtualClass.objects.get_or_create(
        session=session,
        defaults={"room_name": f"VCRoom-{uuid.uuid4().hex[:10]}"}
    )

    # If created, attach the room link to session
    if created or not session.video_link:
        session.video_link = room.room_name
        session.save()

    # Optionally notify student (email, Telegram, etc.)
    # Example:
    # notify_user(session.parent.student, f"Virtual class for your session {session.id} is ready!")

    messages.success(request, f"Virtual classroom ready! Room: {room.room_name}")
    return redirect('virtual_class', session_id=session.id)


@login_required
def join_virtual_class(request, session_id):
    """Allow tutor or student to join the virtual classroom."""
    session = get_object_or_404(BookedSession, id=session_id)


    if request.user not in [session.parent.tutor, session.parent.student]:
        messages.error(request, "You are not enrolled in this class.")
        return redirect("session_list")

    if not session.video_link:
        messages.error(request, "This class does not have an active virtual room yet.")
        return redirect("session_list")


    jitsi_config = {
        'domain': getattr(settings, 'JITSI_DOMAIN', 'meet.jit.si'),
        'room_name': session.video_link,
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
