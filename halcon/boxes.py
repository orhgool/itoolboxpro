from .models import DlFromWebs

class Box():
	def __int__(self, box_url, box_titulo, box_descripcion, box_imagen, box_host):
		self.url = DlFromWebs.objects.url_text
		self.titulo = box_titulo
		self.descripcion = box_descripcion
		self.imagen = box_imagen
		self.host = box_host
