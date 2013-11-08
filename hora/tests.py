"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import Categoria, Enlace
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# titulo, enlace, votos, categoria, usuario, timestamp, 

class SimpleTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(titulo='Categoria de Test')
        self.usuario = User.objects.create_user(username='usuario_test', password='pass')
        

    def test_es_popular(self):
        # si un enlace tiene menos de 11 votos no es popular        
        enlace = Enlace.objects.create(titulo='Test',enlace='http://127.0.0.1',votos=0, categoria=self.categoria, usuario=self.usuario)
        self.assertEqual(enlace.votos, 0)
        self.assertEqual(enlace.es_popular(), False)
        self.assertFalse(enlace.es_popular())
        # si un enlace tien mas de 10 votoso es popular
        enlace.votos = 20
        enlace.save()
        self.assertEqual(enlace.votos, 20)
        self.assertEqual(enlace.es_popular(), True)
        self.assertTrue(enlace.es_popular())

    def test_views(self):
        # testing de las urls
        res = self.client.get(reverse('home'))
        self.assertEqual(res.status_code, 200)
        res = self.client.get(reverse('about'))
        self.assertEqual(res.status_code, 200)
        res = self.client.get(reverse('enlaces'))
        self.assertEqual(res.status_code, 200)

        #testing con de get url con login
        self.assertTrue(self.client.login(username='usuario_test', password='pass'))
        res = self.client.get(reverse('add'))
        self.assertEqual(res.status_code, 200)

    def test_add(self):
        # test de un post a una url para ingresar datos
        self.assertTrue(self.client.login(username='usuario_test', password='pass'))
        self.assertEqual(Enlace.objects.count(), 0)
        data = {}
        data['titulo'] = 'test titulo'
        data['enlace'] = 'http://test.com/'
        #data['votos'] = ''
        data['categoria'] = self.categoria.id
        #data['usuario'] = ''
        #data['timestamp'] = ''
        res = self.client.post(reverse('add'), data)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Enlace.objects.count(), 1)

        enlace = Enlace.objects.all()[0]
        self.assertEqual(enlace.titulo, data['titulo'])
        self.assertEqual(enlace.enlace, data['enlace'])
        self.assertEqual(enlace.categoria, self.categoria)
