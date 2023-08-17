import unittest
import pandas as pd
import urllib3
import requests

import os
import json
from anzo_jupyter import AnzoMagics

from .test_common import (
    GRAPHMART,
    SERVER,
    PORT,
    USERNAME,
    PASSWORD,
)


class TestBasic(unittest.TestCase):

    def setUp(self) -> None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.anzo_magic = AnzoMagics()
        self.anzo_magic.set_graphmart(GRAPHMART)
        self.anzo_magic.set_anzo_server(SERVER)
        self.anzo_magic.set_anzo_port(PORT)
        self.anzo_magic.set_anzo_auth(f"{USERNAME}/{PASSWORD}")

    def test_get_graphmart(self):
        """
        Run AnzoMagics.get_graphmart to confirm it doesn't error.
        Output isn't checked.
        """

        res = self.anzo_magic.get_graphmarts("")
        self.assertIsNone(res)


class TestSparqlQuery(unittest.TestCase):
    select_query = """
        PREFIX data: <http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#>

        SELECT ?city WHERE {
            ?s a data:Person ;
                data:Person_City ?city .
        } ORDER BY ?city LIMIT 5
    """  # noqa

    select_query_no_limit = """
        PREFIX data: <http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#>

        SELECT ?city WHERE {
            ?s a data:Person ;
                data:Person_City ?city .
        } ORDER BY ?city
    """  # noqa

    construct_query = """
        PREFIX data: <http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#>

        construct {
            ?s data:Person_City ?city .
        }
        WHERE {
            ?s a data:Person ;
                data:Person_City ?city .
        } ORDER BY ?city LIMIT 5
    """  # noqa

    named_graph_construct_query = """
        PREFIX data: <http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#>

        construct {
            graph ?s {
                ?s data:Person_City ?city .
            }
        }
        WHERE {
            ?s a data:Person ;
                data:Person_City ?city .
        } ORDER BY ?city LIMIT 5
    """  # noqa

    empty_results_construct_query = """
        construct {
            graph ?s {
                ?s ?p ?o .
            }
        }
        WHERE {
            ?s ?p ?o .
        } LIMIT 0
    """  # noqa

    select_query_results = pd.DataFrame(
        ["Boston", "Cambridge", "Medford", "Somerville", "Watertown"],
        columns=["city"]
    )

    construct_query_results = pd.DataFrame(data={
        's': ['http://csi.com/Person/0c391c0f-340d-4f08-9fa6-13a1793c35cb', 'http://csi.com/Person/879d629b-1015-45b9-8457-7271c0f2a9f0',
              'http://csi.com/Person/a153b0aa-5583-40ff-8710-f94c8a25df3d', 'http://csi.com/Person/c2ee95a3-d5b1-40d8-8243-9c7d541853f7', 'http://csi.com/Person/ffbe9982-7491-42da-9398-e4c22fab5711'],
        'p': ['http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#Person_City', 'http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#Person_City', 'http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#Person_City',
              'http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#Person_City', 'http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#Person_City'],
        'o': ['Watertown', 'Boston', 'Somerville', 'Cambridge', 'Medford']
    }
    ).sort_values(
        by=['s', 'p', 'o'], ignore_index=True)

    named_graph_construct_query_results = pd.DataFrame(data={
        's': ['http://csi.com/Person/0c391c0f-340d-4f08-9fa6-13a1793c35cb', 'http://csi.com/Person/879d629b-1015-45b9-8457-7271c0f2a9f0', 'http://csi.com/Person/a153b0aa-5583-40ff-8710-f94c8a25df3d',
              'http://csi.com/Person/c2ee95a3-d5b1-40d8-8243-9c7d541853f7', 'http://csi.com/Person/ffbe9982-7491-42da-9398-e4c22fab5711'],
        'p': ['http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#Person_City', 'http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#Person_City', 'http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#Person_City',
              'http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#Person_City', 'http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#Person_City'],
        'o': ['Watertown', 'Boston', 'Somerville', 'Cambridge', 'Medford'],
        'g': ['http://csi.com/Person/0c391c0f-340d-4f08-9fa6-13a1793c35cb', 'http://csi.com/Person/879d629b-1015-45b9-8457-7271c0f2a9f0', 'http://csi.com/Person/a153b0aa-5583-40ff-8710-f94c8a25df3d', 'http://csi.com/Person/c2ee95a3-d5b1-40d8-8243-9c7d541853f7', 'http://csi.com/Person/ffbe9982-7491-42da-9398-e4c22fab5711']
    }
    ).sort_values(
        by=['s', 'p', 'o', 'g'], ignore_index=True)

    def setUp(self) -> None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.anzo_magic = AnzoMagics()
        self.anzo_magic.set_anzo_server(SERVER)
        self.anzo_magic.set_anzo_port(PORT)
        self.anzo_magic.set_anzo_auth(f"{USERNAME}/{PASSWORD}")
        self.anzo_magic.set_graphmart(GRAPHMART)

    def test_get_graphmart(self) -> None:
        # just test the call doesn't error out. function doesn't return values, just prints, so hard to validate results.
        self.anzo_magic.get_graphmarts("")

    def test_set_graphmart(self) -> None:
        # just test the call doesn't error out. function doesn't return values, just prints, so hard to validate results.
        am = AnzoMagics()
        am.reset()
        am.set_anzo_server(SERVER)
        am.set_anzo_port(PORT)
        am.set_anzo_auth(f"{USERNAME}/{PASSWORD}")
        am.get_graphmarts("")
        am.set_graphmart("0")

    def test_sparql_select(self) -> None:
        res = self.anzo_magic.sparql("", self.select_query)
        pd.testing.assert_frame_equal(self.select_query_results, res)

    def test_sparql_construct(self) -> None:
        res = self.anzo_magic.sparql("", self.construct_query)
        res = res.sort_values(by=res.columns.to_list(), ignore_index=True)
        pd.testing.assert_frame_equal(
            self.construct_query_results, res, check_like=True)

    def test_empty_sparql_construct(self) -> None:
        res = self.anzo_magic.sparql("", self.empty_results_construct_query)
        pd.testing.assert_frame_equal(pd.DataFrame(), res)

    def test_sparql_named_graph_construct(self) -> None:
        res = self.anzo_magic.sparql("", self.named_graph_construct_query)
        res = res.sort_values(by=res.columns.to_list(), ignore_index=True)
        pd.testing.assert_frame_equal(
            self.named_graph_construct_query_results, res)

    def test_sparql_results_dict(self) -> None:
        res = self.anzo_magic.sparql("", self.select_query)
        self.assertIsNotNone(self.anzo_magic.last_result(''))

    def test_sparql_select_results_dataframe(self) -> None:
        res = self.anzo_magic.sparql("", self.select_query)
        last_result = self.anzo_magic.last_result('df')
        pd.testing.assert_frame_equal(
            self.select_query_results, res)

    # Result nx/rdf should only work following a CONSTRUCT query

    def test_sparql_select_query_with_rdf(self) -> None:
        res = self.anzo_magic.sparql("", self.select_query)
        self.assertRaises(ValueError, self.anzo_magic.last_result, 'rdf')

    def test_sparql_select_query_with_nx(self) -> None:
        res = self.anzo_magic.sparql("", self.select_query)
        self.assertRaises(ValueError, self.anzo_magic.last_result, 'nx')

    def test_sparql_construct_query_with_rdf(self) -> None:
        res = self.anzo_magic.sparql("", self.construct_query)
        self.assertIsNotNone(self.anzo_magic.last_result('rdf'))

    def test_sparql_construct_query_with_nx(self) -> None:
        res = self.anzo_magic.sparql("", self.construct_query)
        self.assertIsNotNone(self.anzo_magic.last_result('nx'))

    def test_list_types(self) -> None:
        res = self.anzo_magic.list_types("")
        self.assertEqual(len(res), 1)

    def test_list_properties(self) -> None:
        res = self.anzo_magic.list_properties(
            "http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#Person")
        self.assertEqual(len(res), 4)

    def test_find_statements_sub(self) -> None:
        res = self.anzo_magic.find(
            "-sub http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#Person_Name")
        self.assertEqual(len(res), 7)

    def test_find_statements_two_subs(self) -> None:
        res = self.anzo_magic.find(
            "-sub http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#Person_Name -sub http://csi.com/Person/ffbe9982-7491-42da-9398-e4c22fab5711")
        self.assertEqual(len(res), 11)

    def test_find_statements_sub_and_pred(self) -> None:
        res = self.anzo_magic.find(
            "-sub http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#Person_Name -pred http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
        self.assertEqual(len(res), 4)

    def test_find_statements_sub_and_pred_and_uri(self) -> None:
        res = self.anzo_magic.find(
            "-sub http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#Person_Name -pred http://www.w3.org/1999/02/22-rdf-syntax-ns#type -uri http://www.w3.org/2002/07/owl#FunctionalProperty")
        self.assertEqual(len(res), 1)

    def test_find_statements_lit(self) -> None:
        res = self.anzo_magic.find("-lit Medford")
        self.assertEqual(len(res), 1)

    def test_find_statements_lit_multiword(self) -> None:
        res = self.anzo_magic.find(
            "-sub http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource -lit \"Auto-generated ontology from PyAnzo Datasource in PyAnzo Datasource\"")
        self.assertEqual(len(res), 2)

    def test_find_statements_lit_multiword_with_quote(self) -> None:
        # no results here, just make sure it doesn't throw a syntax error
        res = self.anzo_magic.find(
            "-lit \"Auto-generated ontology from \\\" PyAnzo Datasource in PyAnzo Datasource\"")

    def test_sparql_with_layers(self) -> None:
        # TODO: can use tests from pyanzo here to
        # test functionality with targeting layers
        pass

    def test_no_limit_provided_failure(self) -> None:
        am = AnzoMagics()
        am.reset()
        am.set_anzo_server(SERVER)
        am.set_anzo_port(PORT)
        am.set_anzo_auth(f"{USERNAME}/{PASSWORD}")
        am.set_graphmart(GRAPHMART)
        self.assertRaises(ValueError, am.sparql, "",
                          self.select_query_no_limit)

    def test_no_limit_magic(self) -> None:
        self.anzo_magic.limit("false")
        res = self.anzo_magic.sparql("", self.select_query_no_limit)
        # query returns same 5 results without no limits so can use the same check
        pd.testing.assert_frame_equal(self.select_query_results, res)

    def test_no_limit_magic_caps(self) -> None:
        self.anzo_magic.limit("False")
        res = self.anzo_magic.sparql("", self.select_query_no_limit)
        # query returns same 5 results without no limits so can use the same check
        pd.testing.assert_frame_equal(self.select_query_results, res)

    def test_limit_magic(self) -> None:
        self.anzo_magic.limit("false")
        self.anzo_magic.limit("true")
        self.assertRaises(ValueError, self.anzo_magic.sparql,
                          "", self.select_query_no_limit)

    def test_bad_limit_setting(self) -> None:
        self.anzo_magic.limit("f")
        self.assertRaises(ValueError, self.anzo_magic.sparql,
                          "", self.select_query_no_limit)

    def test_sparql_without_setting_server(self) -> None:
        am = AnzoMagics()
        am.reset()
        # am.set_anzo_server(SERVER)
        am.set_anzo_port(PORT)
        am.set_anzo_auth(f"{USERNAME}/{PASSWORD}")
        am.set_graphmart(GRAPHMART)

        self.assertRaises(
            ValueError, am.sparql, "", self.select_query
        )

    def test_sparql_without_setting_port(self) -> None:
        am = AnzoMagics()
        am.reset()
        am.set_anzo_server(SERVER)
        # am.set_anzo_port(PORT)
        am.set_anzo_auth(f"{USERNAME}/{PASSWORD}")
        am.set_graphmart(GRAPHMART)

        self.assertRaises(
            ValueError, am.sparql, "", self.select_query
        )

    def test_sparql_without_setting_auth(self) -> None:
        am = AnzoMagics()
        am.reset()
        am.set_anzo_server(SERVER)
        am.set_anzo_port(PORT)
        am.set_graphmart(GRAPHMART)
        # am.set_anzo_auth("")
        self.assertRaises(
            ValueError, am.sparql, "", self.select_query
        )

    def test_sparql_without_setting_graphmart(self) -> None:
        am = AnzoMagics()
        am.reset()
        am.set_anzo_server(SERVER)
        am.set_anzo_port(PORT)
        am.set_anzo_auth(f"{USERNAME}/{PASSWORD}")
        # am.set_graphmart(GRAPHMART)

        self.assertRaises(
            ValueError, am.sparql, "", self.select_query
        )

    def test_with_updating_graphmart(self) -> None:
        am = AnzoMagics()
        am.reset()
        am.set_anzo_server(SERVER)
        am.set_anzo_port(PORT)
        am.set_anzo_auth(f"{USERNAME}/{PASSWORD}")
        am.set_graphmart("http://bad.com")

        self.assertRaises(
            RuntimeError, am.sparql, "", self.select_query
        )

        am.set_graphmart(GRAPHMART)
        res = am.sparql("", self.select_query)
        pd.testing.assert_frame_equal(self.select_query_results, res)


class TestPrefixManager(unittest.TestCase):
    select_query = """
        SELECT ?city WHERE {
            ?s a data:Person ;
                data:Person_City ?city .
        } ORDER BY ?city LIMIT 5
    """  # noqa

    select_query_results = pd.DataFrame(
        ["Boston", "Cambridge", "Medford", "Somerville", "Watertown"],
        columns=["city"]
    )

    def setUp(self) -> None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.anzo_magic = AnzoMagics()
        self.anzo_magic.reset()
        self.anzo_magic.set_anzo_server(SERVER)
        self.anzo_magic.set_anzo_port(PORT)
        self.anzo_magic.set_anzo_auth(f"{USERNAME}/{PASSWORD}")
        self.anzo_magic.set_graphmart(GRAPHMART)

    # Assets should contain one prefix after adding a single prefix.
    def test_add_prefix(self) -> None:
        pm = self.anzo_magic.jupyter_client.prefix_manager

        self.anzo_magic.add_prefix("prefix1,http://prefix1.com")
        self.assertEqual(len(
            pm.assets), 1, "Length of assets not equal to 1 after adding a single prefix.")

    # The assets data structure is a set, so the length should be 1 if adding a duplicate prefix
    def test_add_duplicate_prefix(self) -> None:
        pm = self.anzo_magic.jupyter_client.prefix_manager

        self.anzo_magic.add_prefix("prefix1,http://prefix1.com")
        self.anzo_magic.add_prefix("prefix1,http://prefix1.com")

        self.assertEqual(len(
            pm.assets), 1, "Length of assets not equal to 1 after adding a single prefix.")

    # Lengtrh of assets should be 0 after clearing.
    def test_clear_prefixes(self) -> None:
        pm = self.anzo_magic.jupyter_client.prefix_manager
        self.anzo_magic.add_prefix("prefix1,http://prefix1.com")
        self.anzo_magic.clear_prefixes("")

        self.assertEqual(len(
            pm.assets), 0, "Length of assets not equal to 0 after adding a single prefix.")

    # listAll prefixes should return a non-empty str.
    def test_list_prefixes(self) -> None:
        pm = self.anzo_magic.jupyter_client.prefix_manager

        self.anzo_magic.add_prefix("prefix1,http://prefix1.com")

        self.assertNotEqual("", self.anzo_magic.list_prefixes(""))

    def test_sparql_with_prefix(self) -> None:
        # PREFIX data: <http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#>
        self.anzo_magic.add_prefix(
            "data,http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#")

        res = self.anzo_magic.sparql("", self.select_query)
        pd.testing.assert_frame_equal(self.select_query_results, res)


class TestLayerManager(unittest.TestCase):
    def setUp(self) -> None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.anzo_magic = AnzoMagics()
        self.anzo_magic.reset()
        self.anzo_magic.set_anzo_server(SERVER)
        self.anzo_magic.set_anzo_port(PORT)
        self.anzo_magic.set_anzo_auth(f"{USERNAME}/{PASSWORD}")
        self.anzo_magic.set_graphmart(GRAPHMART)

    def test_get_layer(self) -> None:
        lm = self.anzo_magic.jupyter_client.layer_manager
        self.anzo_magic.get_layers('')
        self.assertEqual(len(
            lm.assets), 2, "Count of layers does not match number in PyAnzo Graphmart, should be 2.")

    def test_select_layer(self) -> None:
        lm = self.anzo_magic.jupyter_client.layer_manager
        self.anzo_magic.get_layers('')
        self.anzo_magic.select_layer("0")
        self.assertEqual(len(
            lm.selected_layers), 1, "Length of assets not equal to 1 after adding a single layer by single index.")

    def test_select_int_list_layer(self) -> None:
        lm = self.anzo_magic.jupyter_client.layer_manager
        self.anzo_magic.get_layers('')
        self.anzo_magic.select_layer("0,1")
        self.assertEqual(len(
            lm.selected_layers), 2, "Length of assets not equal to 2 after selecting layers by comma separated indices.")

    def test_select_str_int_list_layer(self) -> None:
        lm = self.anzo_magic.jupyter_client.layer_manager
        self.anzo_magic.get_layers('')
        self.anzo_magic.select_layer(
            "0,http://cambridgesemantics.com/Layer/dd29f470d8d44dad8e6cf9ce3b6322fd")
        self.assertEqual(len(
            lm.selected_layers), 2, "Length of assets not equal to 2 after selecting layers by comma separated index, title.")

    def test_select_str_list_layer(self) -> None:
        lm = self.anzo_magic.jupyter_client.layer_manager
        self.anzo_magic.get_layers('')
        self.anzo_magic.select_layer(
            "http://cambridgesemantics.com/Layer/dd29f470d8d44dad8e6cf9ce3b6322fd,http://cambridgesemantics.com/Layer/d2bb3f418d7942d8a85fdedad608ccb3")
        self.assertEqual(len(
            lm.selected_layers), 2, "Length of assets not equal to 2 after selecting layers by comma seperated titles.")

    def test_select_slice_list_layer(self) -> None:
        lm = self.anzo_magic.jupyter_client.layer_manager
        self.anzo_magic.get_layers('')
        self.anzo_magic.select_layer("0:1")
        self.assertEqual(len(
            lm.selected_layers), 2, "Length of assets not equal to 1 after selecting layers by list slices..")

    def list_layers(self, line: str) -> None:
        pass

    def clear_layers(self, line: str) -> None:
        lm = self.anzo_magic.jupyter_client.layer_manager

        self.anzo_magic.add_layer("http://layer1.com")
        self.assertEqual(len(
            lm.assets), 1, "Length of assets not equal to 1 after adding a single layer.")

        self.anzo_magic.clear_layers()
        self.assertEqual(len(
            lm.assets), 0, "Length of assets not equal to 0 after clearing.")


class TestSparqlQueryJournal(unittest.TestCase):
    select_query = """
         PREFIX dc: <http://purl.org/dc/elements/1.1/>

         SELECT ?title
         WHERE {
             GRAPH ?g {
                 ?s a <http://cambridgesemantics.com/ontologies/Graphmarts#Graphmart> ;
                     dc:title ?title .
             }
             FILTER(?g = <http://cambridgesemantics.com/Graphmart/9da211618a15476daa10cead2292d8e7>)
         } LIMIT 10
    """  # noqa

    select_query_results = pd.DataFrame(
        ["PyAnzo Graphmart"],
        columns=["title"]
    )

    construct_query = """
        PREFIX dc: <http://purl.org/dc/elements/1.1/>

        CONSTRUCT {
           <urn://one> dc:title ?title
        } WHERE {
            GRAPH ?g {
                ?s a <http://cambridgesemantics.com/ontologies/Graphmarts#Graphmart> ;
                    dc:title ?title .
            }
            FILTER(?g = <http://cambridgesemantics.com/Graphmart/9da211618a15476daa10cead2292d8e7>)
        } LIMIT 10
     """  # noqa

    construct_query_results = pd.DataFrame(
        [["urn://one", "http://purl.org/dc/elements/1.1/title", "PyAnzo Graphmart"]],
        columns=["s", "p", "o"]
    )

    def setUp(self) -> None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.anzo_magic = AnzoMagics()
        self.anzo_magic.reset()
        self.anzo_magic.set_anzo_server(SERVER)
        self.anzo_magic.set_anzo_port(PORT)
        self.anzo_magic.set_anzo_auth(f"{USERNAME}/{PASSWORD}")

    def test_sparql_journal_select(self) -> None:
        res = self.anzo_magic.sparql_journal("", self.select_query)
        pd.testing.assert_frame_equal(self.select_query_results, res)

    def test_sparql_journal_construct(self) -> None:
        res = self.anzo_magic.sparql_journal("", self.construct_query)
        pd.testing.assert_frame_equal(self.construct_query_results, res)


class TestSparqlQuerySystemTables(unittest.TestCase):
    select_query = """
        PREFIX system: <http://openanzo.org/ontologies/2008/07/System#>


        SELECT DISTINCT ?type
        WHERE {
           ?s a ?type .
           FILTER(?type = system:QueryExecution)
        } LIMIT 5
    """  # noqa

    select_query_results = pd.DataFrame(
        ["http://openanzo.org/ontologies/2008/07/System#QueryExecution"],
        columns=["type"]
    )

    construct_query = """
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX system: <http://openanzo.org/ontologies/2008/07/System#>

        CONSTRUCT {
            <urn://one> dc:title ?type
        } WHERE {
           ?s a ?type .
           #FILTER(?type = system:QueryExecution)
        }
        LIMIT 10
     """  # noqa

    construct_query_results = pd.DataFrame(
        [["urn://one",
          "http://purl.org/dc/elements/1.1/title",
          "http://openanzo.org/ontologies/2008/07/System#QueryExecution"]],
        columns=["s", "p", "o"]
    )

    def setUp(self) -> None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.anzo_magic = AnzoMagics()
        self.anzo_magic.reset()
        self.anzo_magic.set_anzo_server(SERVER)
        self.anzo_magic.set_anzo_port(PORT)
        self.anzo_magic.set_anzo_auth(f"{USERNAME}/{PASSWORD}")

    def test_sparql_system_tables_select(self) -> None:
        res = self.anzo_magic.sparql_system_tables("", self.select_query)
        pd.testing.assert_frame_equal(self.select_query_results, res)

    # def test_sparql_system_tables_construct(self) -> None:
        #res = self.anzo_magic.sparql_system_tables("", self.construct_query)
        #pd.testing.assert_frame_equal(self.construct_query_results, res)


class TestCookieAuthentication(unittest.TestCase):
    select_query = """
        PREFIX data: <http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#>

        SELECT ?city WHERE {
            ?s a data:Person ;
                data:Person_City ?city .
        } ORDER BY ?city LIMIT 5
    """  # noqa

    select_query_results = pd.DataFrame(
        ["Boston", "Cambridge", "Medford", "Somerville", "Watertown"],
        columns=["city"]
    )

    def setUp(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def test_auth_with_cookie(self) -> None:
        url = f"https://{SERVER}:{PORT}/anzo_authenticate?client_name=AnzoFormClient"  # noqa

        session = requests.Session()
        data = {
            "anzo_username": USERNAME,
            "anzo_password": PASSWORD,
        }

        session.post(url, verify=False, data=data)
        half_of_token = session.cookies.get_dict()['BAYEUX_BROWSER']
        auth_token = f"BAYEUX_BROWSER={half_of_token}"

        anzo_magic = AnzoMagics()
        anzo_magic.reset()  # reset to force the jupyter global state to reset
        anzo_magic.set_anzo_server(SERVER)
        anzo_magic.set_anzo_port(PORT)
        anzo_magic.set_anzo_auth_token(auth_token)
        anzo_magic.set_graphmart(GRAPHMART)

        res = anzo_magic.sparql("", self.select_query)
        pd.testing.assert_frame_equal(self.select_query_results, res)

        anzo_magic.reset()  # reset to force the jupyter global state to reset

    def test_no_auth_provided(self) -> None:
        url = f"https://{SERVER}:{PORT}/anzo_authenticate?client_name=AnzoFormClient"  # noqa

        anzo_magic = AnzoMagics()
        anzo_magic.reset()  # reset to force the jupyter global state to reset
        anzo_magic.set_anzo_server(SERVER)
        anzo_magic.set_anzo_port(PORT)
        anzo_magic.set_graphmart(GRAPHMART)

        self.assertRaises(
            ValueError,
            anzo_magic.sparql,
            "",
            self.select_query
        )

    def test_token_then_username_password_(self) -> None:
        url = f"https://{SERVER}:{PORT}/anzo_authenticate?client_name=AnzoFormClient"  # noqa

        session = requests.Session()
        data = {
            "anzo_username": USERNAME,
            "anzo_password": PASSWORD,
        }

        session.post(url, verify=False, data=data)
        half_of_token = session.cookies.get_dict()['BAYEUX_BROWSER']
        auth_token = f"BAYEUX_BROWSER={half_of_token}"

        anzo_magic = AnzoMagics()
        anzo_magic.reset()  # reset to force the jupyter global state to reset
        anzo_magic.set_anzo_server(SERVER)
        anzo_magic.set_anzo_port(PORT)
        anzo_magic.set_anzo_auth_token(auth_token)
        anzo_magic.set_graphmart(GRAPHMART)

        self.assertRaises(
            ValueError,
            anzo_magic.set_anzo_auth,
            f"{USERNAME}/{PASSWORD}"
        )

        anzo_magic.reset()  # reset to force the jupyter global state to reset

    def test_username_password_then_token(self) -> None:
        url = f"https://{SERVER}:{PORT}/anzo_authenticate?client_name=AnzoFormClient"  # noqa

        session = requests.Session()
        data = {
            "anzo_username": USERNAME,
            "anzo_password": PASSWORD,
        }

        session.post(url, verify=False, data=data)
        half_of_token = session.cookies.get_dict()['BAYEUX_BROWSER']
        auth_token = f"BAYEUX_BROWSER={half_of_token}"

        anzo_magic = AnzoMagics()
        anzo_magic.reset()  # reset to force the jupyter global state to reset
        anzo_magic.set_anzo_server(SERVER)
        anzo_magic.set_anzo_port(PORT)
        anzo_magic.set_graphmart(GRAPHMART)

        anzo_magic.set_anzo_auth(f"{USERNAME}/{PASSWORD}")
        self.assertRaises(
            ValueError,
            anzo_magic.set_anzo_auth_token,
            auth_token
        )

        anzo_magic.reset()  # reset to force the jupyter global state to reset


class TestClientConfiguration(unittest.TestCase):
    def setUp(self) -> None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.anzo_magic = AnzoMagics()
    # test case should fail if file doesn't exist

    def test_read_invalid_config(self) -> None:
        am = AnzoMagics()
        self.assertRaises(
            OSError, am.set_anzo_config, "/this-file-should-not-exist.txt"
        )

    def test_read_valid_config(self) -> None:
        am = AnzoMagics()
        home = os.environ['HOME']
        config_path = f'{home}/.anzo/jupyter_test_config.json'

        with open(config_path, "w") as config:
            settings = {
                "anzo_server": "localhost",
                "anzo_port": "8443",
                "anzo_username": "sysadmin",
                "anzo_password": "123",
                "graphmart": "<ANZO_GRAPHMART>"
            }
            config.write(json.dumps(settings))

        am.set_anzo_config(config_path)

        # Test that this call doesnt error out after providing the right configuration
        am.get_graphmarts("")
