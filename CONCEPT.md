# Jumperless V5-light Concept Specification

## Product Goal

Build a minimal, highly modular version of the Jumperless V5 named **V5-light** designed to be reusable and seamlessly attachable to the border or outer rails of any standard solderless breadboard.

**Core Hardware Scope**: CH446Q Crosspoint Matrix Switch + RP2350 Microcontroller.

---

## Business & Use Cases

### 1. Target Market & Value Proposition
- **Educational Electronics Labs & Universities**: Students often waste significant time debugging misplaced jumper wires on standard breadboards. V5-light provides software-defined jumper routing and real-time connectivity feedback at a fraction of the cost of full-size hardware IDEs.
- **Hardware Prototypers & Embedded Engineers**: Provides programmatic circuit reconfiguration, automated test matrix cycling, and rapid component verification attached to any existing breadboard setup.
- **Maker & Modular Audio Enthusiasts**: Modular synthesizers and breadboard audio effects routing benefit from instant, silent patch switching without physically re-wiring circuits.

### 2. Primary Use Cases
1. **Edge-Attached Software Jumpering**:
   - Plug V5-light into the top/side rails of any 830-point or 400-point breadboard.
   - Routable analog jumper paths connect arbitrary breadboard columns together via software commands.
2. **Automated Test & Characterization**:
   - Programmatically cycle through circuit configurations (e.g., swapping resistor values or pinouts) for automated hardware testing.
3. **Remote Hardware Debugging**:
   - Developers control hardware routing remotely over USB CLI or REST API without needing physical access to re-wire breadboard connections.

---

## High-Level Functional Architecture

```
+-----------------------------------------------------------------------+
|                         Host CLI / REST Interface                     |
+-----------------------------------------------------------------------+
                                   | (USB CDC Serial / REST)
                                   v
+-----------------------------------------------------------------------+
|                    RP2350 Central Processing Core                     |
|  - Command Processing & Netlist Manager                               |
|  - High-Speed PIO Crosspoint Driver                                  |
|  - Power Rail & Sense Subsystem Control                               |
+-----------------------------------------------------------------------+
        |                                                 |
        v (PIO Signals)                                   v (ADC Probe)
+-------------------------------+              +------------------------+
| CH446Q Crosspoint Switch Array|              | Voltage / Continuity   |
|  (16x8 Matrix Analog Routes)  |              | Measurement Unit       |
+-------------------------------+              +------------------------+
        |                                                 |
        +-----------------------+-------------------------+
                                |
                                v
+-----------------------------------------------------------------------+
|              Breadboard Border Physical Interface Strip               |
|            (Standard 2.54mm Edge Connectors & Power Rails)            |
+-----------------------------------------------------------------------+
                                |
                                v
+-----------------------------------------------------------------------+
|                        Target Breadboard Nodes                        |
+-----------------------------------------------------------------------+
```

### Business Interfaces
- **User Control Interface (CLI / REST)**: Enables developers and automation tools to query and update circuit nets.
- **Breadboard Interconnect Interface**: Universal pin header row connecting directly to breadboard outer rails and tie-point columns.
- **Power & Sensing Interface**: Supply programmable voltages and sample internal matrix node voltages.

---

## Summary of Alternatives and Decisions

For each major architectural choice in the concept phase, three alternatives were evaluated. The selected option and discarded alternatives are summarized below:

### 1. Crosspoint Switching Technology
- **Alternative A (Chosen)**: **CH446Q Analog Crosspoint Switch Array**
  - *Rationale*: Offers 16x8 analog switching per chip with low cost, solid high-frequency performance (>50 MHz), and well-understood overdriving capabilities up to $\pm 8\text{V}$.
- **Alternative B (Discarded)**: Discrete Relay Matrix (Reed / Solid State Relays)
  - *Reason for rejection*: Excessively bulky, higher power consumption, noisy, and cost-prohibitive for compact edge mounting.
- **Alternative C (Discarded)**: Discrete MOSFET Switch Matrix
  - *Reason for rejection*: High chip count, complex gate driving circuits, and non-linear $R_{ON}$ variations across signal voltages.

### 2. Main System Microcontroller
- **Alternative A (Chosen)**: **Raspberry Pi RP2350**
  - *Rationale*: Flexible Programmable I/O (PIO) state machines allow deterministic timing for CH446Q matrix control, high dual-core CPU performance, 520 KB SRAM, and low unit cost.
- **Alternative B (Discarded)**: RP2040 Microcontroller
  - *Reason for rejection*: Lower memory, fewer security/DMA features, lacks ARM Cortex-M33 / Hazard3 RISC-V optionality, and limited high-density GPIO options compared to RP2350.
- **Alternative C (Discarded)**: STM32F4 / ESP32-S3
  - *Reason for rejection*: Lacks PIO state machines required for zero-CPU bit-banged crosspoint strobe control; higher development complexity for fast matrix switching.

### 3. Physical Attachment Form Factor
- **Alternative A (Chosen)**: **Edge-Mounted Modular Strip with Standard 0.1" Headers**
  - *Rationale*: Fits any standard solderless breadboard border; highly reusable and non-destructive.
- **Alternative B (Discarded)**: Custom Integrated Breadboard Baseplate
  - *Reason for rejection*: Forces users to buy proprietary breadboards; reduces reusability across existing setup.
- **Alternative C (Discarded)**: Standalone External Desktop Box with Cable Loom
  - *Reason for rejection*: Messy cabling reduces user convenience and reintroduces wiring clutter.
