from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# templates views
from django.views.generic import TemplateView
from hora.views import EnlaceListView, EnlaceDetailView

# router para el serializador
from rest_framework import routers
from hora.views import EnlaceViewSet, UserViewSet, CategoriaViewSet
router = routers.DefaultRouter()
router.register(r'links', EnlaceViewSet)
router.register(r'users', UserViewSet)
router.register(r'categorias', CategoriaViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # url para al api rest
    url(r'^api/', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls'), namespace='rest_framework'),
    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'hora.views.home', name='home'),
    url(r'^hora/', 'hora.views.hora_actual', name='hora'),
    url(r'^horados/', 'hora.views.hora_actual_dos', name='hora_actual_dos'),
    url(r'^plus/(\d+)$', 'hora.views.plus', name='plus'),
    url(r'^minus/(\d+)$', 'hora.views.minus', name='minus'),
    url(r'^categoria/(\d+)$', 'hora.views.categoria', name='categoria'),
    url(r'^add/$', 'hora.views.add', name='add'),
    #para las template_view
    url(r'^about/$', TemplateView.as_view(template_name='index.html'), name='about'),
    #para class base view
    url(r'^enlaces/$', EnlaceListView.as_view(), name='enlaces'),
    url(r'^enlaces/(?P<pk>[\d]+)$', EnlaceDetailView.as_view(), name='enlaces_details'),
)
