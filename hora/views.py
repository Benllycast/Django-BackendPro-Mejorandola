# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, get_object_or_404, render #si usas context_processors
from datetime import datetime
from models import *
from forms import EnlaceForm
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
#decorador para cache per view 
from django.views.decorators.cache import cache_page
from .tasks import calculo
#agregando decorador de vista
# @cache_page(6000)
def home(request):
	categorias = Categoria.objects.all()
	enlaces = Enlace.objects.order_by('-votos').all()
	template = 'index.html'
	# para celery
	calculo.delay() 
	return render(request, template,locals()) # pasar el request a reden para ver las variables echas en context processors

def hora_actual(request):
	ahora = datetime.now()
	t = get_template("hora.html")
	c = Context({'hora':ahora, 'usuario':'benlllycast'})
	html = t.render(c)
	return HttpResponse(html)

def hora_actual_dos(request):
	ahora = datetime.now()
	return render_to_response('hora.html',{'hora':ahora})

@login_required
def minus(request, id_enlace):
	enlace = Enlace.objects.get(pk=id_enlace)
	enlace.votos -= 1
	enlace.save()
	return HttpResponseRedirect("/")

@login_required
def plus(request, id_enlace):
	enlace = Enlace.objects.get(pk=id_enlace)
	enlace.votos += 1
	enlace.save()
	return HttpResponseRedirect("/")

def categoria(request, id_categoria):
	categorias = Categoria.objects.all()
	# cat = Categoria.objects.get(pk=id_categoria)
	cat = get_object_or_404(Categoria, pk=id_categoria)
	enlaces = Enlace.objects.filter(categoria = cat)
	template = "index.html"
	return render(request, template, locals())

@login_required
def add(request):
	categorias = Categoria.objects.all()
	if request.method == 'POST':
		form = EnlaceForm(request.POST)
		if form.is_valid():
			enlace = form.save(commit=False)
			enlace.usuario = request.user
			enlace.save()
			return HttpResponseRedirect("/")
	else:
		form = EnlaceForm()

	template = "form.html"
	return render_to_response(template,context_instance = RequestContext(request, locals()))

#class view
from django.views.generic import ListView, DetailView

class EnlaceListView(ListView):
	model = Enlace
	context_object_name = 'enlaces'

	def get_template_names(self):
		return 'index.html'

class EnlaceDetailView(DetailView):
	model = Enlace
	
	def get_template_names(self):
		return 'index.html'

# view set para las vistas del serializador
from .serializers import EnlaceSerializer, UserSerializer, CategoriaSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User

class EnlaceViewSet(viewsets.ModelViewSet):
	queryset = Enlace.objects.all()
	serializer_class = EnlaceSerializer

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
	queryset = Categoria.objects.all()
	serializer_class = CategoriaSerializer

# para optimizacion por sitio
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.sessions.models import Session 
# esto es para redis
@receiver(post_save)
def clear_cache(sender, **keyargs):
	if sender != Session:
		cache.clear()

# para memcache
# @receiver(post_save)
# def clear_cache(sender, **keyargs):
# 	if sender is Session:
# 		cache._cache.flush_all()