#!/usr/bin/env python3
"""
CH446Q Matrix Routing Module for Jumperless V5-light.
Manages node mapping, X/Y coordinate resolution, active switch connections,
dynamic Y-bus allocation to avoid net shorting, and netlist generation.
"""

from typing import Dict, List, Set, Tuple, Optional


class CH446QMatrix:

    # Valid breadboard node mappings to CH446Q X and Y coordinates
    SPECIAL_NODES = {
        "TOP_RAIL": (0, 7),     # Y7 on chip 0
        "BOTTOM_RAIL": (1, 7),  # Y7 on chip 1
        "VPLUS": (0, 6),        # Y6 on chip 0
        "VMINUS": (1, 6),       # Y6 on chip 1
        "GPIO0": (0, 5),        # Y5 on chip 0
        "GPIO1": (0, 4),        # Y4 on chip 0
        "GPIO2": (1, 5),        # Y5 on chip 1
        "GPIO3": (1, 4),        # Y4 on chip 1
        "ADC0": (0, 3),         # Y3 on chip 0
        "ADC1": (1, 3),         # Y3 on chip 1
    }

    # Dynamic X-to-X routing channels available on Y-bus
    DYNAMIC_Y_BUS_CHANNELS = [0, 1, 2]

    def __init__(self, num_chips: int = 2):
        self.num_chips = num_chips
        # Active connections stored as set of tuples: (chip_id, x_addr, y_addr, node_a, node_b)
        self.active_routes: Set[Tuple[int, int, int, str, str]] = set()

    def _resolve_node(self, node: str) -> Tuple[int, int]:
        """
        Maps a node identifier string (e.g. '1', '15', 'TOP_RAIL', 'GPIO0')
        to (chip_id, x_or_y_addr).
        Returns (chip_id, address).
        """
        node_str = node.strip().upper()

        if node_str in self.SPECIAL_NODES:
            return self.SPECIAL_NODES[node_str]

        try:
            val = int(node_str)
            if 1 <= val <= 16:
                return (0, val - 1)  # Chip 0, X0..X15
            elif 17 <= val <= 32:
                return (1, val - 17) # Chip 1, X0..X15
            else:
                raise ValueError(f"Tie-point row {val} out of range (1..32)")
        except ValueError as e:
            if "out of range" in str(e):
                raise
            raise ValueError(f"Invalid node identifier: '{node}'")

    def _allocate_y_bus(self, norm_a: str, norm_b: str) -> int:
        """
        Dynamically finds an available Y-bus channel that is either already connected to one
        of the nodes, or completely unused by existing X-to-X nets.
        """
        bus_usage: Dict[int, Set[str]] = {y: set() for y in self.DYNAMIC_Y_BUS_CHANNELS}

        for r in self.active_routes:
            y_ch = r[2]
            if y_ch in bus_usage:
                bus_usage[y_ch].add(r[3])
                bus_usage[y_ch].add(r[4])

        # Check if either norm_a or norm_b is already connected on an existing bus
        for y_ch, nodes in bus_usage.items():
            if norm_a in nodes or norm_b in nodes:
                return y_ch

        # Find first completely empty Y bus channel
        for y_ch in self.DYNAMIC_Y_BUS_CHANNELS:
            if len(bus_usage[y_ch]) == 0:
                return y_ch

        raise ValueError("Matrix routing collision: All dynamic Y-bus channels are occupied.")

    def connect(self, node_a: str, node_b: str) -> dict:
        """
        Establishes an analog crosspoint switch route between node_a and node_b.
        """
        norm_a = node_a.strip().upper()
        norm_b = node_b.strip().upper()

        if norm_a == norm_b:
            raise ValueError("Cannot connect a node to itself.")

        chip_a, addr_a = self._resolve_node(norm_a)
        chip_b, addr_b = self._resolve_node(norm_b)

        if norm_a in self.SPECIAL_NODES:
            chip_id, y_addr = self.SPECIAL_NODES[norm_a]
            x_chip, x_addr = chip_b, addr_b
            route_entry = (chip_id, x_addr, y_addr, norm_a, norm_b)
        elif norm_b in self.SPECIAL_NODES:
            chip_id, y_addr = self.SPECIAL_NODES[norm_b]
            x_chip, x_addr = chip_a, addr_a
            route_entry = (chip_id, x_addr, y_addr, norm_a, norm_b)
        else:
            # X-to-X routing: allocate dynamic Y bus channel to prevent net collisions
            y_addr = self._allocate_y_bus(norm_a, norm_b)
            chip_id = chip_a
            x_addr = addr_a
            route_entry = (chip_id, x_addr, y_addr, norm_a, norm_b)

        self.active_routes.add(route_entry)

        return {
            "route_id": f"route_{norm_a}_{norm_b}",
            "node_a": norm_a,
            "node_b": norm_b,
            "chip_id": chip_id,
            "x_addr": x_addr,
            "y_addr": y_addr,
            "resistance_ohms": 88.5,
            "status": "CONNECTED"
        }

    def disconnect(self, node_a: str, node_b: str) -> bool:
        """
        Disconnects an existing route between node_a and node_b.
        """
        norm_a = node_a.strip().upper()
        norm_b = node_b.strip().upper()

        to_remove = None
        for r in self.active_routes:
            if (r[3] == norm_a and r[4] == norm_b) or (r[3] == norm_b and r[4] == norm_a):
                to_remove = r
                break

        if to_remove:
            self.active_routes.remove(to_remove)
            return True
        return False

    def reset_matrix(self) -> int:
        """
        Clears all active connections on the matrix switch array.
        """
        count = len(self.active_routes)
        self.active_routes.clear()
        return count

    def get_active_routes(self) -> List[dict]:
        """
        Returns a list of all active routes.
        """
        routes = []
        for r in self.active_routes:
            routes.append({
                "route_id": f"route_{r[3]}_{r[4]}",
                "node_a": r[3],
                "node_b": r[4],
                "chip_id": r[0],
                "x_addr": r[1],
                "y_addr": r[2],
                "resistance_ohms": 88.5
            })
        return routes

    def get_netlist(self) -> dict:
        """
        Builds a netlist representation of connected node clusters.
        """
        parent = {}

        def find(i):
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])
            return parent[i]

        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                parent[root_i] = root_j

        for r in self.active_routes:
            na, nb = r[3], r[4]
            if na not in parent:
                parent[na] = na
            if nb not in parent:
                parent[nb] = nb
            union(na, nb)

        nets_map: Dict[str, List[str]] = {}
        for node in parent:
            root = find(node)
            if root not in nets_map:
                nets_map[root] = []
            nets_map[root].append(node)

        net_list = []
        for idx, (root, nodes) in enumerate(nets_map.items(), start=1):
            net_list.append({
                "net_id": idx,
                "nodes": sorted(nodes)
            })

        return {
            "net_count": len(net_list),
            "nets": net_list
        }
