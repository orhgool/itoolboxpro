import os, re, urllib.parse, urllib.request, httplib2

from pytube import YouTube
from bs4 import BeautifulSoup, SoupStrainer
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

from .models import DlFromWebs

def index(request):
	ultimos_boxes = DlFromWebs.objects.filter(fecha__lte=timezone.now()).order_by('-fecha')[:12]
	top_3_hosts = DlFromWebs.objects.filter(fecha__lte=timezone.now()).order_by('-fecha')[:3]
	urls_del_mes = DlFromWebs.objects.filter(fecha__lte=timezone.now()).order_by('-fecha')[:5]
	index_context = {'ultimos_boxes': ultimos_boxes}
	return render(request, 'halcon/index.html', index_context)


def resultados(request):
	imgs = []
	plantilla = ""
	error_message = ""
	if request.method == 'POST' and 'url' in request.POST:
		url = request.POST['url']
		response = urllib.request.urlopen(url)
		html = response.read()
		soup = BeautifulSoup(html, "lxml")
		titulo = ""
		descripcion =""
		imagen = ""
		video = "vacio"
		mostrar_video = "none"
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
					mostrar_video = "block"


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
					mostrar_video = "block"


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

			#video = soup.select_one("a[href*=kiwilimon]")

			#video = soup.select_one("source[src*=pinimg.com]")
			
			 
			"""for img in soup.findAll('source'):
				imgs.append(img.get('src'))"""
			
			#error_message = imgs
				
			#video = soup.find_all('src', type='video/mp4')
			


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
					mostrar_video = "block"

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
					mostrar_video = "block"

			
		datos = {'url': url, 'host': host, 'titulo': titulo, 'descripcion': descripcion, 'imagen': imagen, 'video': video, 'mostrar_video': mostrar_video, 'videoid': videoid, 'error_message': error_message}
		insertar_registro = DlFromWebs(url_text=url, media_src=imagen, media_titulo=titulo, media_descripcion=descripcion, media_host=host)
		insertar_registro.save()

		return render(request, plantilla, datos)
	else:
		return render(request, plantilla, datos)

def detalle(request, url_id):
	box = get_object_or_404(DlFromWebs, id=url_id)
	return render(request, 'halcon/detalle.html', {'box': box})