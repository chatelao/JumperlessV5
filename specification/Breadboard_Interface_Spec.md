# Jumperless V5-light Breadboard Edge Interface Specification

## Overview

The **Jumperless V5-light** is engineered as a compact, reusable modular strip designed to attach directly to the outer border/edge of any standard solderless breadboard (such as MB-102 or standard 830/400 tie-point breadboards).

This specification details the mechanical, electrical, and logical interfaces connecting V5-light to target breadboards.

---

## Mechanical Specifications

- **Form Factor**: Slim PCB strip designed to align along standard 2.54mm (0.1") pitch breadboard rail margins.
- **Mounting Mechanism**:
  - Top edge dual-row male pin headers (0.1" / 2.54mm pitch) angled or right-angled to plug into breadboard power rails ($V_{CC}$, $GND$) and outer row tie-points.
  - Optional mechanical clips / magnetic adhesive strips for border attachment.
- **Dimensions**: ~105 mm (L) × 20 mm (W) × 12 mm (H).

---

## Electrical Pin Interface

| Pin # | Signal Name | Type | Description |
| :---: | :--- | :---: | :--- |
| **P1** | `VBUS_5V` | Power | USB +5V Input / Output Power |
| **P2** | `GND` | Power | Common Ground Reference |
| **P3** | `VPLUS` | Power | Programmable Positive Rail (+1.2V to +8.0V, max 100mA) |
| **P4** | `VMINUS` | Power | Programmable Negative Rail (-1.2V to -8.0V, max 100mA) |
| **P5-P12** | `X0_ROW1` - `X7_ROW8` | Analog I/O | CH446Q Crossbar Crosspoint Connections (Rows 1 to 8) |
| **P13-P20** | `X8_ROW9` - `X15_ROW16` | Analog I/O | CH446Q Crossbar Crosspoint Connections (Rows 9 to 16) |
| **P21-P24** | `GPIO0` - `GPIO3` | Digital I/O | RP2350 Multifunction GPIO Pins (3.3V / 5V tolerant) |
| **P25-P26** | `ADC0` - `ADC1` | Analog Input | RP2350 ADC Measurement Channels (0 - 3.3V / ±8V buffered) |

---

## System Integration & Signal Limits

1. **Analog Switching Limits**:
   - Maximum Signal Voltage: $-8\text{V}$ to $+8\text{V}$.
   - Switch Resistance: $\sim 45\ \Omega$ per crosspoint ($\sim 90\ \Omega$ total loop path).
   - Maximum Current per Path: $100\text{ mA}$.

2. **Expansion Header**:
   - Daisy-chain headers on both ends allow multiple V5-light units to be linked end-to-end along longer breadboards or multi-breadboard setups.
