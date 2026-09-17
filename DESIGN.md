# Detailed Design: JumperlessV5light

## System Architecture Overview

`JumperlessV5light` is a modular, single-sided companion system that connects directly to one side of a standard off-the-shelf breadboard. It derives its requirements and functional goals from `CONCEPT.md` and `GEMINI.md`.

The system architecture focuses on delivering a low-cost, high-reliability software-configurable analog crosspoint matrix (pure datamatrix MVP) powered by a socketed **Raspberry Pi Pico 2** microcontroller board (RP2350).

### Architecture Diagram

![Top Level Architecture](TOP_ARCHITECTURE.puml)

```
 +---------------------------------------------------------------------------------+
 |                           JumperlessV5light Architecture                        |
 |                                                                                 |
 |  +------------------------------------+      +-------------------------------+  |
 |  |  Raspberry Pi Pico 2 (RP2350 MCU)  | SPI  |  CH446Q Crosspoint Matrix     |  |
 |  |  - C++ / PlatformIO Firmware Core   |----->|  (1, 2, 4, or 12 Populated)   |  |
 |  |  - USB CDC CLI Parser              |      |  - Analog Switches (±9V VDD)  |  |
 |  +------------------------------------+      +-------------------------------+  |
 |                    |                                       |                    |
 |          Power Bus |                                       | Crosspoint         |
 |        Passthrough | (3.3V/5V)                             | Signals            |
 |                    v                                       v                    |
 |  +------------------------------------+      +-------------------------------+  |
 |  |  Power Distribution Subsystem      |      |  Single-Sided Edge Header     |  |
 |  |  (3.3V & 5V Rail Routing)          |      |  (Rows 1–30/1–60 + Nano Pins) |  |
 |  +------------------------------------+      +-------------------------------+  |
 +---------------------------------------------------------------------------------+
                                                                |
                                                                v
                                                   +--------------------------+
                                                   | Standard Breadboard      |
                                                   | (One-Sided Connection)   |
                                                   +--------------------------+
```

---

## Tech Stack Definition

The technological stack for development, build, execution, and testing of `JumperlessV5light` is defined as follows:

| Layer | Technology Selected | Justification / Role |
| :--- | :--- | :--- |
| **Microcontroller Host** | Raspberry Pi Pico 2 (RP2350 Dual Arm Cortex-M33 / Hazard3 RISC-V) | Standard DIP module interface; easily swappable, low assembly cost, high RAM/Flash capacity. |
| **Firmware Framework** | C++20 / Pico SDK / PlatformIO | Native performance, tight peripheral timing control, seamless integration with existing JumperlOS codebase. |
| **Matrix Crosspoint IC** | WCH CH446Q (16x8 High-Speed Analog Crosspoint Switch Array) | Proven ±9V signal range support, 50MHz bandwidth, high density matrix switching. |
| **Hardware Control Bus** | Dedicated SPI / GPIO Latch Address Bus | Fast, deterministic crossbar address bit programming for array scaling (1, 2, 4, or 12 ICs). |
| **CLI & Netlist Parser** | USB CDC Serial (ASCII Command Line Interface) | Standardized human-readable netlist syntax (`f {node1-node2, ...}`); platform-agnostic host tool compatibility. |
| **Build & Test Infrastructure** | PlatformIO CLI, Pytest (`test/`), Bash Tooling (`src/install.sh`, `test/install.sh`) | Fully automated local and CI/CD workflow verification without external proprietary dependencies. |

---

## Major Technical Choices & Evaluation

To ensure rigorous architectural discipline, every major technical choice was evaluated against three distinct alternatives.

### Choice 1: Firmware Development Framework & Build Tooling

- **Alternative 1 (MicroPython Core Runtime):** Execute firmware directly as MicroPython scripts running on an onboard interpreter.
- **Alternative 2 (C++ / Pico SDK with PlatformIO Engine) [SELECTED]:** Standardize on C++ embedded codebase compiled via PlatformIO using the official Raspberry Pi Pico SDK.
- **Alternative 3 (Arduino Core for Pico):** Use Arduino IDE framework wrapper over Pico SDK.

#### Justification for Alternative 2 (Selected)
C++ with PlatformIO provides optimal real-time performance for matrix address latching, direct control over SPI hardware DMA, precise hardware abstraction layer (HAL) reuse from JumperlOS, and robust headless CI/CD build integration through `platformio.ini`.

---

### Choice 2: Matrix Bus Addressing & Demuxing Architecture

- **Alternative 1 (Direct Individual Chip Select Lines per CH446Q):** Dedicated GPIO chip-select line routed from Pico 2 to every single CH446Q switch on the board.
- **Alternative 2 (Shared SPI Bus with Shift-Register Address Latches) [SELECTED]:** High-speed SPI bus feeding shift register latches (e.g., 74HC595 / CD4028) to select matrix ICs and output crossbar coordinates (X0-X15, Y0-Y7, Data, Strobe).
- **Alternative 3 (I2C Bus Expander Control):** Control matrix switches using external I2C GPIO expanders (e.g., MCP23017).

#### Justification for Alternative 2 (Selected)
A shared SPI bus with shift-register latches drastically minimizes Pico 2 GPIO pin consumption while maintaining microsecond-level address setup times. I2C (Alternative 3) was discarded due to high bus latency during multi-chip matrix reconfigurations. Dedicated CS lines (Alternative 1) scale poorly as switch count increases to 12 ICs.

---

### Choice 3: Command-Line Interface (CLI) & Netlist Parser Architecture

- **Alternative 1 (Binary Protocol / Protocol Buffers over Serial):** Enforce a binary byte-packed serial frame protocol for netlist updates.
- **Alternative 2 (Human-Readable ASCII Command Engine with Short/Long Flag Support) [SELECTED]:** Maintain standard Jumperless human-readable ASCII netlist parser (`f {node1-node2}`) enhanced with both short (`-f`, `-s`, `-r`) and long (`--file`, `--status`, `--reset`) CLI options.
- **Alternative 3 (REST API Gateway Server over Wi-Fi / WebSockets):** Run an HTTP REST server directly on host PC or MCU to route netlists via JSON payloads.

#### Justification for Alternative 2 (Selected)
Human-readable ASCII CLI interface with dual short/long parameter formatting allows instant interactive debugging from any serial terminal (PuTTY, screen, minicom) without requiring specialized client software, while maintaining 100% backward compatibility with existing Jumperless toolchains.

---

## Technical Component Architecture & Interfaces

### Component Specifications

```
 +---------------------------------------------------------------------------------+
 |                             Detailed Technical Interface                        |
 |                                                                                 |
 |   +------------------------+      SPI Bus        +--------------------------+   |
 |   |  Pico 2 Core (RP2350)  |-------------------->| Shift Latch Matrix Driver|   |
 |   |  - GPIO 16 (MOSI)      |  (SCLK, MOSI, CS)   | - 74HC595 Address Latch  |   |
 |   |  - GPIO 18 (SCLK)      |                     +--------------------------+   |
 |   |  - GPIO 17 (CS)        |                                  |                 |
 |   |  - GPIO 19 (Strobe)    |                                  | X/Y Address     |
 |   +------------------------+                                  v                 |
 |                |                                 +--------------------------+   |
 |   USB CDC      | USB Serial CLI                  | CH446Q Crosspoint Switch |   |
 |   Interface    v                                 | (1, 2, 4, or 12 Array)   |   |
 |   +------------------------+                     +--------------------------+   |
 |   | ASCII Command Engine   |                                  |                 |
 |   | - Netlist Parsing      |                                  | Analog Nets     |
 |   | - Subset Matrix Router |                                  v                 |
 |   +------------------------+                     +--------------------------+   |
 |                                                  | Breadboard Edge Header   |   |
 |                                                  | (Target Single Side)     |   |
 |                                                  +--------------------------+   |
 +---------------------------------------------------------------------------------+
```

#### 1. Microcontroller Core Component (`src/main.cpp`, `lib/MatrixRouter`)
- **Technical Responsibilities:**
  - Ingests CLI netlist string payloads over USB CDC serial.
  - Computes pathfinding across populated CH446Q switches (1, 2, 4, or 12 IC configurations).
  - Handles subset degradation gracefully: when requested node pairs exceed populated switch capabilities or request omitted measurement hardware (e.g., ADCs/DACs), issues clear warnings over serial CLI.
  - Controls SPI address shift registers and Strobe/Reset lines.
- **Technical Interfaces:**
  - `USB_CDC_Read(uint8_t* buffer, size_t len)`
  - `SPI_Write_Crossbar_Address(uint8_t chip_id, uint8_t x_addr, uint8_t y_addr, bool state)`
  - `Router_Compute_Netlist(const char* netlist_str, MatrixConfig_t config)`

#### 2. Matrix Switching Network Component (`lib/CH446QDriver`)
- **Technical Responsibilities:**
  - Interfaces directly to CH446Q hardware pins (X0–X15, Y0–Y7, DATA, ADDRESS 0–3, STROBE, RESET).
  - Maintains shadow matrix state in RAM to enable delta updates and instantaneous state dump.
- **Technical Interfaces:**
  - `CH446Q_SetConnection(uint8_t chip_idx, uint8_t x, uint8_t y)`
  - `CH446Q_ClearConnection(uint8_t chip_idx, uint8_t x, uint8_t y)`
  - `CH446Q_ResetAll()`

#### 3. Power Rail & Single-Side Header Component
- **Technical Responsibilities:**
  - Distributes 3.3V VCC and 5V USB power directly to breadboard outer power rails.
  - Pin-header interface bridges matrix X/Y lines to rows 1–30 / 1–60 on target breadboard edge.

---

## Command-Line Interface (CLI) Technical Specification

The JumperlessV5light CLI provides full control over matrix state, netlist loading, status queries, and board diagnostic routines. In accordance with project standards, every option supports both **short** and **long** flag formats.

### Command Structure

```bash
jumperless-cli [SHORT_OPTION | LONG_OPTION] [ARGUMENT]
```

### CLI Option Reference

| Short Option | Long Option | Description | Example Usage |
| :--- | :--- | :--- | :--- |
| `-f <netlist>` | `--file <netlist>` | Parses and applies a netlist connection string. | `jumperless-cli -f "f {1-10, 15-20}"` |
| `-s` | `--status` | Queries current populated matrix switch status and active netlist. | `jumperless-cli --status` |
| `-r` | `--reset` | Clears all active crosspoint connections across all switches. | `jumperless-cli -r` |
| `-v` | `--version` | Displays system firmware version, hardware variant, and chip count. | `jumperless-cli --version` |
| `-h` | `--help` | Outputs CLI command usage help summary. | `jumperless-cli -h` |
| `-l <slot>` | `--load <slot>` | Loads stored netlist from onboard flash slot index (0–7). | `jumperless-cli -l 2` |
| `-m <count>` | `--matrix <count>` | Configures or queries populated switch count (1, 2, 4, or 12). | `jumperless-cli -m 4` |

---

## Summary of Discarded Alternatives

### 1. Discarded Development Framework Options
- **MicroPython Core Runtime (Choice 1, Alt 1):** Discarded due to non-deterministic execution timing, higher RAM footprint, and inability to maintain microsecond-level matrix latch timing without lower-level C extensions.
- **Arduino Core Wrapper (Choice 1, Alt 3):** Discarded due to redundant abstraction overhead and sub-optimal hardware SPI DMA performance compared to native Pico SDK / PlatformIO C++ implementations.

### 2. Discarded Addressing Architecture Options
- **Direct Individual Chip Select Lines (Choice 2, Alt 1):** Discarded due to excessive Pico 2 GPIO pin consumption, limiting scalability across 1, 2, 4, and 12 chip variants.
- **I2C Bus Expander Control (Choice 2, Alt 3):** Discarded due to severe I2C clock speed limitations resulting in slow multi-switch netlist refresh rates.

### 3. Discarded Interface Options
- **Binary Frame Protocol (Choice 3, Alt 1):** Discarded because it prevents raw human interaction via standard serial terminals without dedicated desktop middleware.
- **REST Gateway Server over WebSockets (Choice 3, Alt 3):** Discarded as unnecessary overhead for Phase 1 MVP datamatrix operation, increasing memory footprint and latency.
