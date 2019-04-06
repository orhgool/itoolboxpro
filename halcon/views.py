import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
from pytube import YouTube
from django.utils import timezone

from .models import DlFromWebs


def index(request):
	ultimos_boxes = DlFromWebs.objects.filter(fecha__lte=timezone.now()).order_by('-fecha')[:12]
	index_context = {'ultimos_boxes': ultimos_boxes}
	return render(request, 'halcon/index.html', index_context)


def resultados(request):
	plantilla = ""
	if request.method == 'POST' and 'url' in request.POST:
		url = request.POST['url']
		response = urllib.request.urlopen(url)
		html = response.read()
		soup = BeautifulSoup(html)
		titulo = ""
		descripcion =""
		imagen = ""
		video = "vacio"
		enlaces = ""
		host = ""
		subtitulos = ""
		formatos = ""
		videoid = ""

		if 'youtube' in url or 'youtu.be' in url:
			host="YouTube"
			plantilla = 'halcon/youtube.html'
			yt = YouTube(url)
			videoid = yt.video_id

			for tag in soup.find_all("meta"):
				if tag.get("property", None) == "og:title":
					titulo = tag.get("content", None)

				if tag.get("property", None) == "og:description":
					descripcion = tag.get("content", None) 

				if tag.get("property", None) == "og:image":
					imagen = tag.get("content", None)

				if tag.get("property", None) == "og:video:url":
					video = tag.get("content", None)
			

		elif 'twitter' in url:
			host="Twitter"
			plantilla = 'halcon/cuerpo.html'
			for tag in soup.find_all("meta"):
				if tag.get("property", None) == "og:title":
					titulo = tag.get("content", None)

				if tag.get("property", None) == "og:description":
					descripcion = tag.get("content", None) 

				if tag.get("property", None) == "og:image":
					imagen = tag.get("content", None)

				if tag.get("property", None) == "og:video:url":
					video = tag.get("content", None)

		elif 'facebook' in url:
			host="Facebook"
			plantilla = 'halcon/cuerpo.html'
			for tag in soup.find_all("meta"):
				if tag.get("property", None) == "og:title":
					titulo = tag.get("content", None)

				if tag.get("property", None) == "og:description":
					descripcion = tag.get("content", None) 

				if tag.get("property", None) == "og:image":
					imagen = tag.get("content", None)

				if tag.get("property", None) == "og:video":
					video = tag.get("content", None)


		elif 'instagram' in url:
			host="Instagram"
			plantilla = 'halcon/cuerpo.html'
			for tag in soup.find_all("meta"):
				if tag.get("property", None) == "og:title":
					titulo = tag.get("content", None)

				if tag.get("property", None) == "og:description":
					descripcion = tag.get("content", None) 

				if tag.get("property", None) == "og:image":
					imagen = tag.get("content", None)

				if tag.get("property", None) == "og:video":
					video = tag.get("content", None)


		elif 'pinterest' in url:
			host="Pinterest"
			plantilla = 'halcon/cuerpo.html'
			for tag in soup.find_all("meta"):
				if tag.get("property", None) == "og:title":
					titulo = tag.get("content", None)

				if tag.get("property", None) == "og:description":
					descripcion = tag.get("content", None) 

				if tag.get("property", None) == "og:image":
					imagen = tag.get("content", None)

				video = soup.find("source").get("src")

		elif 'vimeo' in url:
			host="Vimeo"
			plantilla = 'halcon/cuerpo.html'
			for tag in soup.find_all("meta"):
				if tag.get("property", None) == "og:title":
					titulo = tag.get("content", None)

				if tag.get("property", None) == "og:description":
					descripcion = tag.get("content", None) 

				if tag.get("property", None) == "og:image":
					imagen = tag.get("content", None)

				if tag.get("property", None) == "og:video":
					video = tag.get("content", None)

		else:
			host="Web"
			plantilla = 'halcon/cuerpo.html'
			for tag in soup.find_all("meta"):
				if tag.get("property", None) == "og:title":
					titulo = tag.get("content", None)

				if tag.get("property", None) == "og:description":
					descripcion = tag.get("content", None) 

				if tag.get("property", None) == "og:image":
					imagen = tag.get("content", None)

				if tag.get("property", None) == "og:video":
					video = tag.get("content", None)

			
		datos = {'url': url, 'host': host, 'titulo': titulo, 'descripcion': descripcion, 'imagen': imagen, 'video': video, 'videoid': videoid}
		insertar_registro = DlFromWebs(url_text=url, media_src=imagen, media_titulo=titulo, media_descripcion=descripcion, media_host=host)
		insertar_registro.save()

		return render(request, plantilla, datos)
	else:
		return render(request, plantilla, datos)