from socket import *
import datetime
import os
import sys
import time
from threading import *
from conf import *
import base64
import binascii
statuscodes = { 
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    204: 'No Content',
    301: 'Moved Permanently',
    304: 'Not Modified',
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    408: 'Request Timeout',
    411: 'Length Required',
    412: 'Precondition Failed',
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
    'Last-Modified' : 'Mon, 19 Aug 2021 12∶51∶23 GMT',
    'Connection' : 'Closed',
    'Accept-Ranges' : 'bytes',
    'Content-Length' : '10000',
    'Content-Type' : 'text/html; charset=iso-8859-1',
    'Content-Location' : '/file.html'
}
Months = {'Jan' : 1, 'Feb' : 2, 'Mar' : 3, 'Apr' : 4, 'May' : 5, 'Jun' : 6, 
'Jul' : 7, 'Aug' : 8, 'Sep' : 9, 'Oct' : 10, 'Nov' : 11, 'Dec' : 12}

versions = {"1.0", "1.1"}

def write_log(stcode, time1, url, file):
    time1 = time1.strftime("%d/%b/%Y:%H:%M:%S")
    method = url[0:6] 
    if(stcode == 200 and method == 'DELETE'):
        log = "127.0.0.1 - - " + "[" + str(time1) + " +0530] "  + '"' + url + '" ' + str(stcode) + " 0" + ' "-" "-"\r\n' 
    elif(stcode == 400 or stcode == 415 or stcode == 404 or stcode == 414 or stcode == 403 or stcode == 401 or stcode == 411 or stcode == 413 or stcode == 501):
        log = "127.0.0.1 - - " + "[" + str(time1) + " +0530] "  + '"' + url + '" ' + str(stcode) + " 0" + ' "-" "-"\r\n' 
    elif(stcode == 200 or stcode == 201 or stcode == 204 or stcode == 304 or stcode == 202):
        log = "127.0.0.1 - - " + "[" + str(time1) + " +0530] "  + '"' + url + '" ' + str(stcode) + " " + str(os.stat(file).st_size) + ' "-" "-"\r\n' 
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
                response += i + " : " + str(time1) + '\r\n'
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
    
def user_auth(data):
    h = data[0].split(' : ')
    headers = h[1].split(' ')[1]
    try:
        user_pass = base64.b64decode(headers).decode("ascii")
        user = user_pass.split(":")[0]
        pass1 = user_pass.split(":")[1]
        print(user, pass1)
        if user == username and pass1 == password:
            return True
    except(binascii.Error):
        return False
    return False
def HTTP_400():
    stcode = 400
    response_body = "<html>\n<head>\n<title>400 Bad Request</title>\n</head>\n<body>\n<p>Server could not understand the request you sent.</p>\n<hr>\n<address>Apache/2/4/18 (Ubuntu) Server at 127.0.0.1 </address>\n</body>\n</html>\n"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(400, date_time, l)
    return response, response_body
def HTTP_401():
    stcode = 401
    response_body = "<html>\n<head>\n<title>401 Unauthorized</title>\n</head>\n<body>\n<p>You are not allowed to make changes.</p>\n<hr>\n<address>Apache/2/4/18 (Ubuntu) Server at 127.0.0.1 </address>\n</body>\n</html>\n"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(401, date_time, l)
    return response, response_body
def HTTP_403():
    stcode = 403
    response_body = "<html>\n<head>\n<title>403 Forbidden</title>\n</head>\n<body>\n<p>You don't have permission to access this file on this server.</p>\n<hr>\n<address>Apache/2/4/18 (Ubuntu) Server at 127.0.0.1 </address>\n</body>\n</html>\n"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(403, date_time, l)
    return response, response_body
def HTTP_404():
    stcode = 404
    response_body = "<html>\n<head>\n<title>404 Not Found</title>\n</head>\n<body>\n<h1>404 Not Found</h1>\n<p>The requested URL was not found on this server.</p>\n<hr>\n<address>Apache 2.4.18 (Ubuntu) Server at 127.0.0.1 </address>\n</body>\n</html>\n"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(404, date_time, l)
    return response, response_body
def HTTP_411():
    stcode = 411
    response_body = "<html>\n<head>\n<title>411 Length Required</title>\n</head>\n<body>\n<hr>\n<address>Apache 2.4.18 (Ubuntu) Server at 127.0.0.1 </address>\n</body>\n</html>\n"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(411, date_time, l)
    return response, response_body
def HTTP_412():
    stcode = 412
    response_body = "<html>\n<head>\n<title>412 Precondition Failed</title>\n</head>\n<body>\n<h4>The requested process can't be processed</h4>\n</body><\html>"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(412, date_time, l)
    return response, response_body
def HTTP_413():
    stcode = 413
    response_body = "<html>\n<head>\n<title>413 Payload Too Large</title>\n</head>\n<body>\n<h4>The requested payload was too long for server to process.</h4>\n<hr>\n<address>Apache/2.4.18 (Ubuntu) Server at 127.0.0.1</address>\n</body>\n</html>"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(413, date_time, l)
    return response, response_body
def HTTP_414():
    stcode = 414
    response_body = "<html>\n<head>\n<title>414 URI Too Long</title>\n</head>\n<body>\n<h4>The requested URI was too long for server to process.</h4>\n<hr>\n<address>Apache/2.4.18 (Ubuntu) Server at 127.0.0.1</address>\n</body>\n</html>"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(414, date_time, l)
    return response, response_body
def HTTP_415():
    stcode = 415
    response_body = "<html>\n<head>\n<title>415 Unsupported Media Type</title>\n</head>\n<body>\n<h1>415 Unsupported Media Type</h1>\n<p>The server refused the request because the request entity format is not supported by this server.</p>\n<hr>\n<address>Apache/2.4.18 (Ubuntu) Server at 127.0.0.1 </address>\n</body>\n</html>\n"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(415, date_time, l)
    return response, response_body
def HTTP_501():
    stcode = 501
    response_body = "<html>\n<head>\n<title>501 Not Implemented</title>\n</head>\n</html>"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(501, date_time, l)
    return response, response_body
def GET(url, connectionsocket, addr, data):
    url_len = len(url)
    global stcode
    flag = 0
    if url_len > max_uri_len:
        response, response_body = HTTP_414()
        stcode = 414
        return response, response_body
    headers = data.split('\r\n')
    ims = [string for string in headers if "If-Modified-Since" in string]
    ius = [string for string in headers if "If-Unmodified-Since" in string]
    final_url = url.split('/')
    filename = final_url[-1]
    file = url
    if len(ims) > 0:
        date = ims[0].split(' : ')
        date = date[-1]
        ifms = if_modified_since(date, file)
    else:
        ifms = 1
    if len(ius) > 0:
        date = ius[0].split(' : ')
        date = date[-1]
        ifus = if_modified_since(date, file)
    else:
        ifus = 1
    extension = final_url[-1].split('.')
    extension = extension[-1]
    if(os.path.exists(file) and (os.access(file, os.W_OK) == False or os.access(file, os.R_OK) == False) and url != None): 
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
            elif(ifus == 0):
                if(os.path.exists(file)):
                    date_time1 = datetime.datetime.now()
                    date_time = givedate(date_time1) 
                    stcode = 200
                    if flag == 1:
                        f = open(file, 'rb')
                        response_body = f.read()
                    else:
                        f = open(file, 'r')
                        response_body = f.read()
                    l = len(response_body)
                    response = get_headers(stcode, date_time, l, url, extension, file)
                else:
                    stcode = 404
                    response, response_body = HTTP_404()
            elif (ifus):
                stcode = 412
                response, response_body = HTTP_412()

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

def POST(url, connectionsocket, addr, data):
    url_len = len(url)
    global stcode
    flag = 0
    url1 = "POST " + url
    if url_len > max_uri_len:
        response, response_body = HTTP_414()
        stcode = 414
        write_log(414, datetime.datetime.now(), url1, url)
        return response, response_body
    lines = data.split('\r\n')
    lines_to_post = lines[-2]
    file = url
    flag = 0
    extention = file.split('.')[-1]
    if (os.path.exists(file) and (os.access(file, os.W_OK) == False or os.access(file, os.R_OK) == False) and url != None):
        stcode = 403
        response, response_body = HTTP_403()
        write_log(stcode, datetime.datetime.now(), url, file)
    else:
            if extention in extentions:
                try:
                    if extention in aud_vd:
                        flag = 1
                except(UnboundLocalError):#assigning value to local variable before declaring it
                    flag = 0
                if os.path.exists(file):
                    if len(lines_to_post) > max_payload:
                        stcode=413
                        response, response_body = HTTP_413()
                        time1 = datetime.datetime.now().strftime("%d/%b/%Y:%H:%M:%S")
                        log = "127.0.0.1 - - " + "[" + str(time1) + " +0530] "  + '"POST' + url + '" ' + str(stcode) + " " + str(os.stat(file).st_size) + ' "-" "-"\r\n'
                    else:
                        stcode = 200
                        response_body = lines_to_post
                        date_time1 = datetime.datetime.now()
                        date_time = givedate(date_time1)
                        response = get_headers(200, date_time, len(response_body), url, extention, file)
                        date_time = datetime.datetime.now().strftime("%d/%b/%Y:%H:%M:%S")
                        log = "127.0.0.1 - - " + "[" + str(date_time) + " +0530] "  + '"' + url1 + '" ' + str(stcode) + " " + str(os.stat(file).st_size) + ' "-" "-" ' + lines_to_post + '\r\n'
                    f = open('access.log', 'a')
                    f.write(log)
                else:
                    stcode = 404
                    response, response_body = HTTP_404()
                    write_log(stcode, datetime.datetime.now(), url1, file)
            else:
                stcode = 415
                response, response_body = HTTP_415()
                write_log(stcode, datetime.datetime.now(), url1, file)
    return response, response_body

def DELETE(url, connectionsocket, addr, data):
    url_len = len(url)
    global stcode
    flag = 0
    url1 = "DELETE " + url
    auth = data.split('\r\n')
    auth_flag = [string for string in auth if "Authorization" in string]
    if url_len > max_uri_len:
        response, response_body = HTTP_414()
        stcode = 414
        return response, response_body
    file = url
    extention = file.split('.')[-1]
    if(os.path.exists(file) and (os.access(file, os.W_OK) == False or os.access(file, os.R_OK) == False) and url != None):
        stcode = 403
        response, response_body = HTTP_403()
        write_log(stcode, datetime.datetime.now(), url1, file)
    else:
        if extention in extentions:     
            try:
                if extention in aud_vd:
                    flag = 1
            except(UnboundLocalError):
                flag = 0
            if os.path.exists(file):
                if auth_flag :
                    if user_auth(auth_flag):
                        if flag == 1:
                            f = open(file, 'rb')
                            text = f.read()
                        else:
                            f = open(file, 'r')
                            text = f.read()
                        le = len(text)
                        if le == 0:
                            stcode = 204
                            date_time1 = datetime.datetime.now()
                            date_time = givedate(date_time1)
                            l = 0
                            response = get_headers(stcode, date_time, l, url, extention, file)
                            response_body = ""
                        else:
                            stcode = 200
                            response_body = "<html>\n<body>\n<h1>File deleted.</h1>\n</body>\n</html>"
                            date_time1 = datetime.datetime.now()
                            date_time = givedate(date_time1)
                            response = get_headers(stcode, date_time, len(response_body), url, extention, file)
                        os.remove(file)
                    else:
                        stcode = 401
                        response, response_body = HTTP_401()
                else:
                    if flag == 1:
                        f = open(file, 'rb')
                        text = f.read()
                    else:
                        f = open(file, 'r')
                        text = f.read()
                    le = len(text)
                    if le == 0:
                        stcode = 204
                        date_time1 = datetime.datetime.now()
                        date_time = givedate(date_time1)
                        l = 0
                        response = get_headers(stcode, date_time, l, url, extention, file)
                        response_body = ""
                    else:
                        stcode = 200
                        response_body = "<html>\n<body>\n<h1>File deleted.</h1>\n</body>\n</html>"
                        date_time1 = datetime.datetime.now()
                        date_time = givedate(date_time1)
                        response = get_headers(stcode, date_time, len(response_body), url, extention, file)
                    os.remove(file)

            else:
                stcode = 404
                response, response_body = HTTP_404()
        else:
            stcode = 415
            response, response_body = HTTP_415()
    return response, response_body

def PUT(url, connectionsocket, addr, data):
    url_len = len(url)
    global stcode
    flag = 0 
    if url_len > max_uri_len:
        response, response_body = HTTP_414()
        stcode = 414
        return response, response_body
    data = data.split('\r\n')
    lines = data[-2]
    file = url
    url1 = "PUT " + url
    cont_len = [string for string in data if "Content-Length" in string]
    auth = [string for string in data if "Authorization" in string]
    extention = file.split('.')[-1]
    if (os.path.exists(file) and (os.access(file, os.W_OK) == False or os.access(file, os.R_OK) == False) and url != None):
        stcode = 403
        response, response_body = HTTP_403()    
    else:
        if extention in extentions:
            if cont_len:
                if len(lines) < max_payload:
                    if os.path.exists(file):
                        if auth:
                            if user_auth(auth):
                                f = open(file, "w")
                                f.write(lines)
                                stcode = 200
                                response_body = lines
                                date_time1 = datetime.datetime.now()
                                date_time = givedate(date_time1)
                                response = get_headers(stcode, date_time, len(lines), url, extention, file)
                        
                            else:
                                stcode = 401
                                response, response_body = HTTP_401()
                        else:
                            f = open(file, 'w')
                            f.write(lines)
                            stcode = 200
                            response_body = lines
                            date_time1 = datetime.datetime.now()
                            date_time = givedate(date_time1)
                            response = get_headers(stcode, date_time, len(lines), url, extention, file)
                    else:
                        f = open(file, 'x')
                        f = open(file, 'w')
                        f.write(lines)
                        stcode= 201
                        response_body = lines
                        date_time1 = datetime.datetime.now()
                        date_time = givedate(date_time1)
                        response = get_headers(stcode, date_time, len(lines), url, extention, file)
                        
                else:
                    stcode = 413
                    response, response_body = HTTP_413()

            else:
                stcode = 411
                response, response_body = HTTP_411()
        else:
            stcode = 415
            response, response_body = HTTP_415()  
    if stcode == 411 or stcode == 413 or stcode == 403:
        write_log(stcode, datetime.datetime.now(), url1, file)
    else:
        log = "127.0.0.1 - - " + "[" + str(date_time) + " +0530] "  + '"' + url1 + '" ' + str(stcode) + " " + len(lines) + ' "-" "-"\r\n'
        f = open('access.log', 'a')
        f.write(log)
    return response, response_body

def HEAD(url, connectionsocket, addr, data):
    url_len = len(url)
    global stcode 
    if url_len > max_uri_len:
        response, response_body = HTTP_414()
        stcode = 414
        return response
    data = data.split('\r\n')
    url1 = "HEAD " + url
    file = url
    extention = file.split('.')[-1]
    headers = data.split('\r\n')
    ims = [string for string in headers if "If-Modified-Since" in string]
    ius = [string for string in headers if "If-Unmodified-Since" in string]
    if len(ims) > 0:
        date = ims[0].split(' : ')
        date = date[-1]
        ifms = if_modified_since(date, file)
    else:
        ifms = 1
    if len(ius) > 0:
        date = ius[0].split(' : ')
        date = date[-1]
        ifus = if_modified_since(date, file)
    else:
        ifus = 1
    if (os.path.exists(file) and (os.access(file, os.W_OK) == False or os.access(file, os.R_OK) == False) and url != None):
        stcode = 403
        response, response_body = HTTP_403() 
    else:
        if extention in extentions:
            try:
                if extention in aud_vd:
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
                date_time1 = datetime.datetime.now()
                date_time = givedate(date_time1)
                if ifms == 0:
                    stcode = 304
                elif ifus == 1:
                    stcode == 412
                else:
                    stcode = 200
                response = get_headers(200, date_time,l, url, extention, file)
            else:
                stcode = 404
                response, response_body = HTTP_404()
    return response 

def HTTPRequest(request):
    version = '1.1'
    request = request.split('\r\n')
    words = request[0].split(' ')
    method = words[0]
    url = words[1]
    if len(words) > 2:
        version = words[2].split('/')[-1]
    return version, method, url
def call_methods(connectionsocket, addr, data):
    global stcode 
    data = data.decode()
    fp = data.split('\r\n')
    time1 = datetime.datetime.now()
    version, method, url = HTTPRequest(data)
    print(version)
    if version not in versions:
        stcode = 400
        response, response_body = HTTP_400()
        res = response + response_body
        connectionsocket.sendall(res.encode())
        write_log(stcode, datetime.datetime.now(), fp[0], url)
    if method == 'GET':
        response, response_body = GET(url, connectionsocket, addr, data)
        res = response + response_body
        connectionsocket.send(res.encode())
        write_log(stcode, time1, fp[0], url)
    elif method == 'POST':
        response, response_body = POST(url, connectionsocket, addr, data)
        res = response + response_body
        connectionsocket.sendall(res.encode())
    elif method == 'DELETE':
        response, response_body = DELETE(url, connectionsocket, addr, data)
        res = response + response_body
        connectionsocket.sendall(res.encode())
        write_log(stcode, datetime.datetime.now(), fp[0], url)
    elif method == 'PUT':
        response, response_body = PUT(url, connectionsocket, addr, data)
        res = response + response_body
        connectionsocket.sendall(res.encode())
    elif method == 'HEAD':
        response = HEAD(url, connectionsocket, addr, data)
        connectionsocket.sendall(response.encode())
        write_log(stcode, datetime.datetime.now(), fp[0], url) 
    else:
        stcode = 501
        response, response_body = HTTP_501()
        connectionsocket.sendall((response+response_body).encode())
        write_log(stcode, datetime.datetime.now(), fp[0], url)

def start_restart_stop(serversocket, serverport, host):
    while True:
        action = input()
        action = action.lower()
        if action == 'stop':
            serversocket.close()
            print("Exiting...")
            os._exit(0)
            break
        elif action == 'restart':
            print("Restarting...")
            time.sleep(5)
            serversocket.bind(('127.0.0.1', serverport))
            serversocket.listen(10)
            print("Restarted...")
serversocket = socket(AF_INET, SOCK_STREAM)
serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
servername = '127.0.0.1'
serverport = int(sys.argv[1])
host = serversocket.getsockname()
serversocket.bind(('', serverport))
serversocket.listen(10)
Thread1 = Thread(target=start_restart_stop, args=(serversocket, serverport, host))
Thread1.start()
while True:
    connectionsocket, addr = serversocket.accept()
    print("Connected By :", addr)
    data = (connectionsocket.recv(8192))
    call_methods(connectionsocket, addr, data)