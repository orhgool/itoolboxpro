import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
from pytube import YouTube
from django.utils import timezone

from .models import DlFromWebs
#from html.parser import HTMLParser

def index(request):
	if request.method == 'POST' and 'url' in request.POST:
		url = request.POST['url']
		if 'instagram' in url:
			host="Instagram"
		if 'youtube' in url:
			host="YouTube"
		if 'youtu.be' in url:
			host="YouTube"
		if 'twitter' in url:
			host="Twitter"

		response = urllib.request.urlopen(url)
		html = response.read()
		soup = BeautifulSoup(html)
		titulo = ""
		descripcion =""
		imagen = ""
		video = ""
		enlaces = ""
		if (host == "YouTube"):
			#YouTube('url').streams.first().download()
			yt = YouTube(url)
			#yt.streams.order_by('resolution')
			enlaces = yt.streams.filter(progressive=False, file_extension='mp4').all()
			# yt.streams.get_by_itag(140).download()
			# yt.filter(progressive=True, file_extension='mp4')
			# yt.order_by('resolution')
			# yt.desc()
			# yt.first()
			# yt.streams.first().download()

		#enlace = soup.find("meta",  property="og:image")
		for tag in soup.find_all("meta"):
			if tag.get("property", None) == "og:title":
				titulo = tag.get("content", None)

			if tag.get("property", None) == "og:description":
				descripcion = tag.get("content", None) 

			if tag.get("property", None) == "og:image":
				imagen = tag.get("content", None)

			if tag.get("property", None) == "og:video":
				video = tag.get("content", None)

		datos = {'url': url, 'host': host, 'titulo': titulo, 'descripcion': descripcion, 'imagen': imagen, 'video': video, 'enlaces': enlaces}

		insertar_registro = DlFromWebs(url_text=url, media_src=imagen, media_titulo=titulo, media_descripcion=descripcion, media_host=host)
		insertar_registro.save()

		return render(request, 'halcon/cuerpo.html', datos)
	else:
		return render(request, 'halcon/index.html')   