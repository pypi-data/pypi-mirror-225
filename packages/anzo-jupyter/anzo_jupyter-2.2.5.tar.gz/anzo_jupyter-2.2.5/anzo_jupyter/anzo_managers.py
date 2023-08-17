from .anzo_jupyter_util import parse_list_indices_from_string

# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

class BaseAnzoArtifact:
    def __init__(self, title, uri) -> None:
        self.title = title
        self.uri = uri

    def __hash__(self):
        return hash((self.title, self.uri))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.title == other.title and self.uri == other.uri


class Graphmart(BaseAnzoArtifact):
    def __str__(self):
        return "GRAPHMART {p}: <{u}> ".format(p=self.title, u=self.uri)


class Layer(BaseAnzoArtifact):
    def __init__(self, title, uri, index) -> None:
        self.title = title
        self.uri = uri
        self.index = index

    def __str__(self):
        return "LAYER {p}: <{u}> ".format(p=self.title, u=self.uri)


class Prefix(BaseAnzoArtifact):
    def __str__(self):
        return "PREFIX {p}: <{u}> ".format(p=self.title, u=self.uri)


# Base functionality of asset manager
class AssetManager():
    def __init__(self) -> None:
        self.assets = []

    def clear(self) -> None:
        self.assets = []

    def list_all(self) -> None:
        for a in self.assets:
            print(a)


# Implement add function based on type of asset to manage.
class PrefixManager(AssetManager):
    def add(self, prefix: str, uri: str) -> None:
        if validate_uri(uri):
            self.assets.append(Prefix(prefix.strip(), uri.strip()))
        else:
            print("Attempted to add prefix with an invalid URI.")
        self.assets = list(set(self.assets))

    # Prepends the set of prefixes to a query, returning the string.
    def include_prefixes(self, query: str = None) -> str:
        res = ""
        for p in self.assets:
            res += str(p) + "\n"
        return res + query


class LayerManager(AssetManager):
    def __init__(self) -> None:
        super(LayerManager, self).__init__()
        self.selected_layers = set()

    def add(self, assets: set, title: str, uri: str, index: int) -> None:
        assets.add(Layer(title, uri, index))

    def parse_input_layers(self, str_layers: str) -> None:
        select_layers = parse_list_indices_from_string(str_layers, self.assets)
        for layer in select_layers:
            self.select_layer(layer)

    def select_layer(self, uri: str) -> None:
        layer_count = len(self.assets)

        if uri.isnumeric():
            index = int(uri)
            if index >= layer_count or layer_count <= 0:
                raise ValueError(f'Invalid Option: {uri}.')
            layer = self.assets[index]
            uri = layer.uri

        self.selected_layers.add(uri)

        print(f"Selected layer  -- {uri}")

    def clear(self) -> None:
        self.selected_layers.clear()
        self.assets = []

    def parse_layers(self, layers: list) -> None:
        layer_set = set()
        for row in layers:
            layer = row['layer']['value']
            title = row['title']['value']
            index = int(row['index']['value'])
            self.add(layer_set, title, layer, index)
        self.assets = sorted(list(layer_set), key=lambda l: l.index)
        self.print()

    def print(self) -> None:
        layers = self.assets
        for i in range(len(layers)):
            layer = layers[i]
            print(f'[{i}]: {layer.title} -- {layer.uri} ')


class GraphmartManager(AssetManager):
    def __init__(self) -> None:
        AssetManager.__init__(self)
        self.selected_graphmart = None

    def set_graphmart(self, uri: str) -> None:
        gmart_count = len(self.assets)
        if uri.isnumeric():
            index = int(uri)
            if index >= gmart_count or gmart_count <= 0:
                raise ValueError(f'Invalid Graphmart Option: {uri}.')
            gmart = self.assets[index]
            uri = gmart.uri
        print(f"Selected graphmart  -- {uri}")
        self.selected_graphmart = uri

    def add(self, assets: set, title: str, uri: str) -> None:
        if validate_uri(uri):
            assets.add(Graphmart(title.strip(), uri.strip()))
        else:
            print("Attempted to add prefix with an invalid URI.")

    def parse_graphmarts(self, graphmarts: list) -> None:
        gmart_set = set()
        for gmart in graphmarts:
            gmarts = gmart['gmart']['value']
            title = gmart['title']['value']
            self.add(gmart_set, title, gmarts)
        self.assets = sorted(list(gmart_set), key=lambda l: l.title)
        self.print()

    def print(self) -> None:
        graphmarts = self.assets
        for i in range(len(graphmarts)):
            g = graphmarts[i]
            print(f"[{i}]: {g.title} -- {g.uri}")

# Placeholder, todo: update with sophisticated uri checks


def validate_uri(uri: str) -> bool:
    #uri = uri.lower()
    return True
