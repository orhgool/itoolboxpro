from django.db import models
from django.utils import timezone

class DlFromWebs(models.Model):
	url_text = models.URLField(max_length=200)
	fecha = models.DateTimeField('fecha', default=timezone.now)
	media_src = models.TextField(max_length=300, default='')
	media_titulo = models.TextField(max_length=300, default='')
	media_descripcion = models.TextField(max_length=300, default='')
	media_host = models.TextField(max_length=20, default='')

	def __str__(self):
		return self.media_host

	def get_data():
		return DlFromWebs.objects

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=30) <= self.fecha <= now
