from socket import *
import datetime
import os
import sys
import time
from threading import *
from conf import *
import base64
import binascii
import random
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
    501: 'Not Implemented',
    503: 'Service Unavailable',
    505: 'HTTP Version Not Supported' }
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
    'Accept-Ranges' : 'bytes',
    'Content-Length' : '10000',
    'Content-Type' : 'text/html; charset=iso-8859-1',
    'Content-Location' : '/file.html',
    'Set-Cookie' : 'tarun',
    'Connection' : 'Closed',
}
Months = {'Jan' : 1, 'Feb' : 2, 'Mar' : 3, 'Apr' : 4, 'May' : 5, 'Jun' : 6, 
'Jul' : 7, 'Aug' : 8, 'Sep' : 9, 'Oct' : 10, 'Nov' : 11, 'Dec' : 12}

versions = {"1.0", "1.1"}

def write_log(stcode, time1, url, file, addr = None):
    time1 = time1.strftime("%d/%b/%Y:%H:%M:%S")
    method = url[0:6] 
    if(stcode == 200 and method == 'DELETE'):
        log = "127.0.0.1 - - "  + "[" + str(time1) + " +0530] " + '"' + url + '" ' + str(stcode) + " 0" + ' "-" "-"\r\n' 
    elif(stcode == 400 or stcode == 415 or stcode == 404 or stcode == 414 or stcode == 403 or stcode == 401 or stcode == 411 or stcode == 413 or stcode == 412):
        log = "127.0.0.1 - - " + "[" + str(time1) + " +0530] " + '"' + url + '" ' + str(stcode) + " 0" + ' "-" "-"\r\n' 
    elif(stcode == 200 or stcode == 201 or stcode == 204 or stcode == 304 or stcode == 202):
        log = "127.0.0.1 - - "+ "[" + str(time1) + " +0530] " + '"' + url + '" ' + str(stcode) + " " + str(os.stat(file).st_size) + ' "-" "-"\r\n' 
    elif stcode == 505:
        log = '[' + str(time1) + " +0530] : " + "[client " + str(addr) + "] HTTP Version Not Supported in Request " + url + " " + str(stcode) + '\r\n' 
    elif stcode == 501:
        log = '[' + str(time1) + " +0530] : " + "[client " + str(addr) + "] HTTP Request Not Implemented " + url + " " + str(stcode) + '\r\n'
    fp = open('access.log', 'a')
    fp.write(log)
  

def status_line(statuscode, version):
    status = statuscodes[statuscode]
    response = "HTTP/" + str(version) + " " + str(statuscode) + " " + status + ' \n'
    return response
def get_cookie():
    response = ""
    num = random.randint(0, len(cookiee) - 1)
    response += cookie + cookiee[num] + maxage
    return response
def get_headers(cookie_flag, version, stcode, time1, length = None, url = None,  extension = None, filename = None):
    response = status_line(stcode, version)
    if not cookie_flag:
        cookies = get_cookie()

    for i in Headers:
        if i != 'Content-Length' and i != 'Content-Type' and i != 'Content-Location' and i != 'Date' and i!= 'Last-Modified' and i!= 'Set-Cookie':
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
            elif not cookie_flag and i == 'Set-Cookie':
                response += cookies + "\r\n"
    
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
    print(h)
    headers = h[1]
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
def HTTP_400(version, cookie_flag):
    stcode = 400
    response_body = "<html>\n<head>\n<title>400 Bad Request</title>\n</head>\n<body>\n<p>Server could not understand the request you sent.</p>\n<hr>\n<address>Apache/2/4/18 (Ubuntu) Server at 127.0.0.1 </address>\n</body>\n</html>\n"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(cookie_flag, version, 400, date_time, l)
    return response, response_body
def HTTP_401(version, cookie_flag):
    stcode = 401
    response_body = "<html>\n<head>\n<title>401 Unauthorized</title>\n</head>\n<body>\n<p>You are not allowed to make changes.</p>\n<hr>\n<address>Apache/2/4/18 (Ubuntu) Server at 127.0.0.1 </address>\n</body>\n</html>\n"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(cookie_flag, version, 401, date_time, l)
    return response, response_body
def HTTP_403(version, cookie_flag):
    stcode = 403
    response_body = "<html>\n<head>\n<title>403 Forbidden</title>\n</head>\n<body>\n<p>You don't have permission to access this file on this server.</p>\n<hr>\n<address>Apache/2/4/18 (Ubuntu) Server at 127.0.0.1 </address>\n</body>\n</html>\n"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(cookie_flag, version, 403, date_time, l)
    return response, response_body
def HTTP_404(version, cookie_flag):
    stcode = 404
    response_body = "<html>\n<head>\n<title>404 Not Found</title>\n</head>\n<body>\n<h1>404 Not Found</h1>\n<p>The requested URL was not found on this server.</p>\n<hr>\n<address>Apache 2.4.18 (Ubuntu) Server at 127.0.0.1 </address>\n</body>\n</html>\n"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(cookie_flag, version, 404, date_time, l)
    return response, response_body
def HTTP_411(version, cookie_flag):
    stcode = 411
    response_body = "<html>\n<head>\n<title>411 Length Required</title>\n</head>\n<body>\n<hr>\n<address>Apache 2.4.18 (Ubuntu) Server at 127.0.0.1 </address>\n</body>\n</html>\n"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(cookie_flag, version, 411, date_time, l)
    return response, response_body
def HTTP_412(version, cookie_flag):
    stcode = 412
    response_body = "<html>\n<head>\n<title>412 Precondition Failed</title>\n</head>\n<body>\n<h4>The requested process can't be processed</h4>\n</body><\html>"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(cookie_flag, version, 412, date_time, l)
    return response, response_body
def HTTP_413(version, cookie_flag):
    stcode = 413
    response_body = "<html>\n<head>\n<title>413 Payload Too Large</title>\n</head>\n<body>\n<h4>The requested payload was too long for server to process.</h4>\n<hr>\n<address>Apache/2.4.18 (Ubuntu) Server at 127.0.0.1</address>\n</body>\n</html>"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(cookie_flag, version, 413, date_time, l)
    return response, response_body
def HTTP_414(version, cookie_flag):
    stcode = 414
    response_body = "<html>\n<head>\n<title>414 URI Too Long</title>\n</head>\n<body>\n<h4>The requested URI was too long for server to process.</h4>\n<hr>\n<address>Apache/2.4.18 (Ubuntu) Server at 127.0.0.1</address>\n</body>\n</html>"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(cookie_flag, version, 414, date_time, l)
    return response, response_body
def HTTP_415(version, cookie_flag):
    stcode = 415
    response_body = "<html>\n<head>\n<title>415 Unsupported Media Type</title>\n</head>\n<body>\n<h1>415 Unsupported Media Type</h1>\n<p>The server refused the request because the request entity format is not supported by this server.</p>\n<hr>\n<address>Apache/2.4.18 (Ubuntu) Server at 127.0.0.1 </address>\n</body>\n</html>\n"
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(cookie_flag, version, 415, date_time, l)
    return response, response_body
def HTTP_501(version, cookie_flag):
    stcode = 501
    response_body = "<html>\n<head>\n<title>501 Not Implemented</title>\n</head>\n<body>\n<address>Apache/2.4.18 (Ubuntu) Server at 127.0.0.1 </address>\n</body>\n</html>\n"
    l = len(response_body)
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(cookie_flag, version, 501, date_time, l)
    return response, response_body
def HTTP_505(version, cookie_flag):
    stcode = 505
    response_body = "<html>\n<head>\n<title>505 HTTP Version Not Supported</title>\n</head>\n<body>\n<h1>Server does not support the version specified.</h1>\n<address>Apache/2.4.18 (Ubuntu) Server at 127.0.0.1 </address>\n</body>\n</html>\n"
    l = len(response_body)
    l = len(response_body)
    date_time1 = datetime.datetime.now()
    date_time = givedate(date_time1)
    response = get_headers(cookie_flag, version, 505, date_time, l)
    return response, response_body
def GET(url, connectionsocket, addr, data, version, cookie_flag):
    url_len = len(url)
    #print(url)
    global stcode
    flag = 0
    if url_len > max_uri_len:
        response, response_body = HTTP_414(version, cookie_flag)
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
        ifus = 0
    extension = final_url[-1].split('.')
    extension = extension[-1]
    if(os.path.exists(file) and (os.access(file, os.W_OK) == False or os.access(file, os.R_OK) == False) and url != None): 
        stcode = 403
        response, response_body = HTTP_403(version, cookie_flag)
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
                    response = get_headers(cookie_flag, version, 304, date_time,len(response_body), url, extension, file)
                else:
                    stcode = 404
                    response, response_body = HTTP_404(version, cookie_flag)
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
                    response = get_headers(cookie_flag, version, stcode, date_time, l, url, extension, file)
                else:
                    stcode = 404
                    response, response_body = HTTP_404(version, cookie_flag)
            elif (ifus):
                stcode = 412
                response, response_body = HTTP_412(version, cookie_flag)

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
                    response = get_headers(cookie_flag, version, 200, date_time,l, url, extension, file)
                else:
                    stcode = 404
                    response, response_body = HTTP_404(version, cookie_flag)
        else:
            stcode = 415
            response, response_body = HTTP_415(version, cookie_flag)
   # print(response + response_body)
    return response, response_body

def POST(url, connectionsocket, addr, data, version, cookie_flag):
    url_len = len(url)
    global stcode
    flag = 0
    url1 = "POST " + url
    if url_len > max_uri_len:
        response, response_body = HTTP_414(version, cookie_flag)
        stcode = 414
        write_log(414, datetime.datetime.now(), url1, url)
        return response, response_body
    lines = data.split('\r\n')
    lines_to_post = lines[-1]
    file = url
    flag = 0
    extention = file.split('.')[-1]
    if (os.path.exists(file) and (os.access(file, os.W_OK) == False or os.access(file, os.R_OK) == False) and url != None):
        stcode = 403
        response, response_body = HTTP_403(version, cookie_flag)
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
                        response, response_body = HTTP_413(version, cookie_flag)
                        time1 = datetime.datetime.now().strftime("%d/%b/%Y:%H:%M:%S")
                        log = "127.0.0.1 - - " +"[" + str(time1) + " +0530] " +  '"POST' + url + '" ' + str(stcode) + " " + str(os.stat(file).st_size) + ' "-" "-"\r\n'
                    else:
                        stcode = 200
                        response_body = lines_to_post
                        date_time1 = datetime.datetime.now()
                        date_time = givedate(date_time1)
                        response = get_headers(cookie_flag, version, 200, date_time, len(response_body), url, extention, file)
                        date_time = datetime.datetime.now().strftime("%d/%b/%Y:%H:%M:%S")
                        log =  "127.0.0.1 - - " + "[" + str(date_time) + " +0530] " + '"' + url1 + ' HTTP/' + str(version)+'" ' + str(stcode) + " " + str(os.stat(file).st_size) + ' "-" "-" ' + lines_to_post + '\r\n'
                    f = open('access.log', 'a')
                    f.write(log)
                else:
                    stcode = 404
                    response, response_body = HTTP_404(version, cookie_flag)
                    write_log(stcode, datetime.datetime.now(), url1, file)
            else:
                stcode = 415
                response, response_body = HTTP_415(version, cookie_flag)
                write_log(stcode, datetime.datetime.now(), url1, file)
    return str(response), str(response_body)

def DELETE(url, connectionsocket, addr, data, version, cookie_flag):
    url_len = len(url)
    global stcode
    flag = 0
    url1 = "DELETE " + url
    auth = data.split('\r\n')
    auth_flag = [string for string in auth if "Authorization" in string]
    if url_len > max_uri_len:
        response, response_body = HTTP_414(version, cookie_flag)
        stcode = 414
        return response, response_body
    file = url
    extention = file.split('.')[-1]
    if(os.path.exists(file) and (os.access(file, os.W_OK) == False or os.access(file, os.R_OK) == False) and url != None):
        stcode = 403
        response, response_body = HTTP_403(version, cookie_flag)
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
                        print(le)
                        if le == 0:
                            stcode = 204
                            
                            date_time1 = datetime.datetime.now()
                            date_time = givedate(date_time1)
                            l = 0
                            response = get_headers(cookie_flag, version, stcode, date_time, l, url, extention, file)
                            response_body = ""
                        else:
                            stcode = 200
                            response_body = "<html>\n<body>\n<h1>File deleted.</h1>\n</body>\n</html>"
                            date_time1 = datetime.datetime.now()
                            date_time = givedate(date_time1)
                            response = get_headers(cookie_flag, version, stcode, date_time, len(response_body), url, extention, file)
                        os.remove(file)
                    else:
                        stcode = 401
                        response, response_body = HTTP_401(version, cookie_flag)
                else:
                    if flag == 1:
                        f = open(file, 'rb')
                        text = f.read()
                    else:
                        f = open(file, 'r')
                        text = f.read()
                    le = len(text)
                    print(le)
                    if le == 0:
                        
                        stcode = 204
                        date_time1 = datetime.datetime.now()
                        date_time = givedate(date_time1)
                        l = 0
                        response = get_headers(cookie_flag, version, stcode, date_time, l, url, extention, file)
                        response_body = ""
                    else:
                        stcode = 200
                        response_body = "<html>\n<body>\n<h1>File deleted.</h1>\n</body>\n</html>"
                        date_time1 = datetime.datetime.now()
                        date_time = givedate(date_time1)
                        response = get_headers(cookie_flag, version, stcode, date_time, len(response_body), url, extention, file)
                    os.remove(file)

            else:
                stcode = 404
                response, response_body = HTTP_404(version, cookie_flag)
        else:
            stcode = 415
            response, response_body = HTTP_415(version, cookie_flag)
    return str(response), str(response_body)

def PUT(url, connectionsocket, addr, data, version, cookie_flag):
    url_len = len(url)
    global stcode
    flag = 0 
    if url_len > max_uri_len:
        response, response_body = HTTP_414(version)
        stcode = 414
        return response, response_body
    data = data.split('\r\n')
    lines = data[-1]
    file = url
    url1 = "PUT " + url
    cont_len = [string for string in data if "Content-Length" in string]
    auth = [string for string in data if "Authorization" in string]
    extention = file.split('.')[-1]
    if (os.path.exists(file) and (os.access(file, os.W_OK) == False or os.access(file, os.R_OK) == False) and url != None):
        stcode = 403
        response, response_body = HTTP_403(version, cookie_flag)    
    else:
        if extention in extentions:
            if cont_len:
                if len(lines) < max_payload:
                    if os.path.exists(file):
                        if auth:
                            print("in auth")
                            if user_auth(auth):
                                f = open(file, "w")
                                f.write(lines)
                                stcode = 200
                                response_body = lines
                                date_time1 = datetime.datetime.now()
                                date_time = givedate(date_time1)
                                response = get_headers(cookie_flag, version, stcode, date_time, len(lines), url, extention, file)
                        
                            else:
                                stcode = 401
                                response, response_body = HTTP_401(version, cookie_flag)
                        else:
                            f = open(file, 'w')
                            f.write(lines)
                            stcode = 200
                            response_body = lines
                            date_time1 = datetime.datetime.now()
                            date_time = givedate(date_time1)
                            response = get_headers(cookie_flag, version, stcode, date_time, len(lines), url, extention, file)
                    else:
                        f = open(file, 'x')
                        f = open(file, 'w')
                        f.write(lines)
                        stcode= 201
                        response_body = lines
                        date_time1 = datetime.datetime.now()
                        date_time = givedate(date_time1)
                        response = get_headers(cookie_flag, version, stcode, date_time, len(lines), url, extention, file)
                        
                else:
                    stcode = 413
                    response, response_body = HTTP_413(version, cookie_flag)

            else:
                stcode = 411
                response, response_body = HTTP_411(version, cookie_flag)
        else:
            stcode = 415
            response, response_body = HTTP_415(version, cookie_flag)  
    if stcode == 411 or stcode == 413 or stcode == 403:
        write_log(stcode, datetime.datetime.now(), url1, file)
    else:
        time1 = datetime.datetime.now()
        time1 = time1.strftime("%d/%b/%Y:%H:%M:%S")
        log = "127.0.0.1 - - " +"[" + str(time1) + " +0530] "  +  '"' + url1 + " HTTP/" + str(version) + '" ' + str(stcode) + " " + str(len(lines)) + ' "-" "-"\r\n'
        f = open('access.log', 'a')
        f.write(log)
    return str(response), str(response_body)

def HEAD(url, connectionsocket, addr, data, version, cookie_flag):
    url_len = len(url)
    global stcode 
    flag = 0
    if url_len > max_uri_len:
        response, response_body = HTTP_414(version, cookie_flag)
        stcode = 414
        return response
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
        response, response_body = HTTP_403(version, cookie_flag) 
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
                    response = get_headers(cookie_flag, version, 304, date_time, l, url, extention, file)
                elif ifus == 0:
                    stcode = 412
                    response, response_body = HTTP_412(version, cookie_flag)
                else:
                    stcode = 200
                response = get_headers(cookie_flag, version, 200, date_time,l, url, extention, file)
            else:
                stcode = 404
                response, response_body = HTTP_404(version, cookie_flag)
    return str(response)
def HTTPRequest(request):
    version = '1.1'
    request = request.split('\r\n')
    words = request[0].split(' ')
    method = words[0]
    url = words[1]
    print(method, url)
    if len(words) > 2:
        version = words[2].split('/')[-1]
    return version, method, url
def call_methods(connectionsocket, addr, data):
    global stcode
    global response
    global response_body 
    data = data.decode()
    fp = data.split('\r\n')
    cookie_flag = [string for string in fp if "Cookie" in string]
    time1 = datetime.datetime.now()
    version, method, url = HTTPRequest(data)
    if version not in versions:
        stcode = 505
        response, response_body = HTTP_505(version, cookie_flag)
        res = str(response) + str(response_body)
        connectionsocket.sendall(res.encode())
        connectionsocket.close()
        write_log(stcode, datetime.datetime.now(), fp[0], url, addr)
    elif method == 'GET':
        response, response_body = GET(url, connectionsocket, addr, data, version, cookie_flag)
        res = str(response) + str(response_body)
        connectionsocket.send(res.encode())
        connectionsocket.close()
        write_log(stcode, time1, fp[0], url)
    elif method == 'POST':
        response, response_body = POST(url, connectionsocket, addr, data, version, cookie_flag)
        res = str(response) + str(response_body)
        connectionsocket.send(res.encode())
        connectionsocket.close()
    elif method == 'DELETE':
        response, response_body = DELETE(url, connectionsocket, addr, data, version, cookie_flag)
        res = str(response) + str(response_body)
        connectionsocket.send(res.encode())
        connectionsocket.close()
        write_log(stcode, datetime.datetime.now(), fp[0], url)
    elif method == 'PUT':
        response, response_body = PUT(url, connectionsocket, addr, data, version, cookie_flag)
        res = str(response) + str(response_body)
        connectionsocket.send(res.encode())
        connectionsocket.close()
    elif method == 'HEAD':
        response = HEAD(url, connectionsocket, addr, data, version, cookie_flag)
        connectionsocket.send(response.encode())
        connectionsocket.close()
        write_log(stcode, datetime.datetime.now(), fp[0], url) 
    else:
        stcode = 501
        response, response_body = HTTP_501(version, cookie_flag)
        connectionsocket.sendall((response+response_body).encode())
        connectionsocket.close()
        write_log(stcode, datetime.datetime.now(), fp[0], url, addr)

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
            serversocket.listen(max_connection)
            print("Restarted...")
serversocket = socket(AF_INET, SOCK_STREAM)
serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
servername = '127.0.0.1'
serverport = int(sys.argv[1])
host = serversocket.getsockname()
serversocket.bind(('', serverport))
serversocket.listen(max_connection)
Thread1 = Thread(target=start_restart_stop, args=(serversocket, serverport, host))
Thread1.start()
connections = 0
while True:
    connectionsocket, addr = serversocket.accept()
    if connections < max_connection:
        print("Connected By :", addr)
        connections += 1
        data = (connectionsocket.recv(8192))
        th = Thread(target=call_methods, args=(connectionsocket, addr, data, ))
        th.start()
        connections -= 1
        
    else:
        stcode = 503
        print("Maximum Number of Connections Reached!")
        log = "Server has reached maximum number of connections!\r\n"
        f = open('access.log', 'a')
        f.write(log)

  