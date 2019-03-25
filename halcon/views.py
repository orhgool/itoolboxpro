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
		response = urllib.request.urlopen(url)
		html = response.read()
		soup = BeautifulSoup(html)
		titulo = ""
		descripcion =""
		imagen = ""
		video = ""
		enlaces = ""
		subtitulos = ""

		if 'instagram' in url:
			host="Instagram"
		if 'youtube' or 'youtu.be' in url:
			host="YouTube"
		if 'twitter' in url:
			host="Twitter"
		if 'facebook' in url:
			host="Facebook"

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

		datos = {'url': url, 'host': host, 'titulo': titulo, 'descripcion': descripcion, 'imagen': imagen, 'video': video}

		insertar_registro = DlFromWebs(url_text=url, media_src=imagen, media_titulo=titulo, media_descripcion=descripcion, media_host=host)
		insertar_registro.save()

		return render(request, 'halcon/cuerpo.html', datos)
	else:
		return render(request, 'halcon/index.html')   