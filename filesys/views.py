# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from .models import UploadFileModel
from django.core.files.storage import FileSystemStorage
import datetime
import os

def upload(request):
	fs = FileSystemStorage()
	file_list = []
	for _file in fs.listdir('')[1]:
		file_list.append({'name': os.path.basename(_file), 'url': fs.url(_file)})

	if request.method == 'POST' and request.FILES.get('file', False) and request.POST.get('mode', False):
		start = datetime.datetime.now()
		file = request.FILES['file']
		print request.POST['mode']
		filename = fs.save(file._name, file)
		uploaded_file_url = fs.url(filename)
		end = datetime.datetime.now()
		total_time = end - start
		total_time = total_time.total_seconds()
		file_list.append({'name': os.path.basename(filename), 'url': fs.url(filename)})
		return render(request, 'filesys/file_list.html', {'files': file_list, 'message': 'upload success', 'time': total_time})

	return render(request, 'filesys/file_list.html', {'files': file_list})

# Create your views here.
