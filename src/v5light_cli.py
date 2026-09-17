#!/usr/bin/env python3
"""
Command Line Interface (CLI) for Jumperless V5-light.
Supports short and long form options for all commands.
"""

import argparse
import sys
import json
from typing import List, Optional
from src.ch446q_matrix import CH446QMatrix

# Shared matrix instance for local CLI execution / test mock
global_matrix = CH446QMatrix()

def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="v5light",
        description="Jumperless V5-light CLI Controller - software jumpering for standard breadboards",
        add_help=True
    )

    parser.add_argument(
        "-c", "--connect",
        type=str,
        help="Connect two nodes (e.g. '1-15' or 'TOP_RAIL,5')"
    )

    parser.add_argument(
        "-d", "--disconnect",
        type=str,
        help="Disconnect two nodes (e.g. '1-15')"
    )

    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List all active crosspoint routes"
    )

    parser.add_argument(
        "-n", "--nets",
        action="store_true",
        help="Display active netlist clusters"
    )

    parser.add_argument(
        "-s", "--status",
        action="store_true",
        help="Query V5-light board health and rail voltage telemetry"
    )

    parser.add_argument(
        "-r", "--reset",
        action="store_true",
        help="Reset/clear all matrix switch connections"
    )

    parser.add_argument(
        "-p", "--port",
        type=str,
        default="/dev/ttyACM0",
        help="Serial port path for Jumperless V5-light (default: /dev/ttyACM0)"
    )

    parser.add_argument(
        "-b", "--baud",
        type=int,
        default=115200,
        help="Baud rate for serial communication (default: 115200)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output logging"
    )

    return parser.parse_args(args)


def run_cli(args: argparse.Namespace, matrix: Optional[CH446QMatrix] = None) -> int:
    m = matrix if matrix is not None else global_matrix

    if args.status:
        status_info = {
            "device_id": "JUMPERLESS-V5-LIGHT-001",
            "firmware_version": "1.0.0-light",
            "status": "READY",
            "active_routes_count": len(m.get_active_routes()),
            "power_rails": {
                "vplus_volts": 5.0,
                "vminus_volts": -5.0,
                "vbus_volts": 5.02
            }
        }
        print(json.dumps(status_info, indent=2))
        return 0

    if args.connect:
        raw = args.connect.replace("-", ",").split(",")
        if len(raw) != 2:
            print(f"Error: Connect specifier must contain exactly two nodes, got '{args.connect}'", file=sys.stderr)
            return 1
        node_a, node_b = raw[0].strip(), raw[1].strip()
        try:
            res = m.connect(node_a, node_b)
            print(f"Connected {node_a} <--> {node_b} on CH446Q Chip #{res['chip_id']}")
        except ValueError as err:
            print(f"Error connecting nodes: {err}", file=sys.stderr)
            return 1
        return 0

    if args.disconnect:
        raw = args.disconnect.replace("-", ",").split(",")
        if len(raw) != 2:
            print(f"Error: Disconnect specifier must contain exactly two nodes, got '{args.disconnect}'", file=sys.stderr)
            return 1
        node_a, node_b = raw[0].strip(), raw[1].strip()
        success = m.disconnect(node_a, node_b)
        if success:
            print(f"Disconnected {node_a} <--> {node_b}")
        else:
            print(f"No active route found between {node_a} and {node_b}", file=sys.stderr)
            return 1
        return 0

    if args.reset:
        cleared = m.reset_matrix()
        print(f"Cleared {cleared} active crosspoint routes. Matrix reset complete.")
        return 0

    if args.list:
        routes = m.get_active_routes()
        print(json.dumps(routes, indent=2))
        return 0

    if args.nets:
        netlist = m.get_netlist()
        print(json.dumps(netlist, indent=2))
        return 0

    # Default action if no flags provided
    print("Jumperless V5-light CLI Controller v1.0.0-light. Use -h or --help for available options.")
    return 0


def main():
    parsed = parse_args()
    sys.exit(run_cli(parsed))


if __name__ == "__main__":
    main()
