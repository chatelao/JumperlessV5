# Roadmap: JumperlessV5light

This document outlines the development roadmap for **JumperlessV5light**, focusing on a single-sided breadboard companion matrix powered by a Raspberry Pi Pico 2 (RP2350). The initial phases prioritize delivering a low-cost, pure datamatrix **Minimum Viable Product (MVP)** populated with **1 or 2 CH446Q** analog crosspoint switch ICs.

---

## Progress Overview

| Phase | Description | Status |
| :--- | :--- | :---: |
| **Phase 0: Architecture & System Design** | Core specifications, `CONCEPT.md`, `DESIGN.md`, and CI/CD testing pipeline setup. | ✅ |
| **Phase 1: MVP Datamatrix (1 or 2 CH446Q Switches)** | Pure crosspoint switching MVP hardware & firmware for 1–2 CH446Q chips on single breadboard edge. | 🚧 |
| **Phase 2: Expanded Hardware & Scaled Routing (4 CH446Q Switches)** | Hardware support and routing algorithms expanded to 4 populated CH446Q switches. | ⏳ |
| **Phase 3: Full Array & Advanced Feature Integration (12 CH446Q Switches)** | Complete 12-chip crossbar matrix, OLED/probe extensions, and measurement integration. | ⏳ |

---

## Goals

- 🚧 **MVP Datamatrix Execution:** Deliver a fully functional, low-cost datamatrix MVP operating on 1 or 2 CH446Q ICs.
- ⏳ **Single-Sided Breadboard Compatibility:** Enable direct attachment to one side of standard off-the-shelf breadboards (rows 1–30 / 1–60).
- ⏳ **Pico 2 Core Integration:** Utilize a standard socketed Raspberry Pi Pico 2 board (RP2350) for core system control and ASCII netlist processing.
- ⏳ **Subset Wiring Routing Compatibility:** Maintain 100% netlist format compatibility with Jumperless V5 while handling hardware subset degradation gracefully.

---

## Phases

### Phase 0: Architecture & System Design ✅

- [x] **System Concept & Goals Definition** ✅
  - Document core business cases, single-sided form factor, and Pico 2 host architecture in `CONCEPT.md`.
- [x] **Technical Design & Component Specifications** ✅
  - Define SPI address latching, CLI netlist parser specification, and component interfaces in `DESIGN.md`.
- [x] **CI/CD Test Framework Setup** ✅
  - Establish automated test suite in `test/test_wiring_concept.py` with `test/install.sh` tooling.

---

### Phase 1: MVP Datamatrix (1 or 2 CH446Q Switches) 🚧

Phase 1 delivers the Minimum Viable Product (MVP)—a streamlined, pure software-configurable datamatrix using **1 or 2 CH446Q** crosspoint switches attached to one side of a standard breadboard.

#### 1.1 Hardware Schematic & Unified PCB Design (1 or 2 CH446Q Populated)
- [ ] **1.1.1** Define 1–2 CH446Q schematic footprint and SPI latch addressing lines.
- [ ] **1.1.2** Route single-sided edge header connector for rows 1–14 (1 CH446Q) or 1–28 (2 CH446Q).
- [ ] **1.1.3** Design 3.3V and 5V fixed power rail passthrough traces to breadboard power rails.
- [ ] **1.1.4** Verify 2-layer PCB fabrication layout and Pico 2 DIP socket header pinout.

#### 1.2 Firmware Core & SPI Matrix Driver for 1 or 2 CH446Q Switches
- [ ] **1.2.1** Initialize SPI peripheral (MOSI, SCLK, CS, Strobe) on Pico 2 RP2350 firmware.
- [ ] **1.2.2** Implement `CH446QDriver` low-level crossbar address latching routines for Chip A (and Chip B for 2-chip variant).
- [ ] **1.2.3** Implement shadow matrix state array in RAM for instant delta updates and status dumps.
- [ ] **1.2.4** Implement matrix reset function clearing all crosspoints on populated switches.

#### 1.3 ASCII Command-Line Interface (CLI) & Netlist Parser
- [ ] **1.3.1** Implement USB CDC serial port handler supporting ASCII command stream input.
- [ ] **1.3.2** Integrate netlist parsing engine for Jumperless format: `f {node1-node2, ...}`.
- [ ] **1.3.3** Implement CLI short and long option flags (`-f`/`--file`, `-s`/`--status`, `-r`/`--reset`, `-v`/`--version`, `-h`/`--help`).
- [ ] **1.3.4** Add hardware variant query command (`-m`/`--matrix`) returning populated chip count (1 or 2).

#### 1.4 Subset Routing Engine & Graceful Degradation
- [ ] **1.4.1** Map breadboard top rows 1–7 (Chip A) and 8–14 (Chip B) to matrix X/Y crossbar coordinates.
- [ ] **1.4.2** Implement subset router pathfinding for requested node connections across populated switches (1 or 2 CH446Q).
- [ ] **1.4.3** Implement fallback warning handler for requested nodes exceeding populated switches or requesting omitted measurement hardware (DACs, ADCs, ±8V supplies).

---

### Phase 2: Expanded Hardware & Scaled Routing (4 CH446Q Switches) ⏳

Phase 2 expands the datamatrix capability to **4 CH446Q ICs** (Chips A–D), covering the entire top edge (rows 1–28/30) of a standard breadboard.

- [ ] **2.1 Hardware Expansion to 4 CH446Q ICs** ⏳
  - [ ] **2.1.1** Validate unified PCB layout with 4 CH446Q ICs populated (Chips A, B, C, D).
  - [ ] **2.1.2** Verify power distribution and signal cross-talk across 4-chip crossbar matrix.
- [ ] **2.2 Multi-Chip Routing Algorithm Engine** ⏳
  - [ ] **2.2.1** Extend `MatrixRouter` pathfinding across 4 CH446Q switches (rows 1–28).
  - [ ] **2.2.2** Add multi-hop routing support between non-adjacent switch matrix blocks.
- [ ] **2.3 Persistence & Slot Management** ⏳
  - [ ] **2.3.1** Implement flash-backed netlist slot storage (slots 0–7) accessible via CLI (`-l`/`--load`).

---

### Phase 3: Full Array & Advanced Feature Integration (12 CH446Q Switches) ⏳

Phase 3 achieves complete parity with full Jumperless routing capabilities using all 12 CH446Q ICs, external OLED UI, probe system, and optional measurement expansion.

- [ ] **3.1 Full 12 CH446Q Crossbar Matrix Integration** ⏳
  - [ ] **3.1.1** Populate all 12 CH446Q ICs (Chips A–L) for complete top, bottom, Nano header, and special function routing.
  - [ ] **3.1.2** Integrate Arduino Nano header pin crossbar matrix (Chips I & J).
- [ ] **3.2 Visual Indication & Peripheral Subsystems** ⏳
  - [ ] **3.2.1** Integrate single-wire RGB status LED array driver for visual connection indication.
  - [ ] **3.2.2** Implement TRRRS probe jack sensing and interactive OLED menu navigation.
- [ ] **3.3 Advanced Hardware Option Integration** ⏳
  - [ ] **3.3.1** Add optional ±8V DAC/ADC measurement subsystem module integration.
