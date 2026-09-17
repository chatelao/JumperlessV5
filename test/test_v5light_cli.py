#!/usr/bin/env python3
"""
Integration tests for V5-light Command Line Interface (CLI)
Verifies that all options support both short and long form flags.
"""

import pytest
from src.v5light_cli import parse_args, run_cli
from src.ch446q_matrix import CH446QMatrix

def test_cli_help_flags():
    # argparse handles -h/--help by throwing SystemExit(0)
    with pytest.raises(SystemExit) as exc_info:
        parse_args(["-h"])
    assert exc_info.value.code == 0

    with pytest.raises(SystemExit) as exc_info:
        parse_args(["--help"])
    assert exc_info.value.code == 0

def test_cli_connect_short_and_long():
    m = CH446QMatrix()
    args_short = parse_args(["-c", "1-10"])
    assert args_short.connect == "1-10"
    ret = run_cli(args_short, matrix=m)
    assert ret == 0
    assert len(m.get_active_routes()) == 1

    args_long = parse_args(["--connect", "11-20"])
    assert args_long.connect == "11-20"
    ret = run_cli(args_long, matrix=m)
    assert ret == 0
    assert len(m.get_active_routes()) == 2

def test_cli_disconnect_short_and_long():
    m = CH446QMatrix()
    m.connect("1", "10")
    args_short = parse_args(["-d", "1-10"])
    ret = run_cli(args_short, matrix=m)
    assert ret == 0
    assert len(m.get_active_routes()) == 0

    m.connect("11", "20")
    args_long = parse_args(["--disconnect", "11-20"])
    ret = run_cli(args_long, matrix=m)
    assert ret == 0
    assert len(m.get_active_routes()) == 0

def test_cli_list_short_and_long(capsys):
    m = CH446QMatrix()
    m.connect("1", "10")

    args_short = parse_args(["-l"])
    run_cli(args_short, matrix=m)
    out_short = capsys.readouterr().out
    assert "route_1_10" in out_short

    args_long = parse_args(["--list"])
    run_cli(args_long, matrix=m)
    out_long = capsys.readouterr().out
    assert "route_1_10" in out_long

def test_cli_nets_short_and_long(capsys):
    m = CH446QMatrix()
    m.connect("1", "10")

    args_short = parse_args(["-n"])
    run_cli(args_short, matrix=m)
    out_short = capsys.readouterr().out
    assert "net_count" in out_short

    args_long = parse_args(["--nets"])
    run_cli(args_long, matrix=m)
    out_long = capsys.readouterr().out
    assert "net_count" in out_long

def test_cli_status_short_and_long(capsys):
    m = CH446QMatrix()
    args_short = parse_args(["-s"])
    run_cli(args_short, matrix=m)
    out_short = capsys.readouterr().out
    assert "JUMPERLESS-V5-LIGHT-001" in out_short

    args_long = parse_args(["--status"])
    run_cli(args_long, matrix=m)
    out_long = capsys.readouterr().out
    assert "JUMPERLESS-V5-LIGHT-001" in out_long

def test_cli_reset_short_and_long(capsys):
    m = CH446QMatrix()
    m.connect("1", "2")
    args_short = parse_args(["-r"])
    run_cli(args_short, matrix=m)
    assert len(m.get_active_routes()) == 0

    m.connect("3", "4")
    args_long = parse_args(["--reset"])
    run_cli(args_long, matrix=m)
    assert len(m.get_active_routes()) == 0

def test_cli_port_and_baud():
    args = parse_args(["-p", "/dev/ttyUSB0", "-b", "9600", "-v"])
    assert args.port == "/dev/ttyUSB0"
    assert args.baud == 9600
    assert args.verbose is True

    args_long = parse_args(["--port", "/dev/ttyUSB1", "--baud", "57600", "--verbose"])
    assert args_long.port == "/dev/ttyUSB1"
    assert args_long.baud == 57600
    assert args_long.verbose is True
