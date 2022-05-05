import os
import sys

# import time
import urllib.parse
from prometheus_client.core import Gauge, REGISTRY
from prometheus_client import MetricsHandler
from http.server import HTTPServer

# import prometheus_client as prom

from scapy.all import *


def udp_scan(target, port):
    source_port = RandShort()
    ip_scan_packet = IP(dst=target)
    udp_scan_packet = UDP(sport=source_port, dport=port)
    scan_packet = ip_scan_packet / udp_scan_packet
    scan_response = sr1(scan_packet, timeout=1, verbose=False)

    if scan_response != None:
        if scan_response.haslayer(UDP):
            return 1
        elif int(scan_response[ICMP].type) == 3 and int(scan_response[ICMP].code) == 3:
            return 0
        elif int(scan_response[ICMP].type) == 3 and int(scan_response[ICMP].code) in [
            1,
            2,
            9,
            10,
            13,
        ]:
            return 0
    else:
        return 1


REQUESTS = Gauge("udp_probe_success", "Displays whether or not the probe was a success")


class CustomCollector(MetricsHandler):
    # def __init__(self):
    #   REGISTRY.unregister(prom.PROCESS_COLLECTOR)
    #   REGISTRY.unregister(prom.PLATFORM_COLLECTOR)
    #   REGISTRY.unregister(prom.GC_COLLECTOR)
    #   pass
    def do_GET(self):
        parsed_path = urllib.parse.urlsplit(self.path)
        query = urllib.parse.parse_qs(parsed_path.query)
        if "target" in query:
            host = query["target"][0]
            list = host.split(":")
            ip = list[0]
            port = list[1]
            # print(ip, type(ip))
            # res = os.system("nc -vnzu " + ip + " " + port)
            res = udp_scan(ip, int(port))
            if res == 1:
                REQUESTS.set(int(1))
            else:
                REQUESTS.set(int(0))
            return super(CustomCollector, self).do_GET()


if __name__ == "__main__":
    PORT = sys.argv[1]
    server_address = ("", int(PORT))
    HTTPServer(server_address, CustomCollector).serve_forever()
