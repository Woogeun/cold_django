# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from .models import UploadFileModel
from django.core.files.storage import FileSystemStorage
import time
import os

def upload(request):
	fs = FileSystemStorage()
	file_list = []
	for _file in fs.listdir('')[1]:
		file_list.append({'name': os.path.basename(_file), 'url': fs.url(_file)})

	if request.method == 'POST' and request.FILES.get('file', False) and request.POST.get('mode', False):
		latency = time.time()
		file = request.FILES['file']
		print request.POST['mode']
		filename = fs.save(file._name, file)
		uploaded_file_url = fs.url(filename)
		file_list.append({'name': os.path.basename(filename), 'url': fs.url(filename)})
		print time.time()-latency
		return render(request, 'filesys/file_list.html', {'files': file_list})

	return render(request, 'filesys/file_list.html', {'files': file_list, 'fail': 'failed upload file'})

# Create your views here.
