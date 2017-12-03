# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from .forms import UploadFileForm
from .models import UploadFileModel
from django.core.files.storage import FileSystemStorage
import datetime
import os
import subprocess
import time
import glob
import json
import requests
import socket
import getpass


url_upload = 'http://143.248.225.40:5000/upload'
url_upload_real = 'http://143.248.225.40:5000/upload_real'
url_download = 'http://143.248.225.40:5000/download'

abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

ps = []

for i in abc:
	for j in abc:
		elem = i + j
		ps.append(elem)

address = 'android@143.248.225.40:/home/android/disk_cold'
password =  'changeme'

def upload(request):
	fs = FileSystemStorage()
	file_list = []
	for _file in fs.listdir('')[1]:
		if (_file != '.DS_Store'):
			file_list.append({'name': os.path.basename(_file), 'url': fs.url(_file)})

	if request.method == 'POST' and request.FILES.get('file', False) and request.POST.get('mode', False):
		# store start time
		start = datetime.datetime.now()

		# file name
		file = request.FILES['file']
		size = file.size
		split_size = '-b ' + str(int(0.6 * size))

		filename = fs.save(file._name, file)


		uploaded_file_url = fs.location + '/' + filename

		def command_create (postfix):
			return 'sshpass -p' + password + ' scp -o StrictHostKeyChecking=no ' + uploaded_file_url + postfix + ' ' + address

		def full_command(count):
			cmd = ''
			for i in ps[:count]:
				if i != ps[0]:
					cmd = command_create(i) + ' & ' + cmd
				else:
					cmd = cmd + command_create(i)
			print cmd
			return cmd

		start_ft = time.time()
		subprocess.call (['split', split_size, uploaded_file_url, uploaded_file_url])
		subprocess.call ([full_command(2)], shell=True)
		end = datetime.datetime.now()
		total_time = end - start
		total_time = total_time.total_seconds()
		messages.info(request, 'success!')

		# file block list
		p_file_block_tmp = glob.glob(uploaded_file_url + '*')
		p_file_block_tmp.remove(uploaded_file_url)
		p_file_block_list = [str(os.path.basename(i)) for i in p_file_block_tmp]
		block_to_remove = p_file_block_list[:]
		
		p_file_block_list = json.dumps(p_file_block_list)

		# print p_file_block_list

		# block size list, each corresponding to file block list
		p_block_size_list = [os.stat(i).st_size  for i in p_file_block_tmp]

		# size of original file
		p_file_size = os.stat(uploaded_file_url).st_size
		data = '{"file_name": %s, "file_block_name": %s, "file_size": %s, "block_size": %s}' % (json.dumps(filename), p_file_block_list, p_file_size, p_block_size_list)
		data = json.dumps(str(data))

		# print data
		headers = {"Content-type": "application/json", "Accept": "text/plain"}
		for block in block_to_remove:
			fs.delete(block)
		file_list.append({'name': os.path.basename(filename), 'url': fs.url(filename)})
		res = requests.post(url_upload, data, headers = headers)
		return render(request, 'filesys/file_list.html', {'files': file_list, 'message': 'upload success', 'time': total_time})
			
	if request.method == 'POST' and request.POST.get('filename', False) and request.POST.get('url', False):
		start_down = datetime.datetime.now()
		file_name = request.POST['filename']
		cli_addr = json.dumps(socket.gethostbyname(socket.gethostname()))
		data = '{"file_name" : %s, "client_address": %s, "client_id": %s, "client_pw": %s}'  %(json.dumps(file_name), cli_addr, json.dumps(getpass.getuser()), json.dumps("dlfdltka4"))

		headers = {"Content-type": "application/json", "Accept": "text/plain"}
		res = requests.post(url_download, json.dumps(data), headers = headers)
		end_down = datetime.datetime.now()
		total_down = end_down - start_down
		total_down = total_down.total_seconds()
		res_json = res.json()
		original_file_name = res_json["file_name"]
		cat_command = 'cat ' + '~/' + original_file_name + '*' + ' > ' + '~/' + original_file_name
		subprocess.call ([cat_command], shell=True)
		return render(request, 'filesys/file_list.html', {'files': file_list, 'message': 'download success', 'time': total_down})

	return render(request, 'filesys/file_list.html', {'files': file_list})

# Create your views here.
