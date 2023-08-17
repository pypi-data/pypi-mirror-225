# Anzo-Jupyter

This is a jupyter plug-in that facilitates querying Graphmarts in Anzo.

## Setup

### Build anzo-jupyter for distribution

1. cd install
2. bash build.sh
3. Distribute `anzo-jupyter-dist.tar.gz` to the user

### Installation on a Laptop or Server

#### Prerequisites

1. Python 3.0+
2. Pyanzo 3.0
3. Jupyter 1.0+
4. PyPi/Pip

```
# Download/Unzip anzo jupyter distributable

$ tar -xvzf anzo-jupyter-dist.tar.gz

# Install anzo-jupyter

$ cd anzo-jupyter-dist

$ bash install.sh

# Check that the jupyter executable was added to the PATH variable correctly

$ jupyter

# If this errors out, run
$ export PATH=$PATH:/usr/local/bin

# Edit the configuration file located at $HOME/.anzo/jupyter_config.json, see the example notebook for more details.
# [01 - Getting Started with Anzo Jupyter](https://bitbucket.cambridgesemantics.com/projects/SEL/repos/anzo-jupyter2/notebooks/01%20-%20Getting%20Started%20with%20Anzo%20Jupyter.ipynb)

# Start Jupyter Notebook
$ cd anzo-jupyter-dist/notebooks
$ jupyter notebook
```

### Deploying Updates
- re-run build.sh with the new code to make a new distributable
- follow the same installation instructions as above

## Usage

1. start jupyter notebook
```
$ jupyter notebook
```

2. A new tab should open in your browser at localhost:8888
3. Click the notebook you want to open
4. Use magic functions to connect to your desired Anzo and Graphmart

See notebooks in `anzo_jupyter/notebooks` to get started. And see available magics below for more information on functionality you can use.

A common cell to start with is this:

```
%anzo_server anzo-solutions.com
%anzo_port 443
%anzo_auth username/password
%get_graphmarts
```

These magics will configure the connection to Anzo and return a list of graphmarts you may query from.

```
[0]: Example Graphmart 0 -- http://graphmart-to-query-from/0
[1]: Example Graphmart 1 -- http://graphmart-to-query-from/1
```
Select the graphmart by running either of the following commands in a cell

```
%graphmart http://graphmart-to-query-from/0
%graphmart 0
```

Then write your query with %%sparql at the top of the cell.

```
%%sparql

select * 
where
{
  ?s ?p ?o .
} limit 10
```

See the `notebooks` directory for some example notebooks for help getting started!

## Available Magics:

### %load_ext/%reload_ext
-- Use this magic to load this sparql extension
  - %load_ext anzo_jupyter
  - %reload_ext anzo_jupyter

### %%sparql
-- After connecting to an anzo server, create a cell with %%sparql at the first line
  - This enables writing SPARQL queries against the selected anzo server and graphmart.
  - By default, your SPARQL query must include a LIMIT to prevent accidentally retrieving too large a result set.
  - See `%limit` magic below to disable.


### %get_graphmarts 
-- Retrieve available endpoints from the configured Anzo Server.
  - Will only work if a correctly configured anzo_config.py is provided
  - If anzo_config.py is not being used, configure using %anzo_server, %anzo_port, %anzo_auth 
  - Then run %get_graphmarts AFTER configuration
  - Returns a list  of available graphmart endpoints in the format:
      [index]: "Graphmart Title" -- <graphmart-uri>
      i.e. [0]:  "my anzo graphmart"  --   <http://graphmart.com>

### %graphmart [graphmart-index-or-uri] 
-- Configure the Anzo data endpoint, providing the graphmart index or uri as a parameter. Run after %get_graphmarts
  - %graphmart http://cambridgesemantics.com/Graphmart/f7fe52fc24d84d1a8610fe293541871a
  - %graphmart 0
  
### %anzo_server [anzo-server] 
-- Define the Anzo server for the notebook to connect to. Do not include http/s in the server address.
   - %anzo_server anzo-server

### %anzo_port [port] 
-- Define the Anzo port to connect to. Often either 443 or 8443.
  - %anzo_port 443/8443
  
### %auth_token [COOKIE]=[KEY_VALUE]
-- Authenticate using cookies
  - %auth_token BAYEUX_BROWSER=my-cookie-key-value

### %anzo_auth [user]/[password]
-- Provide the credentials of the Anzo user. Optionally if the secrets manager module is included, you can specify a secret name/region
  - %anzo_auth sysadmin/anzo
  - %anzo_auth secret/SECRET_NAME/REGION_NAME

### %print_anzo_info
-- Prints the currently configured Anzo Server, Port, and User Credentials.
  
### %result [datatype]
-- Print the last result in JSON format by default, if `df` is specified, a dataframe will be returned
  
-- This will directly store the result in a global python variable "_", you may also set a variable equal to the return result
  - i.e. queryDict = %result dict
  - queryDict will now store the last query result as a dictionary.
  
-- Run a %%sparql query, then in the next cell run %result, 
  - %result dict -- return the query results as a Python dictionary.
  - %result nx -- returns a networkx multidigraph
  - %result rdf -- returns an rdflib conjunctive graph
  - %result df -- returns a pandas dataframe
  - %result graph_vis -- returns a pyvis network object that can be rendered

### %list_types
-- Runs a query that lists the types (URIs and class labels) and their respective instance counts in the graphmart

### %list_properties [class-uri]
-- Runs a query that lists the properties (and some associated details) populated on instances of the given class

### %find (-sub [sub-uri]) (-pred [pred-uri]) (-uri [object URI]) (-lit [object string literal])
--  Find statements matching the provided subject, predicate, and object (URI or literal). At least one statement component must be provided. Currently only string literals are supported for `-lit`. Multiple values can be provided for any statement component.
  - %find -sub http://someSubjectUri
  - %find -sub http://someSubjectUri -sub http://someSubjectUri2
  - %find -sub http://someSubjectUri -pred http://somePredicateUri
  - %find -uri http://someObjectUri
  - %find -lit "Some string literal property"

### %prefix [title],[uri]
-- Add a prefix to the global namespace of the sparql query, these prefixes will always be prepended to the sparql query

### %list_prefixes
-- List all prefixes in the current namespace

### %clear_prefixes
-- Clear all prefixes from the current name space

### %get_layers
-- Retrieve a list of available/online layers from the configured graphmart

### %layer [index-or-uri]
-- Select a layer using the index from get_layers or using a uri. Provide a Python index slice or comma seperated values.
  - %layer 0
  - %layer http://cambridgesemantics.com/Layer
  - %layer 0,1,2 OR %layer 0:2
  - %layer http://cambridgesemantics.com/Layer,http://cambridgesemantics.com/LayerA
  
### %clear_layers
-- Clear all layers from the current name space

### %limit ['true' or 'false']
-- Enable or disable the check for LIMIT clauses in submitted SPARQL queries (enabled by default)

### %disable_display_html
-- Disable rendering the entire Pandas dataframe as output.

### %disable_pandas_truncate
-- Prevents text truncation when displaying query results as pandas dataframe
  
### %disable_ssl_warning
-- Suppress SSL warning when querying an HTTPS endpoint



## Advanced Usage:

The following commands are used for advanced use cases to gather system information from an Anzo server.
They should be used with caution and care.

### %%sparql_journal [query string]
-- Query the Anzo system journal

### %%sparql_system_tables [query string]
-- Query the Anzo system tables



## Graph Visualizations:

To create a basic Graph visualiztion, run the magic:
```
nt = %result graph_vis
```

This returns a pyvis network object that can be rendered with nt.show(filename).
This will write an HTML file to the specified filename and render it in jupyter.

You can also open this file directly in your browser to view it outside of the context
of jupyter.

For more fine-graphed control over the rendered visualization, you can import
the GraphVisBuilder class and specify options.

```
nt = GraphVisBuilder(g, node_label_spec, edge_label_spec, width, height).build()
```

The following options are configurable:
- node_label_spec: how nodes are labeled
- edge_label_spec: how edges are labeled
- width: the width of the HTML canvas
- height: the height of the HTML canvas

For more information, see the "04 - Visualizing the Graph.ipynb" example notebook.



## Arrow Flight Magics

The following comamnds are used for interacting with an [Arrow Flight](https://arrow.apache.org/docs/format/Flight.html) server. Anzo currently offers direct integration with flight servers using the [arrow_flight_push UDX](https://docs.cambridgesemantics.com/anzograph/v2.2/userdoc/arrow-apache.htm#arrow_flight_push). For more details, see [this tutorial](https://cambridgesemantics.atlassian.net/wiki/spaces/CI/pages/1511063575/Arrow+Flight+Integration). 

### %flight_server [hostname]
-- Set the hostname for a flight server to connect to
Initialize a python flight client connected to a flight server at the provided location. 
  - %flight_server 127.0.0.1

### %flight_port [port]
-- Set the port for a flight server to connect to.
  - %flight_port 5005

### flight_root_certs [path_to_cert_files]
  Optionally, provide a path to cert files to use in connecting to a flight server, if the server requries a tls connection. Otherwise, basic tcp connections are used as a default.
  - %flight_root_certs /tmp/arrow/keys/cert0.pem /tmp/arrow/keys/cert0.key

### print_flight_server_info
  Print the information of the flight server that the kernel is currently configured to connect to
  - %print_flight_server_info

### %flight [flight-name]
-- Get the flight with the specified flight name from the flight server you have configured to connect to. This can be used to retrieve a result set that was pushed to the flight server from a query that used the arrow_flight_push UDX.
  - flight = %flight my-query-result-flight

### %flights [flight-name]
-- Same as above, except it returns a python list of dataframes, if there are multiple flights stored at the specified name and you would like to retrieve all of them.
  - flights = %flights my-query-result-flight

### %push_flight [df-variable] [flight-name]
-- Push a dataframe in your local namespace to the flight server that your flight client (see above) is connected to. See example notebook "arrow-flight-example" for an example.
  - %push_flight my_df my_new_flight
