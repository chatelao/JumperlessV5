# Concept: JumperlessV5light

## Goal & Product Overview

The primary goal of **JumperlessV5light** is to deliver a lighter, more accessible, and modular version of the Jumperless hardware prototyping system designed to attach directly to one side of an existing standard breadboard.

JumperlessV5light simplifies hardware complexity and manufacturing costs while preserving core jumperless software-defined routing capabilities.

### Key Objectives
- **Single-Sided Attachment:** Connect seamlessly to one side (e.g., top/bottom rows 1–30 or 1–60) of a standard off-the-shelf breadboard without requiring custom replacement spring clip shells.
- **Microcontroller Core:** Replace the onboard surface-mount RP2350 IC with a standard, removable **Raspberry Pi Pico 2** microcontroller board.
- **Modular Matrix Scaling:** Support hardware variants populated with **1, 4, or all (12) CH446Q** analog crosspoint switch ICs to accommodate various price points and application requirements.
- **Subset Wiring Routing Compatibility:** Ensure signal routing and netlist representations remain a strict subset of the existing Jumperless V5 wiring scheme and firmware infrastructure.

---

## Business Case & Use Cases

### Business Case

Traditional breadboard prototyping suffers from high friction due to wire clutter, incorrect wiring, and manual debugging effort. While Jumperless V5 solves these issues, its custom PCB assembly, high IC density, and custom spring-clip breadboard shell result in higher manufacturing costs.

**JumperlessV5light** addresses these commercial and operational goals:
1. **Lower Bill of Materials (BOM) & Manufacturing Cost:** Utilizing off-the-shelf Raspberry Pi Pico 2 modules eliminates chip-down RP2350 placement complexity and reduces board layer counts.
2. **Tiered Product Offerings:** Modular support for 1, 4, or 12 CH446Q switches enables tiered entry pricing (Entry, Standard, Advanced) targeting students, makers, and professional engineers.
3. **Broadened Breadboard Compatibility:** By attaching externally to standard breadboards on one side, users can keep existing hardware components in place and reuse standard lab breadboards.
4. **Maintenance & Repairability:** Socketed Pico 2 modules allow effortless replacement if an MCU is damaged during high-voltage experimentation.

### Use Cases

#### UC-1: Basic Automated Signal Routing (1 CH446Q Variant)
- **Actor:** STEM Student / Hobbyist.
- **Description:** Route up to 8 dual-node software jumper connections across key breadboard rows and power channels.
- **Outcome:** Teaches basic circuit concepts and automated netlist routing at minimal cost.

#### UC-2: Sub-System Prototyping & Audio/Sensor Matrix (4 CH446Q Variant)
- **Actor:** Electronics Maker / Audio Designer.
- **Description:** Dynamically switch audio signals, sensor inputs, and power rails across 16–32 breadboard nodes.
- **Outcome:** Rapid iteration of signal-chain blocks without manually rewiring component leads.

#### UC-3: Full Single-Side Jumperless Prototyping (12 CH446Q Variant)
- **Actor:** Embedded Firmware / Hardware Developer.
- **Description:** Full matrix crossbar routing across all rows on one side of a standard breadboard plus Arduino Nano header pins.
- **Outcome:** Complete automated netlist management, scriptable hardware mutation, and interactive probe measurement.

#### UC-4: Modular MCU Swapping & Educational Labs
- **Actor:** Educator / Lab Instructor.
- **Description:** Swap Pico 2 controller boards between units or replace damaged MCUs directly in classroom environments.
- **Outcome:** Zero downtime and simple field repairs.

#### UC-5: Scripted Hardware-in-the-Loop Testing
- **Actor:** Automated Test Engineer / MicroPython Developer.
- **Description:** Execute Python or CLI scripts to reconfigure breadboard nets, run parametric voltage/current sweeps, and verify device behavior automatically.
- **Outcome:** Reproducible automated testing of analog/digital components.

---

## High-Level Architecture & Functional Components

### System Architecture Overview

```
 +-------------------------------------------------------------------+
 |                   JumperlessV5light Board                         |
 |                                                                   |
 |  +-----------------------+      +------------------------------+  |
 |  |  Raspberry Pi Pico 2  | SPI  |  CH446Q Switch Matrix Array  |  |
 |  |  (RP2350 Host MCU)    |----->|  (1, 4, or 12 ICs)          |  |
 |  +-----------------------+      +------------------------------+  |
 |              |                                |                   |
 |     USB /    | GPIO &                         | Crosspoint        |
 |     Serial   | Measurement                    | Connections       |
 |              v                                v                   |
 |  +-----------------------+      +------------------------------+  |
 |  |  Power & Level Shift  |      |  Single-Side Breadboard      |  |
 |  |  (±8V Supplies, ADCs) |      |  Header & Probe Interface    |  |
 |  +-----------------------+      +------------------------------+  |
 +-------------------------------------------------------------------+
                                                 |
                                                 v
                                    +--------------------------+
                                    | Standard Breadboard      |
                                    | (One-Sided Edge Connect) |
                                    +--------------------------+
```

### Top-Level Functional Components & Business Interfaces

#### 1. Microcontroller Core Component
- **Description:** Hosts system firmware on a socketed Raspberry Pi Pico 2 board (RP2350). Handles command parsing, matrix routing algorithms, netlist management, and peripheral communication.
- **Business Interface:**
  - `USB CDC Serial Interface`: Standard CLI and serial netlist command ingestion (`f {node1-node2, ...}`).
  - `SPI Matrix Bus Interface`: High-speed serial control interface driving address latches on CH446Q switches.

#### 2. Matrix Switching Network Component
- **Description:** Analog crosspoint matrix composed of 1, 4, or 12 CH446Q ICs. Connects arbitrary breadboard nodes on the target side to internal power, measurement, and GPIO channels.
- **Business Interface:**
  - `Crosspoint Route Interface`: Set or clear analog switch connections based on computed crossbar addresses.
  - `Subset Compatibility Layer`: Maps netlist requests down to available hardware chip counts (1, 4, or 12 ICs).

#### 3. Power Supply & Level Shifting Component
- **Description:** Generates ±8V rails for switch matrix operation and buffers DAC/ADC measurement channels.
- **Business Interface:**
  - `Programmable Power Rail Interface`: Software-controlled DAC output lines (±8V).
  - `Analog Sensing Interface`: Level-shifted ADC inputs for voltage, current, and resistance probing.

#### 4. Single-Side Breadboard Connection Component
- **Description:** Precision pin-header assembly physically mating JumperlessV5light to row pins on one edge of a standard breadboard and Nano header.
- **Business Interface:**
  - `Breadboard Node Interface`: Direct analog/digital pin connectivity to breadboard rows 1–30/1–60.

#### 5. Interactive Probing & User Interaction Component
- **Description:** Manages voltage-divider resistance probing and status LED indication.
- **Business Interface:**
  - `Probe Interface`: TRRRS probe jack sensing row selections via resistive tap.
  - `LED Matrix Status Interface`: Visual indication of active connections, voltages, and slot states.

---

## Major Choices & Evaluation

To ensure sound architectural decisions, each major choice was evaluated against three distinct alternatives.

### Choice 1: Microcontroller Core Integration Strategy

- **Alternative 1 (Direct Chip-Down SMT RP2350):** Place surface-mount RP2350 IC and supporting crystal/flash directly on the JumperlessV5light PCB.
- **Alternative 2 (Raspberry Pi Pico 2 DIP Module Header) [SELECTED]:** Mount a standard Raspberry Pi Pico 2 board via headers on the JumperlessV5light PCB.
- **Alternative 3 (External PC Bridge):** Omit onboard microcontroller entirely and control matrix hardware via USB-to-SPI bridge from a PC.

#### Justification for Alternative 2 (Selected)
Using the Pico 2 DIP module dramatically lowers assembly risk, leverages mass-produced module pricing, allows instant MCU swapping in case of overvoltage damage, and simplifies PCB layout to 2–4 layers.

---

### Choice 2: Matrix Crosspoint Switch Scaling & Hardware Variants

- **Alternative 1 (Fixed 12 x CH446Q Matrix Only):** Single rigid hardware design with all 12 CH446Q ICs permanently required.
- **Alternative 2 (Unified PCB Footprint for 1, 4, or 12 CH446Q Variants) [SELECTED]:** A single PCB design accommodating solder populating 1, 4, or 12 CH446Q ICs, coupled with firmware that gracefully handles subset wiring.
- **Alternative 3 (Three Separate PCB Layouts):** Design three completely distinct PCBs for 1-chip, 4-chip, and 12-chip configurations.

#### Justification for Alternative 2 (Selected)
A unified PCB layout with unpopulated IC options minimizes engineering overhead, streamlines manufacturing inventory, and allows software subset mapping to seamlessly scale routing capability based on populated hardware.

---

### Choice 3: Breadboard Mechanical Form Factor & Interface

- **Alternative 1 (Custom Dual-Sided Shell with Custom Clips):** Retain Jumperless V5 custom top and bottom shell with integrated phosphor-bronze spring clips.
- **Alternative 2 (Single-Sided Companion Board Attachment) [SELECTED]:** Design JumperlessV5light as an edge-mating companion board connecting to one side of a standard commercial breadboard via standard 0.1" headers or spring pins.
- **Alternative 3 (Standalone Desktop Box with Ribbon Cable Interconnects):** Place matrix hardware in a standalone external enclosure linked to breadboards via multi-wire ribbon cables.

#### Justification for Alternative 2 (Selected)
Single-sided companion attachment preserves compatibility with standard off-the-shelf breadboards, eliminates expensive custom spring-clip manufacturing, and provides a compact, direct physical footprint.

---

## Summary of Discarded Alternatives

### 1. Discarded Microcontroller Options
- **Direct SMT RP2350 (Choice 1, Alt 1):** Discarded due to increased PCB manufacturing cost, higher assembly failure risk, and difficult field repairability when subjected to experimental circuit overvoltages.
- **External PC Bridge (Choice 1, Alt 3):** Discarded because it removes standalone operation (OLED, probe, local CLI) and increases latency for interactive signal probing.

### 2. Discarded Matrix Scaling Options
- **Fixed 12 x CH446Q Only (Choice 2, Alt 1):** Discarded as it prevents offering a low-cost entry-level product tier for STEM education.
- **Three Separate PCB Layouts (Choice 2, Alt 3):** Discarded due to tripled PCB tooling costs, complex supply chain management, and redundant hardware maintenance.

### 3. Discarded Form Factor Options
- **Custom Dual-Sided Shell with Spring Clips (Choice 3, Alt 1):** Discarded due to high mechanical tooling costs and inability to use standard off-the-shelf breadboards.
- **Standalone Enclosure with Ribbon Cables (Choice 3, Alt 3):** Discarded due to high parasitics, bulky cable clutter, and degraded analog signal integrity over longer ribbon cable runs.
