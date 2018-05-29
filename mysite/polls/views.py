import time

from django.shortcuts import render

from django.views.generic.base import TemplateView, View
# Create your views here.
from django.http import HttpResponse

from mysite.settings import LOGDIR
from mysite.settings import IMAGEDIR
import urllib.parse
import os
import json
import tarfile

#Funcion para obtener en forma de diccionario toda la información de logs
def obtenerDiccionario():
    #abrir fichero logs
    fichero = open(LOGDIR, 'rt')
    #Crear un diccionario de listas
    diccionario = {'TimeStamp': [], 'Latitud': [], 'Longitud': [], 'NUM': [], 'IDPER': [], 'Ruta': [], 'FECHA': [],
                   'HORA': [], 'BRUTO': [], 'TARA': [], 'N_TAG': []}
    #Rellenar las listas del diccionario (En cada lista la info correspondiente a la etiqueta)
    for line in fichero:

        tokens = line.replace('\n','').split('\t;')

        if len(tokens) == 11:
            diccionario['TimeStamp'].append(tokens[0])
            diccionario['Latitud'].append(tokens[1])
            diccionario['Longitud'].append(tokens[2])
            diccionario['NUM'].append(tokens[3])
            diccionario['IDPER'].append(tokens[4])
            diccionario['Ruta'].append(tokens[5])
            diccionario['FECHA'].append(tokens[6])
            diccionario['HORA'].append(tokens[7])
            diccionario['BRUTO'].append(tokens[8])
            diccionario['TARA'].append(tokens[9])
            diccionario['N_TAG'].append(tokens[10])

    #devuelve el diccionario con toda la info cargada
    return diccionario

#Funcion para obtener la información de un token concreto, de uno de los TimeStamp
def informationVersion2(token):
    #Coger el diccionario
    diccionario = obtenerDiccionario()
    lalista = {}
    #Guardar el TimeStamp seleccionado y buscarlo en el diccionario para obtener la info de esa
    pos = diccionario['TimeStamp'].index(token)

    for key in ['TimeStamp', 'Latitud', 'Longitud', 'NUM', 'IDPER', 'Ruta', 'FECHA', 'HORA','BRUTO', 'TARA', 'N_TAG']:
        lalista[key] = diccionario[key][pos]
    #Devuelve la info de ese token
    return lalista


#Devuelve los TimeStamp del diccionario
def logsVersion2():
    diccionario=obtenerDiccionario()
    #Del diccionario coge de la etiqueta TimeStamp toda la lista y la devuelve
    return diccionario.get('TimeStamp')

#Obtener las imagenes de un TimeStamp concreto para poder visualizarlas en la app
def imgs(token):
    #Ya que el directorio donde se encuentran las imagenes no tiene el nombre en el mismo formato, cambiarlo
    token = token.replace(":", "_")

    #añadir a la direccion de IMAGEDIR el TimeStamp, es decir el token
    directorio = os.path.join(IMAGEDIR,token)
    directorio = directorio.replace("\t","")
    token = token.replace("\t","")
    print(directorio)
    #Devolver esa carpeta
    # #Esa carpeta que llegue a image.html y ahí la muestre
    imagenes = []
    archivos = [d for d in os.listdir(directorio) if not os.path.isdir(d)]
    print(archivos)
    #Coger cada una de las imagenes que se encuentra en el directorio y devolverlas juntas
    for imagen in archivos:
        imagenes.append(os.path.join(token,imagen))
    return imagenes

#Funcion para comprobar si existe el directorio del TimeStamp
# (Si no existe, no se podrá acceder (el botón no deberá funcionar))
def comprobarDirectorio(token):
    token = token.replace(":", "_")
    token = token.replace("\t", "")
    #El directorio comprobará si hay directorio sobre esas imagenes
    directorio = os.path.join(IMAGEDIR,token)
    directorio = directorio.replace("\t","")
    print(directorio)
    #Comprobar si existe ese directorio y devolver True o False
    if os.path.isdir(directorio):
        print("EXISTE")
        return True
    else:
        print("NO EXISTE")
        return False


#Funcion para obtener un archivo comprimido con todos los timeStamp y su info y respectivas imagenes
#NO FUNCIONA (NO HACE EL ARCHIVO COMPRIMIDO)
def obtenerArchivoCompleto():
    t0 = time.localtime()
    #Obtener fecha y hora actual
    ahora = time.strftime("%a-%b-%y_%H:%M:%S", t0) + '.tar.gz'
    #Obtener todos los timeStamps
    tokens = logsVersion2()
    #Crear y abrir un archivo en el directorio,
    # El archivo tendrá que tener de nombre la hora y fecha del momento de la descarga
    elarchivo = os.path.join('/home/energy/truckDataApp/mysite/logs/', "Backup_" + ahora)
    with tarfile.open(elarchivo, 'w') as tar:
        #Por cada uno de los timeStamp
        for token in tokens:
            #Guardar la informacion perteneciente a ese timestamp
            info = informationVersion2(token)
            info = {'info': info}
            #Abrir una carpeta dentro del directorio anterior (general)
            #El nombre de la carpeta deberá ser el timeStamp actual
            directoriocarpeta = os.path.join(elarchivo,token)
            with tarfile.open(directoriocarpeta, 'w') as carpeta:
                #Añadir un txt a esa carpeta con la info
                with open('file.txt', 'w') as info_file:
                    info_file.write(json.dumps(info))
                carpeta.add('file.txt')
                #Si existe el directorio (Si tiene carpeta de imagenes)
                if comprobarDirectorio(token) == True:

                    token2 = token.replace(":", "_").replace("\t", "")
                    directorio = os.path.join(IMAGEDIR, token2)
                    fotos = [d for d in os.listdir(directorio) if not os.path.isdir(d)]

                    #Guardar en un directorio2 todas esas imagenes y añadirlo a la carpeta
                    for imagen in fotos:
                        directorio2 = os.path.join(directorio, imagen)
                        print(directorio2)
                        carpeta.add(directorio2, arcname=imagen)
            #Añadir cada una de las carpetas (con nombre del TimeStamp) a la carpeta general que las almacenara
            tar.add(carpeta)

    print("ARCHIVO CREADO")
    return tarfile

#Funcion para obtener un archivo comprimido del TimeStamp en el que se encuentra el usuario
#De esas imagenes y esa informacion concreta
def obtenerArchivo(token):
    t0 = time.localtime()
    # Obtener fecha y hora actual
    #NO ESTA GUARDANDO BIEN FECHA NI HORA (igual es cosa de mi ordenador...)
    ahora = time.strftime("%a-%b-%y %H:%M:%S",t0) + '.tar.gz'
    print('FECHA Y HORA: ' + ahora)
    # Guardar la informacion perteneciente a ese timestamp
    info = informationVersion2(token)
    info = {'info': info}
    #Directorio (Archivo) en el que se almacenará la info y fotos
    elarchivo = os.path.join('/home/energy/truckDataApp/mysite/logs/', ahora)


    #Abrir ese archivo
    with tarfile.open(elarchivo, 'w') as tar:
        #Añadirle la info
        with open('file.txt', 'w') as info_file:
            info_file.write(json.dumps(info))
        tar.add('file.txt')

        token = token.replace(":", "_")
        token = token.replace("\t", "")
        directorio = os.path.join(IMAGEDIR, token)

        #Añadirle cada una de esas imagenes pertenecientes al TimeStamp
        fotos = [d for d in os.listdir(directorio) if not os.path.isdir(d)]

        for imagen in fotos:
            directorio2 = os.path.join(directorio, imagen)
            print(directorio2)
            tar.add(directorio2, arcname=imagen)

    print("ARCHIVO CREADO")
    return tarfile

#View de la página principal
class HomePageView(TemplateView):

    template_name = "home.html"
    #Se necesita los TimeStamp, si existen esos directorios en imagenes o no,
    # un lodo de la app, y la apariencia
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tokens'] = logsVersion2()
        existen = {}
        for token in context['tokens']:
            existen[token] = comprobarDirectorio(token)

        context['sidirectorio'] = existen
        context['logo'] = '/design/camionbasura.png'
        context['apariencia'] = '/css/style.css'
        return context
#View de crear archivo comprimido de un timestamp concreto (Hace UPLOAD)
class CrearArchivoView(View):
    #Se necesita el archivo, pero no tiene que mostrar nada en lo que es la app
    def get(self, request, **kwargs):
        print("CLICK")
        obtenerArchivo(kwargs["token"])
        return HttpResponse('OK')
#View de crear archivo comprimido que incluya todos los timestamp y sus respectivas imagenes
#Hace upload
class CrearArchivoCompletoView(View):
    # Se necesita el archivo, pero no tiene que mostrar nada en lo que es la app
    def get(self, request):
        print("CLICK")
        obtenerArchivoCompleto()
        return HttpResponse('OK')
#View de la página que mostrará la info de cada timestamp y sus imagenes
class ImagePageView(TemplateView):

    template_name = "image.html"
    #Se necesitan las imagenes, la informacion referente a ese timeStamp,
    # el formato de ese diccionario (para hacer las columnas en visualizaion),
    # la apariencia de esa página y el logo
    def get_context_data(self, **kwargs):

       context = super().get_context_data(**kwargs)
       context['imagenes'] = imgs(kwargs["token"])
       context['info'] = informationVersion2(kwargs["token"])
       context['columnas'] = ['TimeStamp', 'Latitud', 'Longitud', 'NUM', 'IDPER', 'Ruta', 'FECHA', 'HORA','BRUTO', 'TARA', 'N_TAG']
       context['apariencia'] = '/css/style_image.css'
       context['logo'] = '/design/camionbasura.png'

       return context