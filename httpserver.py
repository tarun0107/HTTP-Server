from socket import *
import datetime
import os
import sys
import time
statuscodes = { 
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    204: 'No Content',
    301: 'Moved Permanently',
    304: 'Not Modified',
    400: 'Bad Request',
    403: 'Forbidden',
    404: 'Not Found',
    408: 'Request Timeout',
    411: 'Length Required',
    413: 'Payload Too Large',
    414: 'URI Too Long',
    415: 'Unsupported Media Type',
    501: 'Not Implemented' }
def date():
    x = datetime.datetime.now()
    date_time = x.strftime("%a") + ", " + x.strftime("%d %b %Y") + " " + x.strftime("%H:%M:%S")
    return date_time
extentions = {'txt': 'text/html; charset=iso-8859-1',
              'png': 'image/png',
              'jpg': 'image/jpg',
              'jpeg': 'image/jpeg',
              'mp4' : 'video/mp4',
              }
Headers = {
    'Date' : date(),
    'Server' : 'Apache/2.4.18 (Ubuntu)',
    'Connection' : 'Closed',
    'Accept-Ranges' : 'bytes',
    'Content-Length' : '10000',
    'Content-Type' : 'text/html; charset=iso-8859-1',
    'Content-Location' : '/file.html'
}
def status_line(statuscode):
    status = statuscodes[statuscode]
    response = "/HTTP 1.1 " + str(statuscode) + " " + status + "\r\n"
    return response
def get_headers(stcode, length = None, url = None,  extension = None, filename = None):
    response = status_line(stcode)
    for i in Headers:
        if i != 'Content-Length' or i != 'Content-Type' or i != 'Content-Location':
            response += i + " :" + Headers[i] + "\r\n"
        else:
            if i == 'Content-Length':
                response += i + " :" + str(length) + "\r\n"
            elif i == 'Content-Type' and extension != None:
                response += i + " :" + extentions[i] + "\r\n"
            elif i == 'Content-Location' and filename != None:
                x = url.split('/')
                location = ""
                for j in range(3, len(x)):
                    location += j + "/"
                response += i + " :" + location + "\r\n"
    return response
aud_vd = ['mp4', 'jpg', 'png', 'jpeg']
def HTTP_403():
    response_body = "<html><head><title>403 Forbidden</title></head><body><h1>408 Request Timeout</h1><p>You don't have permission to access this file on this server.</p><hr><address>My (Ubuntu) Server at 127.0.0.1 Port 12000</address></body></html>\n"
    l = len(response_body)
    response = get_headers(403, l)
    return response, response_body
def HTTP_404():
    response_body = "<html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1><p>The requested URL was not found on this server.</p><hr><address>My (Ubuntu) Server at 127.0.0.1 Port 12000</address></body></html>\n"
    l = len(response_body)
    response = get_headers(404, l)
    return response, response_body
def HTTP_415():
    response_body = "<html><head><title>415 Unsupported Media Type</title></head><body><h1>415 Unsupported Media Type</h1><p>The server refused the request because the request entity format is not supported by this server.</p><hr><address>My (Ubuntu) Server at 127.0.0.1 Port 12000</address></body></html>\n"
    l = len(response_body)
    response = get_headers(415, l)
    return response, response_body
def GET(url, headers = None):
    global status_code, respo
    final_url = url.split('/')
    file = final_url[-1]
    extension = final_url.split('.')[-1]
    if(os.access(file, os.access.F_OK) and os.access(file, os.access.R_OK) == False and url != None):
        response, response_body = HTTP_403()
    else:
        flag = 0
        if extension in extentions:
            try:
                if extension in aud_vd:
                    flag = 1
            except(UnboundLocalError):#assigning value to local variable before declaring it
                flag = 0
            if os.path.exists(file):
                if flag == 1:
                    f = open(file, 'rb')
                    response_body = f.read()
                else:
                    f = open(file, 'r')
                    response_body = f.read()
                l = len(response_body)
                response = get_headers(200, l, url, extension, file)
            else:
                response, response_body = HTTP_404()
        else:
            response, response_body = HTTP_415()


    return response, response_body
