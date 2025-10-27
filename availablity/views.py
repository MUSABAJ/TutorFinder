from tkinter import Pack
from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse , HttpResponse
from .models import Availablity, TutorPackage
from users.models import TutorProfile
from .forms  import PackageForm
from users.models import User
from core.views import get_tutor_dashboard_context
import json

def create_package(request):
    tutor_profile = TutorProfile.objects.get(user=request.user)
    subjects = tutor_profile.subjects.split(',') # assumig for now subjects are comma separated 
    
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            pkg = form.save(commit=False)
            pkg.tutor=request.user
            pkg.save()
            return HttpResponse('sucessful')
    else:
        form=PackageForm()
        context = {'form':form}
        return render(request, 'package/create.html',context)

def package_list(request, tutor_id): 
        tutor = get_object_or_404(User, id=tutor_id, role= 'tutor')
        packages = TutorPackage.objects.filter(tutor=tutor)         
        tutor_profile = TutorProfile.objects.get(user=tutor)

        subjects = tutor_profile.subjects.split(',') # assumig for now subjects are comma separated

        context = {
            'packages':packages, 
            'tutor':tutor,
            'subjects':[sub.strip() for sub in subjects]}
        
        return render(request, 'package/list.html/',context)



def delete_pkg(request, pkg_id):
    if request:
        pkg = get_object_or_404(TutorPackage, id=pkg_id)
        pkg.delete()
        return JsonResponse('succes' ,safe=False)

    return JsonResponse('error' ,safe=False)
        
def togle_pkg(request, pkg_id):
    if request:
        pkg = get_object_or_404(TutorPackage, id=pkg_id)
        pkg.is_active = True if not pkg.is_active else False
        pkg.save()
        return JsonResponse('succes' ,safe=False)
    return JsonResponse('error' ,safe=False)

def set_availablity(request):
    try:
        avail_obj = Availablity.objects.filter(tutor=request.user).first()
        availablity = avail_obj.availablity if avail_obj else []
    except Exception:
        availablity = []

    packages = TutorPackage.objects.filter(tutor=request.user)

    if request.method == 'POST':
        json_data = request.POST.get('availablity_json')
        try:
            data = json.loads(json_data)
            Availablity.objects.update_or_create(
                tutor=request.user,
                defaults={'availablity': data}
            )
            return redirect('set_availablity')
        except Exception as e:
            return redirect('set_availablity')
        
    ctx= get_tutor_dashboard_context(request.user)
    context = {
        'availablity__json': json.dumps(availablity),
        'packages': packages
    }
    context.update(ctx)
    return render(request, 'tutor/pages/set_availablity.html', context)
