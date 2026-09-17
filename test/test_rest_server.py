#!/usr/bin/env python3
"""
Integration tests for REST API Bridge Server
"""

import pytest
import json
from src.rest_server import app, matrix

@pytest.fixture
def client():
    app.config['TESTING'] = True
    matrix.reset_matrix()
    with app.test_client() as client:
        yield client

def test_rest_status(client):
    rv = client.get("/api/v1/status")
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert data["device_id"] == "JUMPERLESS-V5-LIGHT-001"
    assert data["status"] == "READY"

def test_rest_routes_flow(client):
    # GET empty routes
    rv = client.get("/api/v1/routes")
    assert rv.status_code == 200
    assert json.loads(rv.data) == []

    # POST create route
    rv = client.post("/api/v1/routes", json={"node_a": "1", "node_b": "15"})
    assert rv.status_code == 201
    data = json.loads(rv.data)
    assert data["node_a"] == "1"
    assert data["node_b"] == "15"

    # GET active routes
    rv = client.get("/api/v1/routes")
    assert rv.status_code == 200
    routes = json.loads(rv.data)
    assert len(routes) == 1

    # GET nets
    rv = client.get("/api/v1/nets")
    assert rv.status_code == 200
    nets = json.loads(rv.data)
    assert nets["net_count"] == 1

    # DELETE route
    rv = client.delete("/api/v1/routes?node_a=1&node_b=15")
    assert rv.status_code == 200

    # GET empty routes
    rv = client.get("/api/v1/routes")
    assert len(json.loads(rv.data)) == 0

def test_rest_delete_all(client):
    client.post("/api/v1/routes", json={"node_a": "1", "node_b": "2"})
    client.post("/api/v1/routes", json={"node_a": "3", "node_b": "4"})

    rv = client.delete("/api/v1/routes?all=true")
    assert rv.status_code == 200

    rv = client.get("/api/v1/routes")
    assert len(json.loads(rv.data)) == 0
