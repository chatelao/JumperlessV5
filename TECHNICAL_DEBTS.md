# Jumperless V5-light Technical Debts Log

This document tracks known technical debts, legacy component constraints, security considerations, and potential future optimizations for the **Jumperless V5-light** project.

*Note: Per project policy, items in this log are documented for visibility and tracking but are not to be refactored or fixed until explicitly requested.*

---

## 1. Hardware & Physical Constraints

### TD-01: Crosspoint Switch On-Resistance ($R_{ON}$)
- **Description**: The CH446Q CMOS crosspoint switches have an internal on-resistance of $\sim 45\ \Omega$ per switch channel. A two-stage path through X-Y-X crossbar arrays results in $\sim 90\ \Omega$ total path resistance.
- **Impact**: High-current paths (e.g., >50 mA powering heavy loads) experience minor voltage drop across the switch.
- **Potential Resolution**: Future hardware iterations may explore discrete low-$R_{ON}$ MOSFET matrices or dedicated high-current bypass relays.

### TD-02: Maximum Analog Voltage Swing Limits
- **Description**: The CH446Q switch array operates within $\pm 8\text{V}$ or $\pm 9\text{V}$ overdrive limits. Voltages exceeding $+9\text{V}$ or $-9\text{V}$ will forward-bias ESD protection diodes.
- **Impact**: Users connecting higher voltage sources (e.g. 12V / 24V industrial rails) risk damaging the crosspoint IC.
- **Potential Resolution**: Add input overvoltage protection clamp diodes and inline current-limiting resistors on breadboard interface pins.

---

## 2. Firmware & Software Architecture

### TD-03: USB CDC Buffer Saturation Under High Output Rates
- **Description**: Continuous high-frequency ADC streaming over serial CDC without flow control can saturate host USB buffers.
- **Impact**: Potential dropped packets during high-speed oscilloscope data streaming.
- **Potential Resolution**: Implement hardware flow control or a double-buffered ring buffer with dynamic batching in the firmware communication stack.

### TD-04: Basic Authentication on Local REST API Bridge
- **Description**: The REST API bridge server operating over local serial/loopback currently operates without explicit authentication tokens or API key checks.
- **Impact**: Any local application on the host machine can send route commands if the port is exposed.
- **Potential Resolution**: Introduce optional local token-based header authentication (`X-API-Key`) for HTTP endpoints.

---

## 3. Tooling & Packaging

### TD-05: Single-Threaded Test Script Runner
- **Description**: The automated test suite in `/test/` runs sequentially.
- **Impact**: Test execution time may increase as additional hardware matrix test cases are appended.
- **Potential Resolution**: Refactor test suite execution to use `pytest -n auto` parallel test invocation.
