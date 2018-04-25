from django.shortcuts import render

from django.views.generic.base import TemplateView
# Create your views here.
from django.http import HttpResponse

from mysite.settings import LOGDIR
from mysite.settings import IMAGEDIR
import urllib.parse
import os

#from articles.models import Article


def logs():
    fichero = open(LOGDIR, 'rt')
    ficherobien = []
    for line in fichero:
        tokens = line.split(';')
        ficherobien.append(tokens[0])
    del ficherobien[0]
    return ficherobien

def imgs(token):
    token = token.replace(":", "_")

    #añadir a la direccion de IMAGEDIR
    directorio = os.path.join(IMAGEDIR,token)
    directorio = directorio.replace("\t","")
    token = token.replace("\t","")
    print(directorio)
    #Devolver esa carpeta #Esa carpeta que llegue a image.html y ahí la muestre
    imagenes = []
    archivos = [d for d in os.listdir(directorio) if not os.path.isdir(d)]
    print(archivos)

    for imagen in archivos:
        imagenes.append(os.path.join(token,imagen))
    return imagenes

def comprobarDirectorio(token):
    token = token.replace(":", "_")
    token = token.replace("\t", "")
    directorio = os.path.join(IMAGEDIR,token)
    directorio = directorio.replace("\t","")
    if os.path.isfile(directorio):
        return True
    else:
        return False

def information(token):
    fichero = open(LOGDIR, 'rt')
    info=""
    for line in fichero:
        line = line.replace("\t", "")
        line = line.replace("\n", "")
        tokens = line.split(';')
        token = token.replace("\t", "")
        token = token.replace("\n", "")


        if tokens[0] == token:
            print(tokens)

            info = tokens
            break

    return info

class HomePageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tokens'] = logs()
        context['existeDirectorio'] = comprobarDirectorio(kwargs["token"])
        return context



class ImagePageView(TemplateView):

    template_name = "image.html"

    def get_context_data(self, **kwargs):

       context = super().get_context_data(**kwargs)
       context['imagenes'] = imgs(kwargs["token"])
       context['info'] = information(kwargs["token"])
       return context