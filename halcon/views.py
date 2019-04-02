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
		host = ""
		subtitulos = ""

		if 'instagram' in url:
			host="Instagram"
		if 'youtube' or 'youtu.be' in url:
			host="YouTube"
		if 'twitter' in url:
			host="Twitter"
		if 'facebook' in url:
			host="Facebook"
		if 'pinterest' in url:
			host="Pinterest"
		if 'vimeo' in url:
			host="Vimeo"

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
		return render(request, 'halcon/cuerpo.html', datos)