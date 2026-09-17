#!/usr/bin/env python3
"""
REST API Bridge Server for Jumperless V5-light.
Exposes endpoints matching api/openapi.yaml for web UIs and remote scripts.
"""

from flask import Flask, jsonify, request
from src.ch446q_matrix import CH446QMatrix

app = Flask(__name__)
matrix = CH446QMatrix()

@app.route("/api/v1/status", methods=["GET"])
def get_status():
    return jsonify({
        "device_id": "JUMPERLESS-V5-LIGHT-001",
        "firmware_version": "1.0.0-light",
        "status": "READY",
        "active_routes_count": len(matrix.get_active_routes()),
        "power_rails": {
            "vplus_volts": 5.0,
            "vminus_volts": -5.0,
            "vbus_volts": 5.02
        }
    }), 200

@app.route("/api/v1/routes", methods=["GET"])
def get_routes():
    return jsonify(matrix.get_active_routes()), 200

@app.route("/api/v1/routes", methods=["POST"])
def create_route():
    data = request.get_json(force=True, silent=True) or {}
    node_a = data.get("node_a")
    node_b = data.get("node_b")

    if not node_a or not node_b:
        return jsonify({
            "code": 400,
            "error": "Request body must contain 'node_a' and 'node_b'"
        }), 400

    try:
        route_info = matrix.connect(node_a, node_b)
        return jsonify(route_info), 201
    except ValueError as e:
        return jsonify({
            "code": 400,
            "error": str(e)
        }), 400

@app.route("/api/v1/routes", methods=["DELETE"])
def delete_routes():
    if request.args.get("all", "").lower() == "true":
        count = matrix.reset_matrix()
        return jsonify({"message": f"Cleared all {count} routes"}), 200

    node_a = request.args.get("node_a")
    node_b = request.args.get("node_b")

    if not node_a or not node_b:
        return jsonify({
            "code": 400,
            "error": "Query params 'node_a' and 'node_b' required (or 'all=true')"
        }), 400

    removed = matrix.disconnect(node_a, node_b)
    if removed:
        return jsonify({"message": f"Route between {node_a} and {node_b} disconnected"}), 200
    else:
        return jsonify({
            "code": 404,
            "error": f"No active route found between {node_a} and {node_b}"
        }), 404

@app.route("/api/v1/nets", methods=["GET"])
def get_nets():
    return jsonify(matrix.get_netlist()), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
