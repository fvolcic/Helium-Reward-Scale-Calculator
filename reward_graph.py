"""File that represents the Reward a hexagon graph.

Information on the algorithm can be found at:
    -> https://github.com/helium/HIP/blob/master/0017-hex-density-based-transmit-reward-scaling.md

"""

import h3

from graph import Graph
from graph import read_graph_from_csv

from chain_vars import *

class RewardGraph:
    """A graph data structure."""

    def __init__(self):
        """Constructor."""

        # hex_dict is used to store all hexagons needed for reward algorithms.
        self.hex_dict = HexDict()
        self.graph = Graph()

    def import_graph_from_csv(self, graph_file):
        """Import a graph from a csv file."""
        nodes_file = graph_file + "_nodes.csv"
        edges_file = graph_file + "_edges.csv"

        self.graph = read_graph_from_csv( f"graph_data/{nodes_file}", f"graph_data/{edges_file}", True )
        for node in self.nodes(): 
            self.hex_dict.add_hex(float(node['lat']), float(node['lng']), node['name'])

    def geo_to_node(self, lat:float, lng:float, node_id = None):
        """A position to latitude and longitude coordinates.
        
        REQUIRES:
            -> lat: latitude for a given node.
            -> lng: longitude for a given node.
            -> node_id: a unique id given to a node. 
                    will be set automatically if not provided.
        RETURNS:
            -> Node: the return from this function will be the newly created node.
        """
        if node_id is None:
            node_id = f'{lat}{lng}'

        self.graph.add_node(node_id, lat=lat, lng=lng)
        self.hex_dict.add_hex(lat, lng)

    def get_reward_scale(self, node):
        """Given a node in the graph, return the computed reward scale.
        
        REQUIRES:
            -> node: must be a valid node that exists internally in the graph.
        RETURNS: 
            -> float: the reward scale as an float for a given node.
        """
        if 'reward_scale' not in node.attributes:
            self._generate_reward_scales()
        return node['reward_scale']

    def nodes(self):
        """Get the nodes of the graph."""
        return self.graph.nodes()

    def _generate_reward_scales(self):
        """Runs all prediction algorithms on the graph.
        -> Will compute the reward scale for all nodes in the given graph.
            -> Node will receive a 'reward_scale' attribute once run.
        """
        self.hex_dict.generate_max_res_meta()
        self.hex_dict.generate_parents()
        for node in self.graph.nodes():
            node['reward_scale'] = self.hex_dict.compute_reward_scale(float(node['lat']), float(node['lng']))

class HexDict:
    """A class representing a hexagon dictionary."""

    def __init__(self): 
        """Constructor for a hex map."""
        self.hex_dict = [ {} for _ in range(RES_MAX + 1) ] 
    
    def __getitem__(self, hex_id):
        """Return the hex with the given hex id."""
        res = h3.h3_get_resolution(hex_id)
        if hex_id not in self.hex_dict[res]:
            raise Exception("item not in hex dict. illigal access.")
        return self.hex_dict[res][hex_id]
    
    def __setitem__(self, hex_id, hex):
        """Set a hex with the given hex_id."""
        res = h3.h3_get_resolution(hex_id)
        if not isinstance(hex, Hexagon):
            raise Exception("Can only set hex_dict items with a Hexagon object.")
        self.hex_dict[res][hex_id] = hex

    def __contains__(self, hex_id):
        """Determine if a given hex_id is in the hex_dict."""
        res = h3.h3_get_resolution(hex_id)
        if not hex_id in self.hex_dict[res]:
            return False
        return True

    def add_hex(self, lat:float, lng:float, name=None):
        """Insert a hex into the HexDict.
        
        REQUIRES: 
            lat: latitude of the coordinate. 
            lng: longitude of the coordinate.
        
        EFFECTS:
            -> If the RES_MAX hex does not exist, then the RES_MAX hex is added,
            and the raw density is set to 1. 
            -> If the RES_MAX hex already exists, then the raw density of the hex
            is just incremented by 1.

        RETURNS: Hexagon
            returns the RES_MAX hexagon of the given coordinates.
        """
        
        hex_id = h3.geo_to_h3(lat, lng, RES_MAX)
        if hex_id not in self.hex_dict[RES_MAX]:
            self.hex_dict[RES_MAX][hex_id] = Hexagon(hex_id)
            self.hex_dict[RES_MAX][hex_id].raw_density = 1
        else:
            self.hex_dict[RES_MAX][hex_id].raw_density += 1

        self.hex_dict[RES_MAX][hex_id].residents.append(name)
        return self.hex_dict[RES_MAX][hex_id]


    def generate_max_res_meta(self):
        """Generate the clipped densities for all MAX_RES hexagons.
        
        EFFECTS:
            -> Will generate the density limit, clipped, and unclipped for 
                all MAX_RES hexagons.
        
        """
        for hex in self.hex_dict[RES_MAX].values():
            occupied_count = 0
            hex_neighbors = self.neighbors(hex)
            for neighbor in hex_neighbors:
                if neighbor.raw_density >= HIP_RES_META[RES_MAX][1]:
                    occupied_count += 1
            hex.occupied_count = occupied_count
            hex.hex_density_limit = min(
                HIP_RES_META[RES_MAX][1] * max(occupied_count - HIP_RES_META[RES_MAX][0] + 1, 1),
                HIP_RES_META[RES_MAX][2]
            )
            hex.clipped_density = min(
                hex.hex_density_limit,
                hex.raw_density
            )
            hex.unclipped_density = hex.raw_density

    def neighbors(self, hex):
        """Return a list of all neighbors of a hex.
        All neighbors include the current hex as well.
        REQUIRES:
            -> A valid hex object.
        RETURNS:
            -> A list of all neighboring hex objects.
        """
        neighboring_hexs = list(hex.neighbors)
        # neighboring_hexs.append(hex.hex_id)
        neighbors = []
        for neighbor in neighboring_hexs:
            if neighbor in self:
                neighbors.append(self[neighbor])
            else:
                neighbors.append(Hexagon(neighbor))
        return neighbors

    def children(self, hex):
        """Generate all children hex.
        
        REQUIRES:
            -> hex: a valid hex object.
        
        EFFECTS:
            -> DOES NOT CHANGE THE HEX DICT.
                - if there is a child that is not currently in the hex dict,
                    it will be returned, but no information about the child in saved
                    in the hex dict.

        RETURNS:
            -> A list of all child hex objects.
        
        """
        children = hex.children()
        children_list = []
        for child in children:
            if child in self:
                children_list.append(self[child])
            else:
                children_list.append(Hexagon(child))
        return children_list

    def generate_parents(self, resolution=RES_MAX, generation_id=0):
        """Takes all max res hexagons, and generates their parent hexagons.
        
        REQUIRES:
            -> Requires a valid resolution. Starting resolution is RES_MAX be default.

        EFFECTS:
            -> Generates new hexagons at all resolutions until RES_MIN.
            -> Sets the clipped and unclipped densities of each hex added.
        """
        parent_res = resolution - 1
        for hex in self.hex_dict[resolution].values():
                        
            parent = h3.h3_to_parent(hex.hex_id, parent_res)
            
            # If the parent has already been generated in the hex_dict, then there
            # is no need to regenerate the hex meta data.
            if parent in self.hex_dict[parent_res]\
                and self.hex_dict[parent_res][parent].generation_id == generation_id:
                self.hex_dict[parent_res][parent].residents += hex.residents
                continue
            self.hex_dict[parent_res][parent] = Hexagon(parent)
            self.hex_dict[parent_res][parent].generation_id = generation_id
            self.hex_dict[parent_res][parent].residents += hex.residents
            # Generate the unclipped density of the parent hex
            unclipped = 0
            for child in self.children(self.hex_dict[parent_res][parent]):
                unclipped += child.clipped_density
            
            self.hex_dict[parent_res][parent].unclipped_density = unclipped

            # once all parents are generated along with their unclipped densities, 
            # we can then generate their clipped densities.
            for parent in self.hex_dict[parent_res].values():
                neighbors = self.neighbors(parent)
                occupied_count = 0
                for neighbor in neighbors:
                    if neighbor.unclipped_density >= HIP_RES_META[parent.res][1]:
                        occupied_count += 1
                parent.occupied_count = occupied_count
                parent.hex_density_limit = min(
                    HIP_RES_META[parent.res][1] * max(occupied_count - HIP_RES_META[parent.res][0] + 1, 1),
                    HIP_RES_META[parent.res][2]
                )
                parent.clipped_density = min(
                    parent.unclipped_density,
                    parent.hex_density_limit
                )
            
        if resolution > RES_MIN:
            self.generate_parents(resolution-1, generation_id)
    
    def compute_reward_scale(self, lat:float, lng:float):
        """Generate the reward scale for a given location."""
        hex_id = h3.geo_to_h3(lat, lng, RES_MAX)
        if hex_id not in self.hex_dict[RES_MAX]:
            raise Exception("Cannot compute reward scale. Invalid starting hex.")
        current_hex = self.hex_dict[RES_MAX][hex_id]
        reward_scale = 1
        while current_hex.res >= RES_MIN:
            parent = self[h3.h3_to_parent(current_hex.hex_id, current_hex.res - 1)]
            reward_scale = reward_scale * (parent.clipped_density / parent.unclipped_density)
            current_hex = parent
        
        return reward_scale

class Hexagon:
    """Class representing an h3 hexagon."""

    def __init__(self, hex_id):
        """Hexagon constructor."""
        self.hex_id = hex_id

        # hex res metadata
        self.res = h3.h3_get_resolution(hex_id)

        # Hex density metadata
        self.raw_density = 0
        self.clipped_density = 0
        self.unclipped_density = 0

        # Information for reward scale algorithm
        self.density_max = HIP_RES_META[self.res][2]
        self.density_tgt = HIP_RES_META[self.res][1]
        self.N = HIP_RES_META[self.res][0] 

        # more info for the algorithms
        self.occupied_count = 0
        self.hex_density_limit = self.density_max

        # generation id information for generating meta data about a hex.
        self.generation_id = -1

        self.residents = []

    # ------------- PROPERTY METHODS FOR CLASS -------------------------------
    
    @property
    def neighbors(self):
        """Returns the neighbors of a given node as a list."""
        # return h3.hex_ring(self.hex_id, 1) 
        return h3.hex_range(self.hex_id, 1)
    def children(self, res=None):
        """Return the children of a given node with given res."""
        if res is None:
            res = self.res + 1
        return h3.h3_to_children(self.hex_id, res)