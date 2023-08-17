from collections import defaultdict
from urllib.parse import urlparse
import networkx as nx
import os
import rdflib
import tabulate  # TODO: make optional
import pyvis  # TODO: make optional

# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

class GraphVisBuilder:
    def __init__(self, nx_graph: nx.Graph, node_label_spec=None, edge_label_spec=None, width=None, height=None):
        """
        Args:
            nx_graph: Networkx graph created from a construct query
            node_label_spec: Specification how the label of nodes should
                be rendered.  The options are:
                - localname: localname of the URI
                - localname_title (default): the localname of the URI
                    titleized, so "urn://Person/alex_l" becomes "Alex L"
                - uri: the uri of the property
                - off: which wont display any label)
                - URI of a property: if an instance has the property, the associated
                    value is displayed, otherwise, no label is displayed
            edge_label_spec: Specification how the label of edges should
                be rendered. The options are:
                - localname: localname of the URI
                - localname_title (default): the localname of the URI
                    titleized, so "p_has_friend" becomes "Has Friend"
                - uri: the uri of the property
                - off: which wont display any label)
            width: Width of the html canvas, formatted "<number>px".
                Default is "1000px".
            height: Height of the html canvas, formatted "<number>px".
                Default is "1000px".
        """
        self.nx_graph = nx_graph

        # Don't normalize the case here because we might be
        # matching URIs if a property was provided
        self.node_label_spec = node_label_spec or "localname_title"
        self.edge_label_spec = edge_label_spec or "localname_title"

        self.width = width or "1000px"
        self.width = self.width.lower()

        self.height = height or "1000px"
        self.height = self.height.lower()

    def flatten_list(self, l):
        return [item for subl in l for item in subl]

    def localname(self, s: str) -> str:
        """
        Cleans a string into a good label
        """

        s = str(s)
        ret = urlparse(s).fragment
        if not ret:
            ret = os.path.basename(urlparse(s).path)
        if not ret:
            ret = s
        return ret

    def find_obj(self, prop: str, this_node_literals) -> str:
        for p, o in this_node_literals:
            if prop == p:
                return o
        return ""

    def make_node_label(self, node: str, this_node_literals) -> str:
        node_label = ""
        if self.node_label_spec.lower() == "localname":
            node_label = self.localname(node)

        elif self.node_label_spec.lower() == "localname_title":
            node_label = self.localname(node)
            node_label = node_label.replace("_", " ").replace("-", " ").title()

        elif self.node_label_spec.lower() == "uri":
            node_label = str(node)

        elif self.node_label_spec.lower() == "off":

            # The empty string and none both evaluate to the name of
            # the node. To force it to be "off", use a string with
            # a space
            node_label = " "
        else:
            prop = rdflib.term.URIRef(self.node_label_spec)
            node_label = self.find_obj(prop, this_node_literals)

            node_label = node_label or " "
        return node_label

    def make_edge_label(self, edge_uri: str) -> str:
        edge_label = ""
        if self.edge_label_spec.lower() == "localname":
            edge_label = self.localname(edge_uri)
        elif self.edge_label_spec.lower() == "localname_title":
            edge_label = self.localname(edge_uri)
            edge_label = edge_label.replace("_", " ").replace("-", " ").title()

            # remove the leading "P " which Anzo often adds to properties
            if edge_label.startswith("P ") and len(edge_label) > 2:
                edge_label = edge_label[2:]

        elif self.edge_label_spec.lower() == "uri":
            edge_label = str(edge_uri)
        elif self.edge_label_spec.lower() == "off":
            edge_label = ""
        else:
            raise ValueError(
                f"Unexpected edge label specification: {self.edge_label_spec}"
            )

        return edge_label

    def build(self):
        """
        Builds a networkx digraph that can be used for visualization in pyvis or other tools.
        - A node will be rendered for each instance, where an instance is defined as
          (a) not a literal and (b) not a the object of a type statement
        - This works best if each instance has a single type
        - If an instance has multiple types, then an arbitrary type is chosen to inform
          the group (color) of the node
        - If you render the resulting graph with pyvis, on mouse-over you'll see the types of
          the instance and the datatype properties on the instance
        Networkx tips: build data-structures/lists independent of the
        graph, and loop over that. Then you can modify without issue
        Best place to start with networkx docs:
        https://networkx.org/documentation/stable/reference/classes/digraph.html
        """

        g = self.nx_graph

        # 1. Loop over the graph in order to populate
        # the following data-structures
        node_types = defaultdict(list)     # node -> List[type]
        node_literals = defaultdict(list)  # node -> List[(predicate, value)]
        edge_labels = dict()               # edge -> label

        for u, nbrsdict in g.adjacency():
            for v, eattr in nbrsdict.items():
                keys = list(eattr.keys())

                if len(keys) > 1:
                    # TODO: address this condition
                    pass

                assert len(keys) > 0
                key = keys[0]

                if key == rdflib.namespace.RDF.type:
                    node_types[u].append(v)
                elif isinstance(v, rdflib.term.Literal):
                    node_literals[u].append((key, v))
                else:
                    edge_labels[(u, v)] = self.make_edge_label(keys[0])

        # 2. Remove the type nodes and the literal nodes from the graph
        all_types = set(self.flatten_list(node_types.values()))

        for n in all_types:
            g.remove_node(n)

        for n in list(g.nodes()):
            if isinstance(n, rdflib.term.Literal):
                g.remove_node(n)

        # 3. Add the edge labels to the graph
        for (u, v), label in edge_labels.items():
            # I found that the best way to do this was just to replace the edge

            try:
                g.remove_edge(u, v)
            except nx.NetworkXError as nxe:
                #print("TODO: ignoring networkx error")
                pass

            g.add_edge(u, v, label=label)

        # 4. Add node attributes
        # 4a. Define an integer value to each type.
        # This will be used for the groups
        # Reserve group 0 for nodes with no type
        type_to_group = {
            a_type: i + 1 for i, a_type in enumerate(all_types)
        }

        # 4b. Loop over the nodes and set the node attributes
        node_attrs = dict()
        for node in g.nodes():

            # Sort the types for deterministic behavior
            types = sorted(node_types[node])

            # Determine a group for the node based on the type.
            # This group is ultimately used for coloring the node
            if types:
                # If there's more than one type, use the first type
                group = type_to_group[types[0]]
            else:
                group = 0

            # Put the types into a list for serializing later
            type_info_list = []
            for t in types:
                type_info_list.append(["type:", str(t)])

            # Sort the type information alphabetically
            type_info_list = sorted(type_info_list)

            # Collect info about the properties into a dictionary
            prop_info_dict = defaultdict(list)

            for pred, literal in node_literals[node]:
                local_pred = self.localname(pred)
                prop_info_dict[local_pred].append(str(literal))

            # Flatten prop_info_dict of lists into a single list for
            # serialization
            prop_info_list = []
            for key, vals in prop_info_dict.items():
                for val in vals:
                    prop_info_list.append([f"{key}:", val])

            # Sort the property information alphabetically
            prop_info_list = sorted(prop_info_list)

            node_info = type_info_list + prop_info_list

            node_info_string = tabulate.tabulate(
                node_info, tablefmt="html"
            )

            node_label = self.make_node_label(node, node_literals[node])

            node_attrs[node] = {
                "label": node_label,        # displayed on canvas
                "group": group,             # determines color
                "title": node_info_string,  # displayed on mouse-over
            }

        nx.set_node_attributes(g, node_attrs)
        nt = pyvis.network.Network(
            self.width, self.height, directed=True, notebook=True
        )
        nt.from_nx(g)
        return nt
