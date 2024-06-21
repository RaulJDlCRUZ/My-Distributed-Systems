#!/usr/bin/env python3

import socket
from PaulaCastillejoBravo_Instawhat_pb2 import Release, Response


class Imagen:
    photoComments = [[] for x in range(1000)]
    photoPoints = [[] for x in range(1000)]
    nombre = ""
    like = 0
    CountPoints = 0
    CountComments = 0

    def __init__(self, url):
        self.nombre = url

    def add_comment(self, commend):
        self.photoComments[self.CountComments].append(commend)

    def add_point(self, point):
        self.photoPoints[self.CountPoints].append(point)

    def add_like(self):
        self.like = self.like+1


class Instawhat:
    photoList = [[] for x in range(1000)]
    CountImages = 0

    def imagen_exists(self, element_of_interest):
        i = 0
        while i < self.CountImages:
            image = self.photoList[i]
            if image.nombre == element_of_interest:
                return True
        return False

    def imagen_return(self, element_of_interest):
        i = 0
        while i < self.CountImages:
            image = self.photoList[i]
            if image.nombre == element_of_interest:
                return image
        return None

    def post(self, url):
        self.image = Imagen(url)
        self.photoList[self.CountImages] = self.image
        print(f'[-] Published photo.')
        self.CountImages += 1
        return Response.OK

    def delete(self, url):
        if self.imagen_exists(url):
            position = self.photoList.index(url)
            image = self.photoList[position]
            del image
            del self.photoList[position]
            print(f'[-] Eliminated photo.')
            return Response.OK

        print('[!] Photo do not exist in the system.')
        return Response.ERROR

    def comment(self, url, remark):
        if self.imagen_exists(url):
            imagen = self.imagen_return(url)
            imagen.add_comment(remark)
            print(f'[-] Commented photo.')
            return Response.OK

        print('[!] This imagen do not exists.')
        return Response.Error

    def rate(self, url, point):
        if self.imagen_exists(url):
            imagen = self.imagen_return(url)
            imagen.add_point(point)
            print(f'[-] Rated photo.')
            return Response.OK

        print('[!] This imagen do not exists.')
        return Response.OK

    def like(self, url):
        if self.imagen_exists(url):
            imagen = self.imagen_return(url)
            imagen.add_like()
            print(f'[-] Liked photo.')
            return Response.OK

        print('[!] This imagen do not exists.')
        return Response.Error

    def show(self):
        i = 0
        while i < self.CountImages:
            image = self.photoList[i]
            print(image.nombre)
            i += 1
        return Response.OK


def handle_client(client, instawhat):
    request_data = client.recv(1024)
    release = Release()
    release.ParseFromString(request_data)

    response = Response()
    response.id = release.id

    if release.option == Release.POST:
        response.result = instawhat.post(release.url)

    if release.option == Release.DELETE:
        response.result = instawhat.delete(release.url)

    if release.option == Release.COMMENTS:
        response.result = instawhat.comment(release.url, release.remark)

    if release.option == Release.RATE:
        response.result = instawhat.rate(release.url, release.points)

    if release.option == Release.LIKE:
        response.result = instawhat.like(release.url)

    if release.option == Release.SHOW:
        response.result = instawhat.show()

    client.send(response.SerializeToString())
    client.close()


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', 2002))
    server.listen(5)
    print('Servidor escuchando en el puerto 2002')

    instawhat = Instawhat()

    while True:
        client, address = server.accept()
        handle_client(client, instawhat)
