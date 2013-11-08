from django.contrib import admin
from models import Categoria, Agregador, Enlace
from actions import export_as_csv

class EnlaceAdmin(admin.ModelAdmin):
	list_display = ('titulo', 'enlace', 'categoria', 'usuario','imagen_voto', 'es_popular')
	list_filter = ('categoria','usuario')
	search_fields = ('categoria__titulo','usuario__email',)
	list_editable = ('enlace', 'categoria',) # solo los campos que esten en list_display (no funciones)
	list_display_links = ('es_popular',) # cambiar el enlace de edicion a un nuevo campo
	actions = [export_as_csv]
	raw_id_fields = ('categoria','usuario')

	def imagen_voto(self, obj):
		url = obj.mis_votos_en_imagen_rosada()
		tag = '<img src="%s" alt="votos">' % url
		return tag
	
	imagen_voto.allow_tags = True
	imagen_voto.admin_order_field = 'votos'

#para ilines 
class EnlaceInline(admin.StackedInline):
	model = Enlace
	extra = 1
	raw_id_fields = ('usuario',)

class CategoriaAdmin(admin.ModelAdmin):
	actions = [export_as_csv]
	inlines = [EnlaceInline] #inlines

class AgregadorAdmin(admin.ModelAdmin):
	filter_horizontal = ('enlaces',) #filter_vertical tambien existe

admin.site.register(Agregador, AgregadorAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Enlace,EnlaceAdmin)