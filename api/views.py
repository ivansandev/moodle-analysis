from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.views.decorators.http import require_POST

import json
import os
from .helpers.analysis import PlatformDataAnalyser
from . import models

from frontend.forms import UploadForm, UploadModelForm


def test(request):
    return HttpResponse(json.dumps({"message":"API is OK", "status":200, "authorization": False}))

def file_upload():
    analyser = PlatformDataAnalyser('./uploads/course_{id}')

def calculate_mean(request):
    return HttpResponse(f'This is just a test! {request.GET.get("upr", default=None)}')


def central_tendency(request):
    analyser = PlatformDataAnalyser('/home/bobiyu/Documents/UNI/ПТС/test_folder/files')

    if request.method == 'GET':
        selector = request.GET.get("upr", default="")
    elif request.method == 'POST':
        selector = request.POST.get("upr", default="")

    data = analyser.calculate_central_tendency(selector)
    return HttpResponse(data);


@require_POST
def get_correlation(request):
    if request.POST['upload_id']:
        data = models.CorrelationAnalysis.objects.get(upload_id=request.POST['upload_id'])

        return JsonResponse(data.correlation_data, safe=False)

    return JsonResponse({'status': 404, 'msg': 'Not found!'})


@require_POST
def get_corr_freq_dist(request):
    if request.POST['upload_id']:
        data = models.CorrelationAnalysis.objects.get(upload_id=request.POST['upload_id'])

        return JsonResponse(data.freq_distrib, safe=False)

    return JsonResponse({'status': 404, 'msg': 'Not found!'})


@require_POST
def delete_upload(request):
    if request.POST['upload_id']:
        upload = models.Upload.objects.get(pk=request.POST['upload_id'])

        upload.delete()
        return JsonResponse({'status': 200, 'msg': 'Upload deleted.'})
    
    return JsonResponse({'status': 404, 'msg': 'Not found!'})



def all_analysis(request, user_id):
    # filepath = '/Users/ivansandev/Desktop/stalking_lectures/ExampleInputData'
    filepath = os.path.join(settings.MEDIA_ROOT, str(user_id))

    analyser = PlatformDataAnalyser(filepath)

    data = analyser.calculate_all()
    return HttpResponse(data);


def upload_test_form(request):
    context = {}

    if request.method == 'POST':
        form = UploadModelForm(request.POST, request.FILES, user=request.user)

        # if form.is_valid():
        # from datetime import datetime

        # now = datetime.now().strftime("%Y%m%d%H%M%S")
        # upload = request.FILES.getlist('analysis_files')

        # upload_path = f'user_{request.user.id}/{now}'
        # upload_path = os.path.join(settings.MEDIA_ROOT, upload_path)
        # fs = FileSystemStorage(location=upload_path)

        # upl = []
        # for x in upload:
        #     upl.append(fs.url(fs.save(x.name, x)))

        # context['urls'] = upl

        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = UploadModelForm()

    context['form'] = form

    return render(request, 'upload.html', context)
