# Jumperless V5-light Detailed Technical Design

## Architecture Overview

The **Jumperless V5-light** is a minimal hardware/software solution designed to bring programmable matrix crossbar routing to the edge of any standard breadboard.

### Top-Level Architecture Diagram

![Top Architecture](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/Architeuthis-Flux/JumperlessV5/main/TOP_ARCHITECTURE.puml)
*Source file: [TOP_ARCHITECTURE.puml](TOP_ARCHITECTURE.puml)*

---

## Detailed System Component Design

```
                     +---------------------------------+
                     |     USB Host Interface          |
                     +---------------------------------+
                                     | USB CDC
                                     v
                     +---------------------------------+
                     |   RP2350 Microcontroller        |
                     |  - Core 0: CLI / REST Gateway   |
                     |  - Core 1: Matrix Router Logic  |
                     |  - PIO0: CH446Q Address/Strobe  |
                     +---------------------------------+
                        /           |           \
                       /            |            \
       +--------------+     +---------------+     +------------------+
       | CH446Q #1    |     | Power Rail    |     | Voltage Sensing  |
       | 16x8 Switch  |     | Controller    |     | (RP2350 ADC)     |
       +--------------+     +---------------+     +------------------+
              \                     |                     /
               +--------------------+--------------------+
                                    |
                                    v
                     +---------------------------------+
                     | Breadboard Border Edge Header   |
                     | (2.54mm Pitch Pin Strip)        |
                     +---------------------------------+
```

### 1. Control & Processing Subsystem (RP2350)
- **CPU Allocation**:
  - Core 0 runs the asynchronous communication task (USB CDC virtual COM port, CLI parser, and REST endpoint handler).
  - Core 1 executes matrix state resolution, netlist parsing, and real-time voltage/continuity polling.
- **PIO State Machine (PIO0)**:
  - Generates parallel address bits ($X_0-X_3$, $Y_0-Y_2$), Data bit, and Strobe pulses to drive CH446Q arrays without CPU blocking.
  - Pulse width: $T_{strobe} \ge 25\text{ ns}$.

### 2. CH446Q Analog Switch Matrix
- **Matrix Array Topology**:
  - Standard configuration utilizes 2 × CH446Q ICs tied together on common Y-bus lines, creating a 32-node X-axis to 8-node Y-axis bus matrix ($32 \times 8$).
  - Allows routing between any of the 32 breadboard edge tie-points.
- **Overdrive & Level Shifting**:
  - Powered by LT1054 charge-pump array generating $+8\text{V}$ ($V_{DD}$) and $-8\text{V}$ ($V_{SS}$).
  - Signal limits: $-8\text{V} \le V_{signal} \le +8\text{V}$.
  - Switch resistance: $R_{ON} \approx 45\ \Omega$ per switch ($90\ \Omega$ per two-stage crossbar connection).

### 3. Power Management & Rail Generation
- **Primary Input**: USB-C 5V supply ($V_{BUS}$, up to 500 mA).
- **Secondary Rails**:
  - $V_{3V3}$: 3.3V LDO for RP2350 microcontroller and digital logic.
  - $+8\text{V}$ / $-8\text{V}$: Switched charge-pump boost rails powering CH446Q matrix switches.
  - Programmable Rails: MCP4728 12-bit DAC buffered by op-amps delivering variable $+1.2\text{V}$ to $+8.0\text{V}$ and $-1.2\text{V}$ to $-8.0\text{V}$.

### 4. Technical Interfaces

#### A. Command Line Interface (CLI)
- Protocol: Human-readable serial terminal interface over USB CDC.
- Option Formats: All options support both short and long form flags (e.g., `-c` / `--connect`, `-d` / `--disconnect`, `-l` / `--list`, `-s` / `--status`, `-r` / `--reset`, `-h` / `--help`).
- Example command string:
  ```bash
  v5light -c "1-15,TOP_RAIL-5"
  ```

#### B. REST API Interface
- Protocol: JSON-over-HTTP / WebSocket or USB serial JSON frame bridge.
- OpenAPI specification defined in `api/openapi.yaml`.
- Key Endpoints:
  - `GET /api/v1/status`: Device hardware health, voltage rails, active connections.
  - `POST /api/v1/routes`: Connect two or more nodes.
  - `DELETE /api/v1/routes`: Clear specified routes or reset crossbar matrix.
  - `GET /api/v1/nets`: Retrieve current netlist.

---

## Summary of Technical Alternatives and Decisions

For each major technological choice in the design phase, three alternatives were evaluated. The selected option and discarded alternatives are summarized below:

### 1. Matrix Control Driver Mechanism
- **Alternative A (Chosen)**: **RP2350 PIO State Machine Assembly Code**
  - *Rationale*: Low latency (<1 µs setup time), deterministic timing guarantees, and zero core CPU overhead during switch updates.
- **Alternative B (Discarded)**: GPIO Bit-Banging from CPU Core
  - *Reason for rejection*: Susceptible to interrupts, higher latency, and wastes main CPU core cycles during serial address transmission.
- **Alternative C (Discarded)**: External I2C / SPI GPIO Expander (e.g. MCP23S17)
  - *Reason for rejection*: SPI/I2C propagation delays slow down crossbar reconfigurations significantly.

### 2. Software Communication Protocol Structure
- **Alternative A (Chosen)**: **Unified Dual-Mode (CLI + REST/JSON) Protocol over USB CDC**
  - *Rationale*: CLI provides immediate interactive manual control for engineers; REST/JSON enables easy script automation and web application integration.
- **Alternative B (Discarded)**: Raw Binary Serial Protocol
  - *Reason for rejection*: Harder to debug manually, lacks direct human readability.
- **Alternative C (Discarded)**: Pure WebSockets / Wi-Fi Bridge
  - *Reason for rejection*: Requires additional wireless microcontroller module (increasing power and board size) not needed for basic wired breadboard testing.

### 3. Firmware Build & Test Stack
- **Alternative A (Chosen)**: **Python Gateway / Native Driver Core with Pytest Test Suite**
  - *Rationale*: Allows rapid cross-platform deployment, automated unit/integration testing on CI/CD pipelines, and standalone deployment.
- **Alternative B (Discarded)**: Bare-Metal C-Only Stack with Custom Toolchain
  - *Reason for rejection*: Less flexible for REST/CLI API wrapper distribution on host side.
- **Alternative C (Discarded)**: Arduino Framework Monolith
  - *Reason for rejection*: Higher build overhead, complex dependency locking, and less suited for automated host-side CI/CD testing.
