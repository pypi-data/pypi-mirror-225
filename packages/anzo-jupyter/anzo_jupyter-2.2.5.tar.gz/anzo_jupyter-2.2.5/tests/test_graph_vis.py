import unittest
import urllib3
import pyvis

from anzo_jupyter import AnzoMagics
from anzo_jupyter.graph_vis import GraphVisBuilder

from .test_common import (
    GRAPHMART,
    SERVER,
    PORT,
    USERNAME,
    PASSWORD,
)


class TestGraphVis(unittest.TestCase):
    query = """
        CONSTRUCT {
            <urn://person/alice> a <urn://Person> ;
                <urn://Person/p_name> "Alice the Astronaut" ;
                <urn://Person/p_age> "30" .

            <urn://person/bob> a <urn://Person> ;
                 <urn://Person/p_name> "Bob the Builder" ;
                 <urn://Person/p_age> "31" .

            # Instance with two types and a multi-valued property
            <urn://person/carlos> a <urn://Person>, <urn://Organism> ;
                 <urn://Person/p_name> "Carlos the Chemist" ;
                 <urn://Person/p_age> "32" ;
                 <urn://Person/p_favorite_foods> "Hot Dogs", "Apple" .

            # Instance without a type
            <urn://person/diana> <urn://Person/p_name> "Diana the Dentist" ;
                 <urn://Person/p_age> "33" .

            <urn://person/alice> <urn://Person/p_friend> <urn://person/carlos> .
            <urn://person/bob> <urn://Person/p_older_than> <urn://person/alice> .
        }
        WHERE {
            ?s ?p ?o
        }
        """  # noqa

    def setUp(self) -> None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.anzo_magic = AnzoMagics()
        self.anzo_magic.set_anzo_server(SERVER)
        self.anzo_magic.set_anzo_port(PORT)
        self.anzo_magic.set_anzo_auth(f"{USERNAME}/{PASSWORD}")
        self.anzo_magic.set_graphmart(GRAPHMART)

    def test_basic_graph_vis(self) -> None:
        self.anzo_magic.sparql("", self.query)
        self.anzo_magic.last_result("graph_vis")

    def test_after_select_query(self) -> None:
        select_query = "select * where { ?s ?p ?o } limit 5"
        self.anzo_magic.sparql("", select_query)

        self.assertRaises(
            Exception,
            self.anzo_magic.last_result,
            "graph_vis"
        )

    def test_localname(self) -> None:
        self.anzo_magic.sparql("", self.query)
        g = self.anzo_magic.last_result("nx")
        builder = GraphVisBuilder(g)

        self.assertEqual(
            builder.localname("http://csi.com/alex#bob"), "bob"
        )

        self.assertEqual(
            builder.localname("http://csi.com"), "http://csi.com"
        )

        self.assertEqual(builder.localname("http://csi.com/alex"), "alex")
        self.assertEqual(builder.localname("urn://csi/alex"), "alex")
        self.assertEqual(builder.localname("urn://csi#alex"), "alex")
        self.assertEqual(builder.localname("urn://csi"), "urn://csi")
        self.assertEqual(builder.localname("hello"), "hello")
        self.assertEqual(builder.localname(4), "4")
        self.assertEqual(builder.localname(""), "")

    def test_node_labeling(self) -> None:
        self.anzo_magic.sparql("", self.query)
        prop1 = "urn://Person/p_age"
        prop2 = "urn://Person/p_name"
        bad_prop = "urn://Person/p_bad"

        node_label_specs = [
            None, "", "uri", "localname", "localname_title",
            prop1, prop2, bad_prop
        ]

        for node_label_spec in node_label_specs:
            g = self.anzo_magic.last_result("nx")
            builder = GraphVisBuilder(g, node_label_spec=node_label_spec)
            builder.build()

    def test_edge_labeling(self) -> None:
        self.anzo_magic.sparql("", self.query)

        edge_label_specs = [
            None, "", "uri", "localname", "localname_title"
        ]

        for edge_label_spec in edge_label_specs:
            g = self.anzo_magic.last_result("nx")
            builder = GraphVisBuilder(g, edge_label_spec=edge_label_spec)
            builder.build()

    def test_bad_edge_labeling(self) -> None:
        self.anzo_magic.sparql("", self.query)
        g = self.anzo_magic.last_result("nx")

        bad_spec = "bad spec"
        builder = GraphVisBuilder(g, edge_label_spec=bad_spec)
        self.assertRaises(ValueError, builder.build)
