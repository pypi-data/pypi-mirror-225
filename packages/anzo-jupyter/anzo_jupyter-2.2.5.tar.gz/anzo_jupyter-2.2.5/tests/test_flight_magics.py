import unittest
import pandas as pd
import urllib3
import threading

from .sample_flight_server import FlightServer
from anzo_jupyter import FlightMagics

class TestFlightMagics(unittest.TestCase):
    push_df = pd.DataFrame(
            ["Boston", "Cambridge", "Medford", "Somerville", "Watertown"],
            columns=["city"]
        )
    
    flight_name = "test-flight"

    def setUp(self) -> None:
        host = "127.0.0.1"
        port = "5005"
        scheme = "grpc+tcp"
        tls_certificates = [] #TODO: test tls connections
        self.fm = FlightMagics()
        self.fm.set_flight_server(host)
        self.fm.set_flight_port(port)
        if len(tls_certificates) > 0:
            self.fm.set_flight_cert(tls_certificates)


        location = "{}://{}:{}".format(scheme, host, port)
        flight_server = FlightServer(host, location,
                          tls_certificates=tls_certificates)
        
        #somehow, things work without the below block.
        #i guess we don't need to explicitly call .serve()
        
        # with server as flight_server:
        #     thread = threading.Thread(target=server.serve)
        #     thread.daemon = True
        #     thread.start()
        #     print("Serving on", location)
        
    #it'd be cleaner to separate these into separate tests,
    #but each one is needed for the other at this point...
    def test_push_pull_flight(self) -> None:
        self.fm.push_flight(f"self.push_df {self.flight_name}", locals())
        pulled_df = self.fm.flight(self.flight_name)
        pd.testing.assert_frame_equal(self.push_df, pulled_df)
