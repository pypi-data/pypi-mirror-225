from .node import Node
from .link import Link
import json


class Network():

    def __init__(self, arg=None):
        self.__link_counter = 0
        self.__node_counter = 0
        self.__nodes = []
        self.__links = []
        self.__links_in = []
        self.__links_out = []
        self.__nodes_in = []
        self.__nodes_out = []

        self.nodes_in.append(0)
        self.nodes_out.append(0)

        if arg != None:
            if isinstance(arg, Network):
                self.__link_counter = arg.link_counter
                self.__node_counter = arg.node_counter
                self.__nodes = arg.nodes
                self.__links = arg.links
                self.__links_in = arg.links_in
                self.__links_out = arg.links_out
                self.__nodes_in = arg.nodes_in
                self.__nodes_out = arg.nodes_out
            else:
                f = open(arg)
                NSFnet = json.load(f)
                f.close()
                nummber_of_nodes = len(NSFnet["nodes"])
                number_of_links = len(NSFnet["links"])
                for i in range(0, nummber_of_nodes):
                    id = NSFnet["links"][i]["id"]
                    node = Node(id)
                    self.add_node(node)

                for i in range(0, number_of_links):
                    id = NSFnet["links"][i]["id"]
                    length = NSFnet["links"][i]["length"]
                    slots = NSFnet["links"][i]["slots"]
                    link = Link(id, length, slots)
                    self.add_link(link)

                    src = NSFnet["links"][i]["src"]
                    id = NSFnet["links"][i]["id"]
                    dst = NSFnet["links"][i]["dst"]
                    self.connect(src, id, dst)

    @property
    def nodes(self):
        return self.__nodes

    @property
    def links(self):
        return self.__links

    @property
    def node_counter(self):
        return self.__node_counter

    @property
    def nodes_in(self):
        return self.__nodes_in

    @property
    def nodes_out(self):
        return self.__nodes_out

    @property
    def link_counter(self):
        return self.__link_counter

    @property
    def links_out(self):
        return self.__links_out

    @property
    def links_in(self):
        return self.__links_in

    def get_link(self, link_pos):
        if(link_pos < 0) or (link_pos >= len(self.__links)):
            raise ValueError("Cannot get Link from a position out of bounds.")
        return self.__links[link_pos]

    def get_node(self, node_pos):
        if (node_pos < 0) or (node_pos >= len(self.__nodes)):
            raise ValueError("Cannot get Node from a position out of bounds.")
        return self.__nodes[node_pos]

    def add_node(self, node: Node):
        if node.id != self.__node_counter:
            raise ValueError(
                "Cannot add a Node to this network with Id mismatching node counter.")
        self.__node_counter += 1
        self.__nodes.append(node)
        self.__nodes_in.append(0)
        self.__nodes_out.append(0)

    def add_link(self, link: Link):
        if link.id != self.__link_counter:
            raise ValueError(
                "Cannot add a Link to this network with Id mismatching link counter.")
        self.__link_counter += 1
        self.__links.append(link)

    def connect(self, src, link_pos, dst):
        if(src < 0) or (src >= self.__node_counter):
            raise ValueError(
                f"Cannot connect src {src} because its ID is not in the network. Number of nodes in network: {self.node_counter}")

        if(dst < 0) or (dst >= self.__node_counter):
            raise ValueError(
                f"Cannot connect dst {dst} because its ID is not in the network. Number of nodes in network: {self.node_counter}")

        if(link_pos < 0) or (link_pos >= self.__link_counter):
            raise ValueError(
                f"Cannot use link {link_pos} because its ID is not in the network. Number of links in network: {self.link_counter}")

        self.__links_out.insert(self.__nodes_out[src], self.__links[link_pos])
        for i in range((src+1), len(self.__nodes_out)):
            self.__nodes_out[i] += 1
        self.__links_in.insert(self.__nodes_in[dst], self.__links[link_pos])
        for i in range((dst+1), len(self.__nodes_in)):
            self.__nodes_in[i] += 1
        self.__links[link_pos].src = src
        self.__links[link_pos].dst = dst

    def is_connected(self, src, dst):
        for i in range(self.__nodes_out[src], self.__nodes_out[src+1]):
            for j in range(self.__nodes_in[dst], self.__nodes_in[dst+1]):
                if self.__links_out[i].id == self.__links_in[j].id:
                    return self.__links_out[i].id
        return -1

    def use_slot(self, link_pos, *, slot_pos=None, slot_from=None, slot_to=None):
        if (link_pos < 0) or (link_pos >= len(self.__links)):
            raise ValueError("Link position out of bounds")
        if (slot_pos != None) and (slot_from == None) and (slot_to == None):
            if(slot_pos < 0) or (slot_pos >= self.__links[link_pos].slots_number()):
                raise ValueError("Slot position out of bounds.")
            self.__links[link_pos].set_slot(slot_pos, True)

        elif (slot_pos == None) and (slot_from != None) and (slot_to != None):
            if(slot_from < 0) or (slot_from >= self.__links[link_pos].slots_number()):
                raise ValueError("Slot position out of bounds.")
            if(slot_to < 0) or (slot_to >= self.__links[link_pos].slots_number()):
                raise ValueError("Slot position out of bounds.")
            if(slot_from > slot_to):
                raise ValueError(
                    "Initial slot position must be lower than the final slot position.")
            if(slot_from == slot_to):
                raise ValueError("Slot from and slot To cannot be equals.")

            for i in range(slot_from, slot_to):
                self.__links[link_pos].set_slot(i, True)

        else:
            raise ValueError("Incorrect arguments given.")

    def unuse_slot(self, link_pos, *, slot_pos=None, slot_from=None, slot_to=None):
        if (link_pos < 0) or (link_pos >= len(self.__links)):
            raise ValueError("Link position out of bounds")
        if (slot_pos != None) and (slot_from == None) and (slot_to == None):
            if(slot_pos < 0) or (slot_pos >= self.__links[link_pos].slots_number()):
                raise ValueError("Slot position out of bounds.")
            self.__links[link_pos].set_slot(slot_pos, False)

        elif (slot_pos == None) and (slot_from != None) and (slot_to != None):
            if(slot_from < 0) or (slot_from >= self.__links[link_pos].slots_number()):
                raise ValueError("Slot position out of bounds.")
            if(slot_to < 0) or (slot_to >= self.__links[link_pos].slots_number()):
                raise ValueError("Slot position out of bounds.")
            if(slot_from > slot_to):
                raise ValueError(
                    "Initial slot position must be lower than the final slot position.")
            if(slot_from == slot_to):
                raise ValueError("Slot from and slot To cannot be equals.")

            for i in range(slot_from, slot_to):
                self.__links[link_pos].set_slot(i, False)

        else:
            raise ValueError("Incorrect arguments given.")

    def is_slot_used(self, link_pos, *, slot_pos=None, slot_from=None, slot_to=None):
        if (link_pos < 0) or (link_pos >= len(self.__links)):
            raise ValueError("Link position out of bounds")
        if (slot_pos != None) and (slot_from == None) and (slot_to == None):
            if(slot_pos < 0) or (slot_pos >= self.__links[link_pos].slots_number()):
                raise ValueError("Slot position out of bounds.")
            return self.__links[link_pos].get_slot(slot_pos)

        elif (slot_pos == None) and (slot_from != None) and (slot_to != None):
            if(slot_from < 0) or (slot_from >= self.__links[link_pos].slots_number()):
                raise ValueError("Slot position out of bounds.")
            if(slot_to < 0) or (slot_to >= self.__links[link_pos].slots_number()):
                raise ValueError("Slot position out of bounds.")
            if(slot_from > slot_to):
                raise ValueError(
                    "Initial slot position must be lower than the final slot position.")
            if(slot_from == slot_to):
                raise ValueError("Slot from and slot To cannot be equals.")

            for i in range(slot_from, slot_to):
                if self.__links[link_pos].get_slot(i):
                    return True
            return False

        else:
            raise ValueError("Incorrect arguments given.")

    def average_neighborhood(self):
        if self.__node_counter == 0:
            raise ValueError("The network must be have at least one node.")
        result = self.__link_counter/self.__node_counter
        return result

    def normal_average_neighborhood(self):
        if self.__node_counter == 0:
            raise ValueError("The network must be have at least one node.")
        result = self.__link_counter / \
            (self.__node_counter * (self.__node_counter - 1))
        return result

    def nodal_variance(self):
        if self.__node_counter == 0:
            raise ValueError("The network must be have at least one node.")
        result = 0.0
        average = self.average_neighborhood()
        for i in range(self.__node_counter):
            result += pow((self.__nodes_out[i+1] -
                          self.__nodes_out[i])-average, 2)
        result /= self.__node_counter
        return result
