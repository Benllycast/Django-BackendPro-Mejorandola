#para agregar variables al contexto de las plantillas
# todo context processors retorna un diccionario con claves y valores
from random import choice
from django.core.cache import cache

frases = ['frase uno', 'frase dos', 'frase tres']

# todo context processors retorna un diccionario con claves y valores
def ejemplo(request):
	# ejemplo basico de cache low level
	frase = cache.get('frase_cool')
	if frase is None:
		frase = choice(frases)
		cache.set('frase_cool', frase)
	# return {'frase':choice(frases)}
	return {'frase':frase}

from django.core.urlresolvers import reverse

def menu(request):
	menu = {'menu':[
		{'name':'home', 'url':reverse('home')},
		{'name':'add', 'url':reverse('add')},
		{'name':'Acerca de', 'url':reverse('about')},
	]}
	for item in menu['menu']:
		if request.path == item['url']:
			item['active'] = True
	return menu