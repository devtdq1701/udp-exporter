import os
import sys
import time
import urllib.parse
from prometheus_client.core import Gauge, REGISTRY
from prometheus_client import MetricsHandler
from http.server import HTTPServer
import prometheus_client as prom

REQUESTS = Gauge('udp_probe_success',
        'Displays whether or not the probe was a success')

class CustomCollector(MetricsHandler):
    # def __init__(self):
    #   REGISTRY.unregister(prom.PROCESS_COLLECTOR)
    #   REGISTRY.unregister(prom.PLATFORM_COLLECTOR)
    #   REGISTRY.unregister(prom.GC_COLLECTOR)
    #   pass
    def do_GET(self):
      parsed_path = urllib.parse.urlsplit(self.path)
      query = urllib.parse.parse_qs(parsed_path.query)
      if("target" in query):
        host = query['target'][0]
        list=host.split(':')
        ip=list[0]
        port=list[1]
        res = os.system("nc -vnzu "+ip+" "+port)
        if res == 0:
          REQUESTS.set(1)
        else:
          REQUESTS.set(0)
        return super(CustomCollector, self).do_GET()

if __name__ == '__main__':
  PORT = sys.argv[1]
  server_address = ('', int(PORT))
  HTTPServer(server_address, CustomCollector).serve_forever()
  while True:
    time.sleep(15)