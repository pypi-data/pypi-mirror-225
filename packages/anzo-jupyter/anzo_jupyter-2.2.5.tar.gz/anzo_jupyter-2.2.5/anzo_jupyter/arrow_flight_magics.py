import pandas as pd
import warnings
from IPython.core.magic import (Magics, magics_class, line_magic, needs_local_scope)
from .anzo_jupyter_util import import_optional_dependency

# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

@magics_class
class FlightMagics(Magics):
    """ A class with magics for interacting with an Arrow Flight server,
    specifically for use with Anzo and AnzoGraph.

    Attributes:
        flight_server: The hostname of the Arrow Fligt server that should be connected to
        flight_port: The port of the Arrow Flight server that should be connected to
        flight_root_certs: The paths to TLS root certs to be used for TLS connections to the specified Arrow Flight server
    """

    flight_server: str = ""
    flight_port: str = ""
    flight_root_certs: str = ""

    pyarrow = None #used to hold optional import
    pyarrow_flight = None #used to hold optional import
    
    def get_flight_client(self):
        """
        Instantiates and returns Arrow Flight client to connect to the 
        configured Arrow Flight server.
        """
        self.check_pyarrow_imports()
        
        if not self.flight_server:
            raise ValueError("Flight server has not been set")

        if not self.flight_port:
            raise ValueError("Flight port has not been set")

        if not self.flight_root_certs:
            return self.pyarrow_flight.FlightClient(f"grpc+tcp://{self.flight_server}:{self.flight_port}")
        else:
            connection_args = {}
            with open(args[2], "rb") as root_certs:
                connection_args["tls_root_certs"] = self.flight_root_certs.read()
            return self.flight.FlightClient(f"grpc+tls://{self.flight_server}:{self.flight_port}", **connection_args)
            
    @line_magic('print_flight_server_info')
    def print_flight_server_info(self, line: str) -> None:
        """ Prints information about the current configuration
        """

        self.check_pyarrow_imports()

        if not self.flight_root_certs:
            info_string = f"Connected to Flight Server: grpc+tcp://{self.flight_server}:{self.flight_port}"
        else:
            info_string = f"Connected to Flight Server: grpc+tls://{self.flight_server}:{self.flight_port}. Using certs from: {self.flight_root_certs}"

        print(info_string)

    @line_magic('flight_server')
    def set_flight_server(self, line) -> None:
        """ Sets the flight server hostname to connect to
        """
        self.flight_server = line.strip()

    @line_magic('flight_port')
    def set_flight_port(self, line) -> None:
        """ Sets the flight server port to connect to
        """
        self.flight_port = line.strip()
    
    @line_magic('flight_root_certs')
    def set_flight_cert(self, line) -> None:
        """ Sets the directory to use for tls certificates in connecting to the flight server
        """
        self.flight_root_certs = line

    @line_magic('flight') 
    def flight(self, line) -> pd.DataFrame:
        """ Retrieve the flight with the specified flight name from the flight server
        """
        flight_cmd = line.split(' ')[0]
        return self.get_flights(flight_cmd)[0]

    def get_flights(self, flight_command) -> list:
        """ Retrieve a list of flights with the specified flight name from the flight server
        """
        flight_client = self.get_flight_client()
        descriptor = self.pyarrow.flight.FlightDescriptor.for_command(flight_command)

        info = flight_client.get_flight_info(descriptor)
        flights = list()
        for endpoint in info.endpoints:
            flight_reader = flight_client.do_get(endpoint.ticket)
            flights.append(flight_reader.read_pandas())                
        return flights
    
    @line_magic('push_flight')
    @needs_local_scope
    def push_flight(self, line, local_ns) -> None:
        """ Push the input dataframe to the flight server
        """
        line = line.split(' ')
        df = eval(line[0], local_ns)
        self.push_data(df, line[1])

    def push_data(self, df, flightname) -> None:
        print('Writing flight {} ...'.format(flightname))
        flight_client = self.get_flight_client()
        table = self.pyarrow.Table.from_pandas(df)
        writer, _ = flight_client.do_put(
            self.pyarrow_flight.FlightDescriptor.for_command(flightname), table.schema)
        writer.write(table)
        writer.close()
        print('Wrote flight {}'.format(flightname))


    def check_pyarrow_imports(self) -> None:
        if not self.pyarrow or not self.pyarrow_flight:
            self.pyarrow = import_optional_dependency('pyarrow') 
            self.pyarrow_flight = import_optional_dependency('pyarrow.flight')
