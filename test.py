import requests
from socket import *
import sys
servername = '127.0.0.1'
serverport = int(sys.argv[1])
url = "http://127.0.0.1:" + str(serverport)
def part1():
#get
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((servername,serverport))
    request = "GET /home/tarun/index.html HTTP/1.1\r\n"
    clientsocket.send(request.encode())
    response = clientsocket.recv(2048)
    clientsocket.close()
#head
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((servername,serverport))
    request = "HEAD /home/tarun/index.html HTTP/1.1\r\n"
    clientsocket.send(request.encode())
    response = clientsocket.recv(2048)
    clientsocket.close()

#post
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((servername,serverport))
    request = "POST /home/tarun/index.html HTTP/1.1\r\nThis is a http server."
    clientsocket.send(request.encode())
    response = clientsocket.recv(2048)
    clientsocket.close()
#put
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((servername,serverport))
    request = "PUT /home/tarun/index.html HTTP/1.1\r\nContent-Length : 16\r\nMy Name is Tarun"
    clientsocket.send(request.encode())
    response = clientsocket.recv(2048)
    clientsocket.close()
#delete
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((servername,serverport))
    request = "DELETE /home/tarun/index0.html HTTP/1.1\r\n"
    clientsocket.send(request.encode())
    response = clientsocket.recv(2048)
    clientsocket.close()

def part2():
    #get
    requests.get(url + "/nfeobioehbierhbiuernbuiebuibuirbjiebfnujerbviuebvijnvjfjbjibbejivnfejbnrjinbjiernbjernjkdhthfdhgfjfgjfgdfjftjdfhfgjghjjghdtagsjfykerfzsdhjghjcgzsyjsyshcvbvubvuherbvuebvuh.html")
    requests.get(url + "/home/tarun/http.pcap")
    requests.get(url + "/home/tarun/Car.jpeg")
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((servername,serverport))
    request = "GET /home/tarun/hi.html HTTP/1.1\r\nIf-Modified-Since : Sun, 14 Nov 2021 08∶17∶00 GMT"
    clientsocket.send(request.encode())
    response = clientsocket.recv(2048)
    clientsocket.close()
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((servername,serverport))
    request = "GET /home/tarun/index.html HTTP/1.1\r\nIf-Unmodified-Since : Sun, 13 Nov 2021 07∶17∶00 GMT"
    clientsocket.send(request.encode())
    response = clientsocket.recv(2048)
    clientsocket.close()
    #post
    requests.post(url + "/home/tarun/form.txt", data="hii")
    requests.post(url + "/home/tarun/test.txt", data="Hello.")
    #delete
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((servername,serverport))
    request = "DELETE /home/tarun/moodle.html HTTP/1.1\r\nAuthorization : dGFydW46dHJ0MTcwMQ=="
    clientsocket.send(request.encode())
    response = clientsocket.recv(2048)
    clientsocket.close()
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((servername,serverport))
    request = "DELETEEE /home/tarun/moodle.html HTTP/1.1\r\nAuthorization : dGFydW46dHJ0MTcwMQ=="
    clientsocket.send(request.encode())
    response = clientsocket.recv(2048)
    clientsocket.close()
    #head
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((servername,serverport))
    request = "HEAD /home/tarun/index.html HTTP/1.1\r\nIf-Modified-Since : Sun, 14 Nov 2021 07∶17∶00 GMT"
    clientsocket.send(request.encode())
    response = clientsocket.recv(2048)
    clientsocket.close()
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((servername,serverport))
    request = "HEAD /home/tarun/index.html HTTP/2.1\r\nIf-Modified-Since : Sun, 14 Nov 2021 07∶17∶00 GMT"
    clientsocket.send(request.encode())
    response = clientsocket.recv(2048)
    clientsocket.close()
    requests.head(url + "/home/tarun/Car.png")
    requests.head(url + "/home/tarun/demo.mp4")
    #put
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((servername,serverport))
    request = "PUT /home/tarun/form.txt HTTP/1.1\r\nContent-Length : 63\r\nMy Name is Tarun. I study in COEP. This is my CN course projecthbierhbiuernbuiebuibuirbjiebfnujerbviuebvijnvjfjbjibbejivnfejbnrjinbjiernbjernjkdhthfdhgfjfgjfgdfjftjdfhfgjghjjghdtagsjfykerfzsdhjghjcgzsyjsyshcvbvubvuherbvuebv"
    clientsocket.send(request.encode())
    response = clientsocket.recv(2048)
    clientsocket.close()
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((servername,serverport))
    request = "PUT /home/tarun/form.html HTTP/1.1\r\nContent-Length : 63\r\nAuthorization : dGFydW46dHJ0MTcwMQ\r\nMy Name is Tarun. I study in COEP. This is my CN course project"
    clientsocket.send(request.encode())
    response = clientsocket.recv(2048)
    clientsocket.close()
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((servername,serverport))
    request = "PUT /home/tarun/form.html HTTP/1.1\r\nAuthorization : dGFydW46dHJ0MTcwMQ\r\nMy Name is Tarun. I study in COEP. This is my CN course project"
    clientsocket.send(request.encode())
    response = clientsocket.recv(2048)
    clientsocket.close()
part1()
print("Part 1 Done\n")
part2()
print("Part 2 Done\n")


