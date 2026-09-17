#!/usr/bin/env python3
"""
Unit tests for CH446Q Matrix Routing Module
"""

import pytest
from src.ch446q_matrix import CH446QMatrix

def test_matrix_init():
    m = CH446QMatrix()
    assert len(m.get_active_routes()) == 0
    assert m.get_netlist()["net_count"] == 0

def test_node_resolution():
    m = CH446QMatrix()
    chip_id, addr = m._resolve_node("1")
    assert chip_id == 0
    assert addr == 0

    chip_id, addr = m._resolve_node("17")
    assert chip_id == 1
    assert addr == 0

    chip_id, addr = m._resolve_node("TOP_RAIL")
    assert chip_id == 0
    assert addr == 7

def test_connect_and_disconnect():
    m = CH446QMatrix()
    res = m.connect("1", "15")
    assert res["status"] == "CONNECTED"
    assert len(m.get_active_routes()) == 1

    netlist = m.get_netlist()
    assert netlist["net_count"] == 1
    assert "1" in netlist["nets"][0]["nodes"]
    assert "15" in netlist["nets"][0]["nodes"]

    success = m.disconnect("1", "15")
    assert success is True
    assert len(m.get_active_routes()) == 0

def test_special_nodes():
    m = CH446QMatrix()
    res = m.connect("TOP_RAIL", "5")
    assert res["node_a"] == "TOP_RAIL"
    assert res["node_b"] == "5"

def test_invalid_nodes():
    m = CH446QMatrix()
    with pytest.raises(ValueError):
        m.connect("1", "1")

    with pytest.raises(ValueError):
        m.connect("999", "1")

def test_matrix_reset():
    m = CH446QMatrix()
    m.connect("1", "2")
    m.connect("3", "4")
    assert len(m.get_active_routes()) == 2
    cleared = m.reset_matrix()
    assert cleared == 2
    assert len(m.get_active_routes()) == 0
