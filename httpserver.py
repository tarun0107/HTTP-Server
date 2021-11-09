from socket import *
import datetime
import os
import sys
import time
from threading import *
max = 128
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
def givedate(x):
    date_time = x.strftime("%a") + ", " + x.strftime("%d %b %Y") + " " + x.strftime("%H:%M:%S") + " GMT"
    return date_time
extentions = {'txt': 'text/plain',
              'png': 'image/png',
              'jpg': 'image/jpg',
              'jpeg': 'image/jpeg',
              'mp4' : 'video/mp4',
              'html' : 'text/html; charset=iso-8859-1',
              'mpeg' : 'audio/mpeg'
              }
Headers = {
    'Date' : 'Time',
    'Server' : 'Apache/2.4.18 (Ubuntu)',
    'Last-Modified' : 'Mon, 18 Aug 2020 12∶51∶23 GMT',
    'Connection' : 'Closed',
    'Accept-Ranges' : 'bytes',
    'Content-Length' : '10000',
    'Content-Type' : 'text/html; charset=iso-8859-1',
    'Content-Location' : '/file.html'
}
Months = {'Jan' : 1, 'Feb' : 2, 'Mar' : 3, 'Apr' : 4, 'May' : 5, 'Jun' : 6, 
'Jul' : 7, 'Aug' : 8, 'Sep' : 9, 'Oct' : 10, 'Nov' : 11, 'Dec' : 12}

def write_access_log(stcode, time1, url, file):
    time1 = time1.strftime("%d/%b/%Y:%H:%M:%S")
    method = url[0:6] 
    if(stcode == 200 and method == 'DELETE'):
        log = "127.0.0.1 - - " + "[" + str(time1) + " +0530] "  + " " + url + " " + str(stcode) + " 0" + '"-" "-"\r\n' 
    elif(stcode == 400 or stcode == 415 or stcode == 404 or stcode == 414 or stcode == 403):
        log = "127.0.0.1 - - " + "[" + str(time1) + " +0530] "  + " " + url + " " + str(stcode) + " 0" + '"-" "-"\r\n' 
    elif(stcode == 200 or stcode == 201 or stcode == 204 or stcode == 304 or stcode == 202):
        log = "127.0.0.1 - - " + "[" + str(time1) + " +0530] "  + " " + url + " " + str(stcode) + " " + str(os.stat(file).st_size) + '"-" "-"\r\n' 
    fp = open('access.log', 'a')
    fp.write(log) 

def status_line(statuscode):
    status = statuscodes[statuscode]
    response = "HTTP/1.1 " + str(statuscode) + " " + status + ' \n'
    return response

def get_headers(stcode, time1, length = None, url = None,  extension = None, filename = None):
    response = status_line(stcode)
    for i in Headers:
        if i != 'Content-Length' and i != 'Content-Type' and i != 'Content-Location' and i != 'Date' and i!= 'Last-Modified':
            response += i + " : " + Headers[i] + "\r\n"
        else:
            if i == 'Content-Length':
                response += i + " : " + str(length) + "\r\n"
            elif i == 'Content-Type' and extension != None:
                response += i + " : " + extentions[extension] + "\r\n"
            elif i == 'Content-Location' and filename != None:
                response += i + " : " + filename + "\r\n"
            elif i == 'Date':
                response += i + " : " + time1 + '\r\n'
            elif i == 'Last-Modified':
                if filename != None:
                    date2 = time.ctime(os.path.getmtime(filename))
                    date2 = date2.split(" ")
                    new = date2[0] + ", " + date2[2] + " " + date2[1] + " " + date2[-1] + " " + date2[-2]
                    response += i + " : " + str(new) + '\r\n'
    return response
aud_vd = ['mp4', 'jpg', 'png', 'jpeg']

def if_modified_since(date, file):
    modidate = time.ctime(os.path.getmtime(file))
    modidate = modidate.split(" ")
    new = modidate[0] + ", " + modidate[2] + " " + modidate[1] + " " + modidate[-1] + " " + modidate[-2]
    flag = 0
    new = new.split(' ')
    date = date.split(' ')
    if new[3] >= date[3]:
        if Months[new[2]] >= Months[date[2]]:
            if new[1] > date[1]:
                flag = 1
            elif new[1] == date[1]:
                if new[4] > date[4]:
                    flag = 1
    return flag

def HTTP_403():
    response_body = "<html>\n<head>\n<title>403 Forbidden</title>\n</head>\n<body>\n<p>You don't have permission to access this file on this server.</p>\n<hr>\n<address>My (Ubuntu) Server at 127.0.0.1 </address>\n</body>\n</html>\n"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(415, date_time, l)
    return response, response_body
def HTTP_404():
    response_body = "<html>\n<head>\n<title>404 Not Found</title>\n</head>\n<body>\n<h1>404 Not Found</h1>\n<p>The requested URL was not found on this server.</p>\n<hr>\n<address>My (Ubuntu) Server at 127.0.0.1 </address>\n</body>\n</html>\n"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(404, l)
    return response, response_body
def HTTP_414():
    response_body = "<html>\n<head>\n<title>414 URI Too Long</title>\n</head>\n<body>\n<h4>The requested URI was too long for server to process.</h4>\n<hr>\n<address>Apache/2.4.41 (Ubuntu) Server at 127.0.0.1</address>\n</body>\n</html>"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(415, date_time, l)
    return response, response_body
def HTTP_415():
    response_body = "<html>\n<head>\n<title>415 Unsupported Media Type</title>\n</head>\n<body>\n<h1>415 Unsupported Media Type</h1>\n<p>The server refused the request because the request entity format is not supported by this server.</p>\n<hr>\n<address>My (Ubuntu) Server at 127.0.0.1 </address>\n</body>\n</html>\n"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(415, date_time, l)
    return response, response_body

def GET(url, connectionsocket, addr, data):
    url_len = len(url)
    flag = 0
    if url_len > 128:
        response, response_body = HTTP_414()
        return response, response_body
    global status_code, respo
    headers = data.split('\r\n')
    ims = [string for string in headers if "if-modified-since" in string]
    final_url = url.split('/')
    filename = final_url[-1]
    file = url
    if len(ims) > 0:
        date = ims[0].split(' : ')
        date = date[-1]
        ifms = if_modified_since(date, file)
    extension = final_url[-1].split('.')
    extension = extension[-1]
    if(os.access(file, os.F_OK) and os.access(file, os.R_OK) == False and url != None):
        stcode = 403
        response, response_body = HTTP_403()
    else:
        if extension in extentions:
            try:
                if extension in aud_vd:
                    flag = 1
            except(UnboundLocalError):#assigning value to local variable before declaring it
                flag = 0
            
            if(ifms == 0):
                if(os.path.exists(file)):
                    date_time1 = datetime.datetime.now()
                    date_time = givedate(date_time1)
                    response_body = ""
                    stcode = 304
                    response = get_headers(304, date_time,len(response_body), url, extension, file)
                else:
                    stcode = 404
                    response, response_body = HTTP_404()
            else:
                if os.path.exists(file):
                    if flag == 1:
                        f = open(file, 'rb')
                        response_body = f.read()
                    else:
                        f = open(file, 'r')
                        response_body = f.read()
                    l = len(response_body)
                    date_time1 = datetime.datetime.now()
                    date_time = givedate(date_time1)
                    stcode = 200
                    response = get_headers(200, date_time,l, url, extension, file)
                else:
                    stcode = 404
                    response, response_body = HTTP_404()
        else:
            stcode = 415
            response, response_body = HTTP_415()
    return response, response_body

def HTTPRequest(request):
    version = '1.1'
    request = request.split('\r\n')
    words = request[0].split(' ')
    method = words[0]
    url = words[1]
    if len(words) > 2:
        version = words[2]
    return version, method, url
def call_methods(connectionsocket, addr, data):
    global stcode 
    data = data.decode()
    fp = data.split('\r\n')
    print(fp[0])
    version, method, url = HTTPRequest(data)
    if method == 'GET':
        response, response_body = GET(url, connectionsocket, addr, data)
        res = response + response_body
        connectionsocket.send(res.encode())
def start_restart_stop(serversocket):
    while True:
        action = input()
        action = action.lower()
        if action == 'stop':
            serversocket.close()
            print("Exiting...")
            os._exit(0)
            break

serversocket = socket(AF_INET, SOCK_STREAM)
servername = '127.0.0.1'
serverport = int(sys.argv[1])
serversocket.bind(('', serverport))
serversocket.listen(10)

print(serversocket)
while True:
    connectionsocket, addr = serversocket.accept()
    print("Connected By :", addr)
    data = (connectionsocket.recv(8192))
    call_methods(connectionsocket, addr, data)
 