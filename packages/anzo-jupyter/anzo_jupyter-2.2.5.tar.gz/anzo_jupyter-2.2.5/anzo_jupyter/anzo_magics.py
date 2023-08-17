from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic)
from IPython.display import display

import pandas as pd
from .anzo_jupyter import JupyterClient

# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

@magics_class
class AnzoMagics(Magics):
    """ A class with magics for interacting with an Anzo server, and
    more specifically, with an Anzo graphmart.
    """

    # Initialized other class variables to empty strings
    jupyter_client: JupyterClient = JupyterClient()

    @line_magic('print_anzo_info')
    def print_anzo_info(self, line: str) -> None:
        """ Prints information about the current configuration
        """
        self.jupyter_client.print_config()

    @line_magic('anzo_server')
    def set_anzo_server(self, line: str) -> None:
        """Sets the Anzo URL
        Args:
            line: The Anzo URL without http or https prepended.
                For example, "localhost" or "anzo-server.com" are good values.
        """
        self.jupyter_client.anzo_server = line.strip()
        self.jupyter_client.set_anzo_client()

    @line_magic('anzo_port')
    def set_anzo_port(self, line: str) -> None:
        """ Sets the anzo port

        Args:
            line: A string with Anzo port, often either 443 or 8443.
        """
        self.jupyter_client.anzo_port = line.strip()
        self.jupyter_client.set_anzo_client()

    @line_magic('auth_token')
    def set_auth_token(self, line: str) -> None:
        """ Sets the anzo auth token, bypasses user,password authentication

        Args:
            line: COOKIE-KEY=COOKIE-VALUE
        """
        self.jupyter_client.auth_token = line.strip()
        self.jupyter_client.set_anzo_client()

    """ Sets the anzo server, port, username, user password based on provided configuration file.

    Args:
        line: /path/to/config.json
    """
    @line_magic('anzo_config')
    def set_anzo_config(self, line: str) -> None:
        self.jupyter_client.read_config(line)
        self.jupyter_client.set_anzo_client()

    @line_magic('anzo_auth')
    def set_anzo_auth(self, line: str) -> None:
        """Setup Anzo user authentication

        Args:
            line: A string containining information about the Anzo user in
                the form of {username}/{password}.
        """
        self.jupyter_client.set_anzo_auth(line)

    @line_magic('anzo_auth_token')
    def set_anzo_auth_token(self, line: str) -> None:
        self.jupyter_client.set_anzo_auth_token(line)

    @line_magic('disable_pandas_truncate')
    def disable_pandas_truncate(self, line: str) -> None:
        self.jupyter_client.disable_pandas_truncate()

    @line_magic('disable_ssl_warning')
    def disable_ssl_warning(self, line: str) -> None:
        self.jupyter_client.disable_ssl_warning()

    @line_magic('graphmart')
    def set_graphmart(self, line: str) -> None:
        """
        Sets the Graphmart URI
        """
        self.jupyter_client.set_graphmart(line)

    @line_magic('prefix')
    def add_prefix(self, line: str) -> None:
        """
        Add a prefix to prepend to each query
        """
        self.jupyter_client.add_prefix(line)

    @line_magic('clear_prefixes')
    def clear_prefixes(self, line: str) -> None:
        """
        Clear all prefixes to prepend to each query
        """
        self.jupyter_client.clear_prefixes()

    @line_magic('list_prefixes')
    def list_prefixes(self, line: str) -> None:
        """
        List all prefixes to prepend to each query
        """
        return self.jupyter_client.list_prefixes()

    @line_magic('layer')
    def select_layer(self, line: str) -> None:
        """
        Limit query to selected layer(s) graphs, call magic multiple times to add multiple graphs.
        """
        self.jupyter_client.select_layer(line)

    @line_magic('list_layers')
    def list_layers(self, line: str) -> None:
        """
        List actively selected layers to query from.
        """
        return self.jupyter_client.list_layers()

    @line_magic('clear_layers')
    def clear_layers(self, line: str) -> None:
        """
        Clear actively selected layers to query from.
        """
        self.jupyter_client.clear_layers()

    @line_magic('get_graphmarts')
    def get_graphmarts(self, line: str) -> None:
        """
        Retrieve online graphmarts from selected SPARQL endpoint.

        """
        return self.jupyter_client.get_graphmarts()

    @line_magic('get_layers')
    def get_layers(self, line: str) -> None:
        """
        Retrieve layers from currently selected graphmart.

        """
        return self.jupyter_client.get_layers()

    @line_magic('limit')
    def limit(self, line: str) -> None:
        """
        Enable or disable limit check

        """
        self.jupyter_client.set_limit(line)

    @cell_magic('sparql')
    def sparql(self, line: str, cell: str) -> pd.DataFrame:
        """
        Execute a SPARQL query against the pre-configured Anzo and Graphmart

            Args:
                line: Not used
                cell: A SPARQL query as a string
        """
        return self.jupyter_client.query(cell)

    @cell_magic('sparql_journal')
    def sparql_journal(self, line: str, cell: str) -> pd.DataFrame:
        """
        Execute a SPARQL query against the Anzo system journal

            Args:
                line: Not used
                cell: A SPARQL query as a string
        """
        return self.jupyter_client.query_journal(cell)

    @cell_magic('sparql_system_tables')
    def sparql_system_tables(self, line: str, cell: str) -> pd.DataFrame:
        """
        Execute a SPARQL query against the Anzo system tables

            Args:
                line: Not used
                cell: A SPARQL query as a string
        """
        return self.jupyter_client.query_system_tables(cell)

    @line_magic('result')
    def last_result(self, line: str):
        return self.jupyter_client.return_results(line)

    @line_magic('list_types')
    def list_types(self, line: str) -> pd.DataFrame:
        """ List the types (URIs and class labels) and their respective instance counts in the graphmart

        """
        return self.jupyter_client.list_types()

    @line_magic('list_properties')
    def list_properties(self, line: str) -> pd.DataFrame:
        """ List the properties (and some associated details) populated on instances of the given class

        Args:
            line: the class URI whose properties are to be listed
        """
        return self.jupyter_client.list_properties(line)

    @line_magic('find')
    def find(self, line):
        """ Find statements matching the provided subject, predicate, and object (URI or literal).
        Currently only string literals are supported.
        Multiple values can be provided for any statement component.

        Args:
            line: the values to match on, using the following syntax:
                -sub [subject URI] -pred [predicate URI] -uri [object URI] -lit [object string literal]
        """
        # TODO support non-string literals
        return self.jupyter_client.find_statements(line)

    def reset(self) -> None:
        """
        Reset the config state to a totally "blank slate." No configurations set, not even those provided in a config file.
        """
        self.jupyter_client = JupyterClient()
        self.set_anzo_server("")
        self.set_anzo_port("")
        self.set_anzo_auth("")
        self.set_anzo_auth_token("")
        self.set_graphmart("")
        self.clear_layers("")
        self.clear_prefixes("")
