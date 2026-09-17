# Raspberry Pi RP2350 Microcontroller Specification Summary

## Overview

The **RP2350** is high-performance microcontroller developed by Raspberry Pi, featuring dual ARM Cortex-M33 cores and dual Hazard3 RISC-V cores running up to 150 MHz, with advanced Programmable I/O (PIO) blocks, high-speed DMA, and flexible security primitives.

In **Jumperless V5-light**, the RP2350 serves as the main system controller managing CH446Q crossbar matrix switches, host communications via USB CDC CLI/REST endpoints, power rail controls, and breadboard edge interface sensing.

---

## Core Specifications

| Feature | Details |
| :--- | :--- |
| **CPU Cores** | Dual ARM Cortex-M33 or Dual Hazard3 RISC-V @ 150 MHz |
| **SRAM** | 520 KB on-chip SRAM in 10 accessible banks |
| **Flash Memory** | External Quad-SPI Flash (typically 4 MB to 16 MB) |
| **PIO Blocks** | 3 PIO state machine blocks (12 total independent state machines) |
| **GPIO Count** | Up to 30 (RP2350A) / 48 (RP2350B) flexible multifunction GPIOs |
| **ADC** | 12-bit 500 ksps ADC with up to 4/8 external channels |
| **Interfaces** | 2 × UART, 2 × SPI, 2 × I2C, 24 × PWM channels, USB 1.1 Host/Device |
| **Security** | ARM TrustZone, Secure Boot, SHA-256 hardware accelerator, OTP memory |
| **Supply Voltage** | 3.3V I/O supply ($IOVDD$), 1.1V core supply ($DVDD$ via internal LDO / Buck) |

---

## Role in V5-light System

1. **CH446Q Matrix Driver via PIO**:
   - High-speed address decoding, data multiplexing, and pulse timing generated deterministically via RP2350 PIO state machines.
   - Allows matrix updates in microsecond execution windows.

2. **USB Interface & Dual Virtual COM Ports**:
   - USB CDC Class for CLI control terminal and REST/JSON API interface over serial/socket bridge.
   - USB Mass Storage (UF2) for drag-and-drop firmware updates and netlist profile management.

3. **Breadboard Control & Voltage Measurement**:
   - Integrated 12-bit ADC channels monitor breadboard rail voltages and node connection continuity.
   - Digital I/O channels interface to breadboard logic lines with level shifting.
