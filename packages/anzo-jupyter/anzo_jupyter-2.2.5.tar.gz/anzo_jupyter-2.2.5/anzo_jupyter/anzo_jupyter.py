from .anzo_managers import PrefixManager
from .anzo_managers import LayerManager
from .anzo_managers import GraphmartManager
from .anzo_queries import AnzoQueryBuilder
from .graph_vis import GraphVisBuilder
from .secrets_manager import SecretsManager

import pandas as pd
import json
import requests
import shlex
import os

from pyanzo import AnzoClient
from IPython.display import HTML
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

class JupyterClient:
    """
    Attributes:
        anzo_server: The server that Anzo is running on.
        anzo_port: The port on which Anzo is listening for HTTP traffic.
            Often 80, 443, 8080, or 8443.
        anzo_username: Username of the user with which to interact with Anzo.
        anzo_password: The password of the Anzo user
        auth_token: The cookie of the Anzo session to authenticate with.
        config_path: The default filepath for the Jupyter Client to read configurations from.
        graphmart_uri: URI of the Anzo Graphmart to interact with
        anzo_client: AnzoClient object for interacting with Anzo
        graphmart_manager: GraphmartManager object for interacting with an
            Anzo Graphmart
        layer_manager: Manages selected graphmarts layers for queries.
        last_result: Stores the most recent query results of a query
                     which can be converted to rdf, json, see PyAnzo QueryResult for more info.

    """
    # Initialized other class variables to empty strings
    # because they may be set over time
    anzo_client: AnzoClient = None
    anzo_server: str = ""
    anzo_port: str = ""
    anzo_username: str = ""
    anzo_password: str = ""
    auth_token: str = ""
    config_path: str = ""
    limit: bool = True

    prefix_manager: PrefixManager = None
    layer_manager: LayerManager = None
    graphmart_manager: GraphmartManager = None
    last_result = None

    def __init__(self):
        self.anzo_client = None
        self.prefix_manager = PrefixManager()
        self.layer_manager = LayerManager()
        self.graphmart_manager = GraphmartManager()

        try:
            self.config_path = os.environ['HOME'] + \
                "/.anzo/jupyter_config.json"
        except KeyError:
            print("HOME environment variable not set, config file will not be written!")

        if os.path.exists(self.config_path):
            self.init_config(self.config_path)
            self.set_anzo_client()

    def disable_pandas_truncate(self) -> None:
        """
        Prevent pandas from truncating text when displaying data frames.
        """
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_colwidth', None)

    def disable_ssl_warning(self) -> None:
        """
        Suppress SSL Warning
        """
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def init_config(self, config_path: str) -> None:
        if not os.path.exists(config_path):
            print("Configuration file does not exist, please configure connection to Anzo SPARQL Endpoint before writing queries.")
            with open(config_path, "w+") as config:
                settings = {
                    "anzo_server": "",
                    "anzo_port": "",
                    "anzo_username": "",
                    "anzo_password": "",
                    "graphmart": ""
                }
                try:
                    print(
                        f"Template configuration written to {config_path}, please update values.")
                    config.write(json.dumps(settings))
                except OSError as e:
                    print(
                        f"Exception: Attempted to write to {config_path}\n{e}")
        else:
            self.read_config(config_path)

    def read_config(self, config_path: str) -> None:
        try:
            if not config_path:
                config_path = self.config_path
            with open(config_path, "r") as config:
                settings = json.load(config)
                if 'anzo_server' in settings:
                    self.anzo_server = settings['anzo_server']
                if 'anzo_port' in settings:
                    self.anzo_port = settings['anzo_port']
                if 'anzo_username' in settings:
                    self.anzo_username = settings['anzo_username']
                if 'anzo_password' in settings:
                    self.anzo_password = settings['anzo_password']
                if 'graphmart' in settings:
                    self.set_graphmart(settings['graphmart'])
        except OSError as e:
            print("""\nFailed to load configuration file, set config path using %config </path/to/config.json> magic
                  or create configuration file in ~/.anzo/jupyter_config.json""")
            raise e

    def print_config(self):
        cleared_password = "xxxxxxxx" if self.anzo_password else "None"

        info_string = f"""
Anzo URL: {self.anzo_server}
Anzo Port: {self.anzo_port}
Anzo Username: {self.anzo_username}
Password: {cleared_password}
Graphmart: {self.selected_graphmart()}
"""
        print(info_string)

    def add_prefix(self, line: str) -> None:
        """
        Stores prefixes as prefix class instances within the prefix manager
        All prefixes are prepended to every query.
        """
        prefix, uri = line.split(",")
        self.prefix_manager.add(prefix, uri)

    def clear_prefixes(self) -> None:
        """
        Remove every prefix stored in the prefix manager.
        """
        self.prefix_manager.clear()

    def list_prefixes(self) -> None:
        """
        List every prefix stored in the prefix manager.
        """
        self.prefix_manager.list_all()

    def selected_graphmart(self) -> str:
        return self.graphmart_manager.selected_graphmart

    def list_layers(self) -> None:
        self.layer_manager.list_all()

    def clear_layers(self) -> None:
        self.layer_manager.clear()

    def select_layer(self, line: str) -> str:
        """
        Sets the selected layers to query from
        """
        self.layer_manager.parse_input_layers(line)

    def selected_layers(self) -> str:
        return self.layer_manager.selected_layers

    def set_graphmart(self, line: str) -> None:
        """
        Sets the Selected Graphmart of graphmart manager
        """
        self.layer_manager.clear()
        self.graphmart_manager.set_graphmart(line.strip())

    def get_graphmarts(self) -> None:
        """
        Queries the Anzo system tables storing the all graphmart uri and titles within graphmart manager
        """
        self.set_anzo_client()

        query_result = self.anzo_client.query_system_tables(
            query_string=AnzoQueryBuilder.activeGraphmarts()).as_table_results().result_dicts

        self.graphmart_manager.parse_graphmarts(query_result)

    def get_layers(self) -> None:
        """
        Given a selected graphmart, anzo endpoint
        Queries the Anzo journal storing the all graphmart uri and titles within graphmart manager
        """
        self.raise_if_missing_configuration()

        selected_graphmart = self.selected_graphmart()

        query_result = self.anzo_client.query_journal(
            query_string=AnzoQueryBuilder.activeLayers(selected_graphmart)).as_table_results().result_dicts

        self.layer_manager.parse_layers(query_result)

    def construct_query(self, query_results) -> pd.DataFrame:
        """
        Converts the results of a construct query into a readable dataframe object.
        Additionally stores results as a python dictionary and rdflib conjunctive graph in self.last_result
        """
        if not len(query_results.json_string):
            return pd.DataFrame()

        record_dicts = query_results.as_quad_store().as_record_dictionaries()
        return pd.DataFrame.from_records(record_dicts)

    def query(self, query_string: str = '', validate_limit: bool = True) -> pd.DataFrame:
        self.raise_if_missing_configuration()

        if not self.anzo_client:
            self.set_anzo_client()

        graphmart_uri = self.selected_graphmart()

        query = self.prefix_manager.include_prefixes(query_string)
        if validate_limit:
            self.validate_limit(query)

        data_layers = self.selected_layers()

        query_results = self.anzo_client.query_graphmart(
            graphmart=graphmart_uri, query_string=query, data_layers=data_layers
        )

        self.last_result = query_results

        if "construct" in query_string.lower():
            return self.construct_query(query_results)

        return pd.DataFrame(
            self.result_dict()
        )

    def query_journal(self, query_string: str = '') -> pd.DataFrame:
        self.raise_if_missing_configuration(False)

        if not self.anzo_client:
            self.set_anzo_client()

        query = self.prefix_manager.include_prefixes(query_string)
        self.validate_limit(query)

        query_results = self.anzo_client.query_journal(query_string=query)

        self.last_result = query_results

        try:
            return self.construct_query(query_results)
        except RuntimeError as e1:
            try:
                return pd.DataFrame(self.result_dict())
            except Exception as e2:
                raise RuntimeError("Unable to parse query reuslt")

    def query_system_tables(self, query_string: str = '') -> pd.DataFrame:
        self.raise_if_missing_configuration(False)

        if not self.anzo_client:
            self.set_anzo_client()

        query = self.prefix_manager.include_prefixes(query_string)
        self.validate_limit(query)

        query_results = self.anzo_client.query_system_tables(
            query_string=query)

        self.last_result = query_results

        try:
            return self.construct_query(query_results)
        except RuntimeError as e1:
            try:
                return pd.DataFrame(self.result_dict())
            except Exception as e2:
                raise RuntimeError("Unable to parse query reuslt")

    def list_types(self) -> pd.DataFrame:
        return self.query(AnzoQueryBuilder.list_instances(), False)

    def list_properties(self, line: str) -> pd.DataFrame:
        class_uri = line.strip()
        if not class_uri:
            raise ValueError(
                "Class URI must be specified to retrieve property counts.")
        return self.query(AnzoQueryBuilder.list_properties(class_uri), False)

    def find_statements(self, line: str) -> pd.DataFrame:
        # shell-like split to capture quoted literal values
        split = shlex.split(line)
        subs = []
        preds = []
        lits = []
        uris = []
        try:
            sub_indices = [i for i, x in enumerate(split) if x == "-sub"]
            subs = [split[x + 1] for x in sub_indices]
        except ValueError:
            pass
        try:
            pred_indices = [i for i, x in enumerate(split) if x == "-pred"]
            preds = [split[x + 1] for x in pred_indices]
        except ValueError:
            pass
        try:
            lit_indices = [i for i, x in enumerate(split) if x == "-lit"]
            # any quotes captured within a quoted literal must be escaped in the query
            lits = [split[x + 1].replace('"', "\\\"") for x in lit_indices]
        except ValueError:
            pass
        try:
            uri_indices = [i for i, x in enumerate(split) if x == "-uri"]
            uris = [split[x + 1] for x in uri_indices]
        except ValueError:
            pass

        if not subs and not preds and not lits and not uris:
            raise ValueError(
                "A subject, predicate, literal or URI must be provided")

        subs_string = ""
        if subs:
            subs_string = to_values_clause("s", [urify(x) for x in subs])

        preds_string = ""
        if preds:
            preds_string = to_values_clause("p", [urify(x) for x in preds])

        objs_string = ""
        objs = [quote(x) for x in lits] + [urify(x) for x in uris]
        if objs:
            objs_string = to_values_clause("o", objs)

        res = self.query(AnzoQueryBuilder.find_statements(
            subs_string, preds_string, objs_string), False)
        if (res.empty):
            print("No results found")
        return res

    def return_results(self, line: str):
        """
        Return the last result and convert based on provided parameter

            Args:
                line: By default returns a json_string
                        "rdf", returns an RDF lib conjunctive graph
                        "nx", returns a Networkx multidigraph
                        "dict", returns Python records dictionary
                        "df", returns a Pandas data frame
        """
        output_type = line.strip().lower()
        if output_type == "rdf":
            try:
                return self.result_rdf()
            except:
                raise ValueError(
                    "Expected CONSTRUCT query prior to outputting rdf graph.")

        if output_type == "nx":
            try:
                return self.result_nx()
            except:
                raise ValueError(
                    "Expected CONSTRUCT query prior to conversion to nx graph.")

        if output_type == "dict":
            try:
                return self.result_dict()
            except:
                raise ValueError(
                    "Expected SELECT/CONSTRUCT query prior to outputting results.")

        if output_type == "graph_vis":
            g = self.return_results("nx")  # TODO: remove hardcode
            return GraphVisBuilder(g).build()
        if output_type == "df":
            try:
                return self.result_df()
            except:
                raise ValueError(
                    "Expected SELECT/CONSTRUCT query prior to outputting results.")

        return self.result_json()

    def result_dict(self) -> dict:
        if self.last_result != None:
            return self.last_result.as_table_results().as_record_dictionaries()
        raise ValueError(
            "Last result not defined, please run a CONSTRUCT or SELECT query then try again.")

    def result_json(self) -> str:
        if self.last_result != None:
            return self.last_result.json_string
        raise ValueError(
            "Last result not defined, please run a CONSTRUCT or SELECT query then try again.")

    def result_rdf(self):
        if self.last_result != None:
            return self.last_result.as_quad_store().as_rdflib_graph()
        raise ValueError(
            "Last result or quad store not defined, please run a CONSTRUCT query then try again.")

    def result_nx(self):
        if self.last_result != None:
            return rdflib_to_networkx_multidigraph(self.last_result.as_quad_store().as_rdflib_graph())
        raise ValueError(
            "Last result or quad store not defined, please run a CONSTRUCT query then try again.")

    def result_df(self) -> pd.DataFrame:
        if self.last_result != None:
            return pd.DataFrame(self.result_dict())
        raise ValueError(
            "Last result or quad store not defined, please run a CONSTRUCT or SELECT query then try again.")

    def raise_if_invalid_authentication(self) -> None:
        """
        Raises a value error if username, password, AND auth_token is set

        Only username/password OR auth_token should be used for authentication

        This will often be called before an anzo_client is initialized
        """
        if self.anzo_username and self.anzo_password and self.auth_token:
            raise ValueError(
                "Only one of username and password or auth_token may be specified")

    def raise_if_missing_configuration(self, check_graphmart=True) -> None:
        """
        Raises a value error if an important piece of configuration is missing

        This will often be called before an operation is executed
        """
        if not self.anzo_server:
            raise ValueError("Anzo server has not been set")

        if not self.anzo_port:
            raise ValueError("Anzo port has not been set")

        if self.auth_token:
            if self.anzo_username:
                raise ValueError("Anzo username and token have been set")

            if self.anzo_password:
                raise ValueError("Anzo password and token have been set")

        else:
            if not self.anzo_username:
                raise ValueError("Anzo username has not been set")

            if not self.anzo_password:
                raise ValueError("Anzo password has not been set")

        if check_graphmart and not self.selected_graphmart():
            raise ValueError("Graphmart has not been set")

    def set_anzo_auth(self, line: str) -> None:
        """
        Setup Anzo user authentication

        Args:
            line: A string containining information about the Anzo user in
                the form of {username}/{password}.
                if the form 'secret/{secret_name}/{region_name}' is provided then
                attempt to read from an existing AWS secrets manager.'
        """
        parsed_input = line.split("/")

        if parsed_input[0].lower() == 'secret':
            _, secret_name, region_name = parsed_input
            login = SecretsManager.parse_login_info(secret_name, region_name)
            self.anzo_username, self.anzo_password = login
            self.set_anzo_client()
            return

        # TODO: not good yet - not good error handling & bad assumptions
        try:
            self.anzo_username, self.anzo_password = parsed_input
        except:
            self.anzo_username, self.anzo_password = None, None

        self.set_anzo_client()

    def set_anzo_auth_token(self, line: str) -> None:
        """
        Setup Anzo user authentication

        Args:
            line: A string containining information about the Anzo user in
                the form of {username}/{password}.
        """
        self.auth_token = line.strip()
        self.set_anzo_client()

    def set_anzo_client(self) -> None:
        """
        Initialize the anzo client

        This will called after each of the following parameters are provided:
            anzo_server, anzo_port, anzo_username, anzo_password

        """
        if self.anzo_server and self.anzo_port and ((self.anzo_username and self.anzo_password) or self.auth_token):
            self.anzo_client = AnzoClient(
                domain=self.anzo_server, port=self.anzo_port,
                username=self.anzo_username, password=self.anzo_password, auth_token=self.auth_token
            )

    def set_limit(self, line: str) -> None:
        parsed = line.strip().lower()
        if parsed == "false":
            self.limit = False
        elif parsed == "true":
            self.limit = True
        else:
            print(
                "Please provide 'true' or 'false' string to enable or disable limit checking.")

    def validate_limit(self, query: str) -> None:
        if self.limit and "limit" not in query.lower():
            raise ValueError(
                'You have to include a limit!\n Please append limit # to your query.')


def to_values_clause(var: str, inputs: list):
    return "VALUES (?{}) {{ ({}) }}".format(var, ")(".join(inputs))


def urify(input: str) -> str:
    return "<{}>".format(input)


def quote(input: str) -> str:
    return "\"{}\"".format(input)
