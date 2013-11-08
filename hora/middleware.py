from django.shortcuts import redirect
from random import choice

paises =['colombia', 'peru', 'panama', 'mexico']

def de_donde_vengo(request):
	return choice(paises)

class PaisMiddleware(object):
	def process_request(self, request):
		pais = de_donde_vengo(request)
		print pais
		if pais == 'mexico':
			#return redirect('http://mejorando.la')
			pass
		#return request

	def process_response(self, request, response):
		return response