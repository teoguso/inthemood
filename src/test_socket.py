from heuro_api import Heuro
from credentials import email, password, pipeline_id
import socket
import time

# creates socket object
s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)

host = '' # do we need socket.gethostname() ?
port = 8080
sock.bind((host, port))
sock.listen(1) # don't queue up any requests

# Loop forever, listening for requests:
while True:
    csock, caddr = sock.accept()
    print "Connection from: " + `caddr`
    req = csock.recv(1024) # get the request, 1kB max
    print req
    time.sleep(5)