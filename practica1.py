#!/usr/bin/python3
"""
    Práctica 1 version 1.0
    Jaime Fernández Sánchez
    
    En principio todo funciona correctamente, pero probablemente se puedan
    implificar y mejorar cosas.
"""

import webapp
import csv


formulario = """
<form action = "" method = "POST">   
Introduzca la URL que desee acortar:<br>
<input type = "text" name = "url" required><br>   
<input type = "submit" value = "Acortar"> 
</form>
"""
global puerto
puerto = 4005

class PrototipoApp(webapp.webApp):

    urls_largas = {}
    urls_cortas = {}
    contador = 0

    def abrir_database(self):
        try:
            with open('urls_data.csv','r') as csvfile:
                urls = csv.reader(csvfile, delimiter = ',')
                for url in urls:
                    self.urls_largas[url[0]] = int(url[1])
                    self.urls_cortas[int(url[1])] = url[0]
                    self.contador = self.contador + 1
        except FileNotFoundError:                               #Si no encuentro la base de datos, o la elimino sin querer, la creo
            myfile = open('urls_data.csv','w')
            myfile.close()

    def add_http(sefl,url):
    	if url.startswith('http://'):
    		return url
    	elif url.startswith('https://'):
    		return url
    	else:
    		url = ('http://') + url
    		return url


    def crear_enlaces(self,url,delimiter):                      #El delimitador me indica como separo los dos enlaces
        enlace_1 = ("<html><a href =" + str(self.urls_largas[url]) + 
            ">" + url + "</a>") 
        enlace_2 = ("<a href = " + str(self.urls_largas[url]) + 
            ">" + "http://localhost:" + str(puerto) + "/" + 
            str(self.urls_largas[url]) + "</a></html>")
        enlaces = enlace_1 + delimiter + enlace_2
        return enlaces

    def lista_urls(self):                                 
        titulo = "Lista de URLs acortadas:<br>"
        lista = ""
        for url in self.urls_largas:
            enlaces = self.crear_enlaces(url," , ")
            lista = lista + enlaces +"<br>"
        lista = titulo + lista
        return lista

    def menu(self,formulario):
        titulo = "<html><head><title>AcortaTusURLs</title></head>"
        titular = "<body><h1>El mejor acortador de URLs de Internet</h1>"
        cuerpo = formulario + self.lista_urls() + "</body></html>"
        return(titulo + titular + cuerpo)

    def reescribir_database(self):
        with open('urls_data.csv','w',newline = '') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            for url_larga in self.urls_largas:
                writer.writerow([url_larga]+[self.urls_largas[url_larga]])        

    def parse(self,request):
        try:
            request_1 = request.split()[0]
            request_2 = request.split()[1]
            request_3 = request
            return(request_1,request_2,request_3)
        except IndexError:
            return(None,None,None)                              #En el caso de recibir cualquier cosa no deseada, no devuelvo nada

    def process(self,parsedRequest):
        metodo,recurso,peticion = parsedRequest

        if metodo == "GET": 
            if recurso == "/":
                return ("200 OK", self.menu(formulario))
            elif recurso == "/favicon.ico":
                return ("200 OK", "<html><body><h1>Vete!</h1></body></html>")
            else:
                try:
                    recurso = int(recurso.split("/")[1])
                    url_dest = self.urls_cortas[recurso]
                    redirect = ("<html>" + "<meta http-equiv='refresh'"
                    + "content='1 url= " + url_dest + "'>" 
                    + "</html>")
                    return("302 Redirect", redirect)
                except KeyError:
                    return ("404 Not Found","<html><body><h1>HTTP ERROR: "
                        "Recurso no disponible</h1></body></html>")

        elif metodo == "POST":
            try: 
                url = peticion.split("url=")[1]
                url = self.add_http(url)
                if url in self.urls_largas:
                    return("200 OK",self.crear_enlaces(url,"<br>"))

                else:
                    self.urls_cortas[self.contador] = url
                    self.urls_largas[url] = self.contador
                    self.reescribir_database()
                    self.contador = self.contador + 1

                    return("200 OK",self.crear_enlaces(url,"<br>"))
            except IndexError:
                return ("404 Not Found","<html><body><h1>Error: "
                    "POST sin URL</h1></body></html>")                
        else:
            return ("404 Not Found","<html><body><h1>Error</h1></body></html>")

    def __init__(self,hostname,port):
        self.abrir_database()
        print(self.urls_largas)
        print(self.urls_cortas)
        super().__init__(hostname, port)

if __name__ == "__main__":
    testApp = PrototipoApp("localhost",puerto)