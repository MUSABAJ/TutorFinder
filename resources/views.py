from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, HttpResponseForbidden, HttpResponse
from .forms import ResourceForm
from .models import Resource
from users.models import TutorProfile
import os

@login_required
def list_resources(request):
    query = request.GET.get('q')
    resources = Resource.objects.all()
    if query:
        resources = resources.filter(title__icontains=query)
    return render(request, 'resources/resource_list.html', {'resources': resources})


@login_required
def upload_resource(request):
    if request.user.role != 'tutor':
        return HttpResponseForbidden("Only tutors can upload resources.")
    
    tutor_profile = TutorProfile.objects.filter(user=request.user).first()
    subjects = []
    if tutor_profile and tutor_profile.subjects:
        subjects = [s.strip() for s in tutor_profile.subjects.split(',')]

    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.tutor = request.user
            resource.save()
            return redirect('resource_list')
    else:
        form = ResourceForm()

    context = {'form': form, 'subjects': subjects}
    return render(request, 'resources/upload.html', context)


@login_required
def delete_resource(request, id):
    resource = get_object_or_404(Resource, id=id)
    if resource.tutor != request.user:
        return HttpResponseForbidden("You can only delete your own resources.")
    
    if request.method == 'POST':
        if resource.file:
            resource.file.delete()
        resource.delete()
        return redirect('resource_list')

    return render(request, 'resources/confirm_delete.html', {'resource': resource})


@login_required
def download_resource(request, id):
    resource = get_object_or_404(Resource, id=id)
    if not resource.file:
        return HttpResponse('No downloadable file for this resource.')

    file_path = resource.file.path
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
    return HttpResponse('File not found.', status=404)
