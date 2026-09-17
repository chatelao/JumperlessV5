# CH446Q High-Speed CMOS 16x8 Analog Crosspoint Switch Specification

## Overview

The **CH446Q** is a high-speed CMOS analog crosspoint switch array manufactured by WCH (WinChipHead). It features a 16x8 matrix of analog switches that can connect any of the 16 X-axis pins to any of the 8 Y-axis pins under digital control.

In the **Jumperless V5-light** architecture, CH446Q crossbar switches provide hardware-programmable jumperless connection routes between standard breadboard tie-points, power rails, measurement channels, and RP2350 microcontroller GPIOs.

---

## Key Features & Electrical Specifications

| Parameter | Specification | Notes / Operating Conditions |
| :--- | :--- | :--- |
| **Matrix Configuration** | 16 × 8 Crosspoint Array | 128 total internal switch nodes |
| **Operating Voltage ($V_{DD} - V_{SS}$)** | 4.5V to 12.0V | Overdriven up to ±9V / 18V total in Jumperless design |
| **Analog Signal Range** | $V_{SS}$ to $V_{DD}$ | Signals within supply rail boundaries |
| **On-Resistance ($R_{ON}$)** | ~45 Ω per switch | Total ~90 Ω for X-to-Y-to-X double pass |
| **Bandwidth (-3dB)** | > 50 MHz | Suitable for audio, high-speed SPI, UART, I2C |
| **Off-Isolation / Crosstalk** | -65 dB @ 10 MHz | Minimal signal leak between channels |
| **Control Interface** | 7-bit Parallel / Serial Addressable | 4-bit X address ($X_0-X_3$), 3-bit Y address ($Y_0-Y_2$), Data, Strobe |
| **Package** | SOP-24 / SSOP-24 | Compact SMD form factor |

---

## Pinout and Signal Definitions

| Pin Number | Name | Type | Description |
| :---: | :--- | :---: | :--- |
| 1 - 8 | $Y_0$ - $Y_7$ | Analog I/O | Y-axis matrix channels (8 channels) |
| 9 | $V_{SS}$ | Power | Negative Power Supply Rail (-5V to -9V) |
| 10 - 13 | $X_0$ - $X_3$ | Analog I/O | X-axis matrix channels (first 4 of 16) |
| 14 | $GND$ | Power | Digital Logic Ground reference |
| 15 - 20 | $X_4$ - $X_9$ | Analog I/O | X-axis matrix channels |
| 21 | $RESET$ | Digital Input | Master clear / reset all switch connections (Active High) |
| 22 | $STROBE$ | Digital Input | Latches the current address and DATA state into switch cell |
| 23 | $DATA$ | Digital Input | Switch state to write (1 = Closed / Connected, 0 = Open / Disconnected) |
| 24 | $V_{DD}$ | Power | Positive Power Supply Rail (+5V to +9V) |

---

## Digital Addressing Scheme

To configure an individual crosspoint switch at address $(X_i, Y_j)$:

1. Assert 4-bit binary address on $AX_0 - AX_3$ corresponding to $X_0 \dots X_{15}$.
2. Assert 3-bit binary address on $AY_0 - AY_2$ corresponding to $Y_0 \dots Y_7$.
3. Set $DATA = 1$ to close (connect) the switch, or $DATA = 0$ to open (disconnect) the switch.
4. Pulse $STROBE$ high for at least 20 ns to latch the state.

---

## Operating Characteristics for V5-light

- **Overdrive Supply Strategy**: The CH446Q is powered at $\pm 8\text{V}$ or $\pm 9\text{V}$ rail-to-rail using an LT1054 charge-pump inverter / boost circuit driven by RP2350 USB 5V.
- **Multiplexed Daisy Chaining**: Multiple CH446Q chips are tiled along the X and Y buses to scale connection points along the breadboard edge interface.
