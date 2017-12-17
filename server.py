from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import threading
import argparse
import re
import urllib
import json
import settings

def getHereAddress(address):
    params = urllib.urlencode({'app_id': settings.HERE_APP_ID,\
     'app_code': settings.HERE_APP_CODE,\
      'searchtext': address})
    f = urllib.urlopen("https://geocoder.cit.api.here.com/6.2/geocode.json?%s" % params)
    here = json.loads(f.read())
    if not here['Response']['View']:
        return False
    return here

def getAddress(address):
    here = getHereAddress(address)
    if here:
        here['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0].update({'status':True})
        return here['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]
    return False
 
class HTTPRequestHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    if None != re.search('/latlong/v1/getaddress/*', self.path):
      address = self.path.split('/')[-1]
      address = getAddress(address)
      if address:
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(address)
      else:
        self.send_response(400, 'Bad Request: address does not exist')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(address)
    else:
      self.send_response(403)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()
    return
 
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
  allow_reuse_address = True
 
  def shutdown(self):
    self.socket.close()
    HTTPServer.shutdown(self)
 
class SimpleHttpServer():
  def __init__(self, ip, port):
    self.server = ThreadedHTTPServer((ip,port), HTTPRequestHandler)
 
  def start(self):
    self.server_thread = threading.Thread(target=self.server.serve_forever)
    self.server_thread.daemon = True
    self.server_thread.start()
 
  def waitForThread(self):
    self.server_thread.join()
 
  def stop(self):
    self.server.shutdown()
    self.waitForThread()
 
if __name__=='__main__':
  parser = argparse.ArgumentParser(description='HTTP Server')
  parser.add_argument('port', type=int, help='Listening port for HTTP Server')
  parser.add_argument('ip', help='HTTP Server IP')
  args = parser.parse_args()
 
  server = SimpleHttpServer(args.ip, args.port)
  print 'HTTP Server Running...........'
  server.start()
  server.waitForThread()
