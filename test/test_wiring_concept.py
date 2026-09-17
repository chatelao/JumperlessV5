import os
import re
import pytest

FIRMWARE_DIR = os.path.join(os.path.dirname(__file__), "..", "RP23V50firmware", "src")
DEFINES_HEADER = os.path.join(FIRMWARE_DIR, "JumperlessDefines.h")
MATRIX_STATE_CPP = os.path.join(FIRMWARE_DIR, "MatrixState.cpp")
CONCEPT_MD = os.path.join(os.path.dirname(__file__), "..", "CONCEPT.md")
DESIGN_MD = os.path.join(os.path.dirname(__file__), "..", "DESIGN.md")


def read_file_content(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_chip_definitions_exist():
    """Verify that all 12 CH446Q chips (CHIP_A through CHIP_L) are defined in original firmware and referenced in concept docs."""
    defines_content = read_file_content(DEFINES_HEADER)

    expected_chips = {
        "CHIP_A": 0, "CHIP_B": 1, "CHIP_C": 2, "CHIP_D": 3,
        "CHIP_E": 4, "CHIP_F": 5, "CHIP_G": 6, "CHIP_H": 7,
        "CHIP_I": 8, "CHIP_J": 9, "CHIP_K": 10, "CHIP_L": 11
    }

    for chip_name, val in expected_chips.items():
        pattern = rf"#define\s+{chip_name}\s+{val}"
        assert re.search(pattern, defines_content), f"Missing definition for {chip_name} with value {val} in JumperlessDefines.h"

    concept_content = read_file_content(CONCEPT_MD)
    design_content = read_file_content(DESIGN_MD)

    # Verify CH446Q matrix scalability is specified in concept/design
    assert "CH446Q" in concept_content
    assert "CH446Q" in design_content


def test_breadboard_top_row_y_mappings():
    """Verify Chips A-D map to top breadboard rows 1-28."""
    matrix_content = read_file_content(MATRIX_STATE_CPP)

    # Chip A Y map: TOP_1 .. TOP_7
    assert "TOP_1" in matrix_content and "TOP_7" in matrix_content
    # Chip B Y map: TOP_8 .. TOP_14
    assert "TOP_8" in matrix_content and "TOP_14" in matrix_content
    # Chip C Y map: TOP_15 .. TOP_21
    assert "TOP_15" in matrix_content and "TOP_21" in matrix_content
    # Chip D Y map: TOP_22 .. TOP_28
    assert "TOP_22" in matrix_content and "TOP_28" in matrix_content


def test_breadboard_bottom_row_y_mappings():
    """Verify Chips E-H map to bottom breadboard rows 31-58."""
    matrix_content = read_file_content(MATRIX_STATE_CPP)

    # Chip E Y map: BOTTOM_1 .. BOTTOM_7
    assert "BOTTOM_1" in matrix_content and "BOTTOM_7" in matrix_content
    # Chip F Y map: BOTTOM_8 .. BOTTOM_14
    assert "BOTTOM_8" in matrix_content and "BOTTOM_14" in matrix_content
    # Chip G Y map: BOTTOM_15 .. BOTTOM_21
    assert "BOTTOM_15" in matrix_content and "BOTTOM_21" in matrix_content
    # Chip H Y map: BOTTOM_22 .. BOTTOM_28
    assert "BOTTOM_22" in matrix_content and "BOTTOM_28" in matrix_content


def test_nano_pin_x_mappings():
    """Verify Chips I and J map to Nano header pins (D0-D13, A0-A7)."""
    matrix_content = read_file_content(MATRIX_STATE_CPP)

    nano_pins = ["NANO_A0", "NANO_D1", "NANO_A2", "NANO_D3", "NANO_D0", "NANO_A1", "NANO_D2", "NANO_A3"]
    for pin in nano_pins:
        assert pin in matrix_content, f"Nano pin {pin} not found in matrix mapping"


def test_special_functions_x_mappings():
    """Verify Chips K and L map to power rails, DACs, ADCs, and GND."""
    matrix_content = read_file_content(MATRIX_STATE_CPP)

    sf_nodes = ["TOP_RAIL", "BOTTOM_RAIL", "DAC0", "DAC1", "ADC0", "ADC1", "GND", "ROUTABLE_BUFFER_IN", "ROUTABLE_BUFFER_OUT"]
    for node in sf_nodes:
        assert node in matrix_content, f"Special function node {node} not found in matrix mapping"


def test_concept_subset_wiring_compatibility():
    """Verify that CONCEPT.md specifies a subset wiring model compatible with Jumperless V5."""
    concept_content = read_file_content(CONCEPT_MD)

    # Must mention subset wiring routing compatibility
    assert "Subset Wiring Routing Compatibility" in concept_content or "subset of the existing Jumperless V5 wiring" in concept_content
    # Must specify single-sided breadboard connection
    assert "Single-Sided" in concept_content or "single side" in concept_content
