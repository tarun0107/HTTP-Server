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
Headers = {
    'Date' : date(),
    'Server' : 'Apache/2.4.18 (Ubuntu)',
    'Connection' : 'Closed',
    'Accept-Ranges' : 'bytes',
    'Content-Encoding' : 'gzip',
    'Content-Length' : '10000',
    'Content-Type' : 'text/html; charset=iso-8859-1',
    'Content-Location' : '/file.html'
}
def status_line(statuscode):
    status = statuscodes[statuscode]
    response = "HTTP 1.1 " + str(statuscode) + " " + status + "\r\n"
    return response

