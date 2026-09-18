# Optimal Interconnections for 4x CH446Q Matrix Configuration

## 1. Executive Summary & Overview

The **Jumperless V5** platform utilizes high-speed WCH **CH446Q 16×8 analog crosspoint switches** to achieve software-configurable breadboard routing. While a full Jumperless V5 system can scale up to 12 CH446Q ICs, a **4-Multiplexer (4x CH446Q) configuration** offers an optimal balance between routing density, component count, and cost.

This document details the hardware architecture, pin assignment topology, backplane routing, and pathfinding strategies for a 4x CH446Q matrix setup (**Chips A, B, C, and D**).

---

## 2. Chip Hardware & Electrical Specifications

Each CH446Q IC contains a $16 \times 8$ matrix of CMOS analog switches, providing 128 crosspoint switches per chip, for a total of **512 crosspoints** across the 4-chip matrix.

| Specification | Parameter Value | Architectural Impact / Notes |
| :--- | :--- | :--- |
| **Matrix Size per IC** | 16 X-Channels, 8 Y-Channels | $16 \times 8 = 128$ crosspoints per IC |
| **Total Crosspoints (4 ICs)** | 512 Crosspoints | Supports up to 64 X-lines and 32 Y-lines total |
| **Overdriven Supply Voltage** | $\pm 9\text{V}$ (via LT1054 charge pump) | Extends signal handling to $\pm 9\text{V}$, exceeds default datasheet limits safely |
| **Switch On-Resistance ($R_{ON}$)** | $\sim 45\,\Omega$ per crosspoint switch | A full path through two switches gives $\sim 90\,\Omega$ total series resistance |
| **Current Handling** | up to $\sim 100\text{mA}$ per path | Stacking paths/rails reduces resistance for power nets |
| **Analog Bandwidth (-3dB)** | $50\text{ MHz}$ | Passes high-speed digital and analog signals with minimal degradation |
| **Address & Control Lines** | 4 Address lines ($A_0$--$A_3$), Data, Strobe | Driven by RP2350 PIO state machine |

---

## 3. 4-Chip Functional Distribution & Pin Mapping

In the optimal 4-chip layout, responsibilities are split logically across the breadboard and special function hardware:

```
                  ┌─────────────────────────────────────────┐
                  │              CHIP D (TRUNK)             │
                  │   Global Backplane & Inter-Chip Bridge  │
                  └────────────────────┬────────────────────┘
                                       │ Global Y-Bus
         ┌─────────────────────────────┼─────────────────────────────┐
         │                             │                             │
┌────────┴─────────┐         ┌─────────┴────────┐         ┌──────────┴─────────┐
│     CHIP A       │         │      CHIP B      │         │       CHIP C       │
│ Breadboard Left  │         │ Breadboard Right │         │ Special Functions  │
│ (Rows 1–15 & Top)│         │(Rows 16–30 & Btm)│         │ (Power/DAC/ADC/GPIO│
└──────────────────┘         └──────────────────┘         └────────────────────┘
```

### 3.1. Chip A: Left Breadboard Matrix (Rows 1–15)
Chip A handles the upper/left side of the breadboard rows and top rail.

* **X0 – X14:** Breadboard Terminal Rows 1 through 15.
* **X15:** `TOP_RAIL` (Programmable Power Rail).
* **Y0 – Y7:** Connected to the primary inter-chip Y-bus (`Y_BUS[0..7]`).

### 3.2. Chip B: Right Breadboard Matrix (Rows 16–30)
Chip B handles the lower/right side of the breadboard rows and bottom rail.

* **X0 – X14:** Breadboard Terminal Rows 16 through 30.
* **X15:** `BOTTOM_RAIL` (Programmable Power Rail).
* **Y0 – Y7:** Connected to the primary inter-chip Y-bus (`Y_BUS[0..7]`).

### 3.3. Chip C: Special Function & Peripheral Matrix
Chip C connects system power sources, analog peripherals, measure hardware, and microcontroller interfaces to the Y-bus.

* **X0:** `GND` (System Ground Reference)
* **X1:** `SUPPLY_3V3` (+3.3V Supply)
* **X2:** `SUPPLY_5V` (+5.0V USB Power)
* **X3:** `DAC0` (Buffered Analog Output 0)
* **X4:** `DAC1` (Buffered Analog Output 1)
* **X5:** `ADC0` / Current Probe Input
* **X6:** `ADC1` / Probe Tip Connection
* **X7:** `ADC2`
* **X8:** `ADC3`
* **X9 – X12:** Microcontroller Routable GPIOs (`GPIO_1` – `GPIO_4`)
* **X13:** `UART_TX`
* **X14:** `UART_RX`
* **X15:** `ROUTABLE_BUFFER_IN` / `ROUTABLE_BUFFER_OUT`
* **Y0 – Y7:** Connected to the primary inter-chip Y-bus (`Y_BUS[0..7]`).

### 3.4. Chip D: Inter-Chip Trunking & Tie-Line Matrix
Chip D acts as a dedicated high-capacity crossbar trunk between Chips A, B, and C when the direct Y-bus lines are fully populated or require independent isolated paths.

* **X0 – X7:** Secondary Tie-Lines linked to Chip A & B X-lines.
* **X8 – X15:** Inter-chip bridging lanes and stacked rail drivers.
* **Y0 – Y7:** Global Backplane Interconnect.

---

## 4. Optimal Y-Bus Interconnection & Tie-Line Topology

### 4.1. Shared Y-Bus (Backplane Lines)
The 8 Y-channels ($Y_0$ through $Y_7$) on Chips A, B, C, and D are wired in parallel to form an 8-lane global analog backplane (`Y_BUS[0..7]`).

```
Chip A Y[0..7]  ───────┐
Chip B Y[0..7]  ───────┼─────── [ GLOBAL Y-BUS (8 LANES) ]
Chip C Y[0..7]  ───────┤
Chip D Y[0..7]  ───────┘
```

This arrangement guarantees that **any node on Chip A, B, or C can connect to any other node via a single Y-line** (1-hop through the global bus).

### 4.2. Routing Path Types

1. **Intra-Chip Connection (1 Switch):**
   When two nodes exist on the same CH446Q chip (e.g., connecting Row 3 to Row 8 on Chip A), routing requires turning on a single crosspoint switch ($X_3 \to Y_k \to X_8$).
   * *Resistance:* $\sim 45\,\Omega$

2. **Inter-Chip Direct Connection via Y-Bus (2 Switches):**
   Connecting a node on Chip A (e.g., Row 5) to a node on Chip B (e.g., Row 20) uses a shared Y-line:
   $$\text{Chip A: } X_5 \to Y_2 \quad \Longleftrightarrow \quad \text{Chip B: } X_{20} \to Y_2$$
   * *Resistance:* $\sim 90\,\Omega$

3. **Special Function Routing (2 Switches):**
   Connecting a breadboard row on Chip B (Row 22) to `DAC0` on Chip C:
   $$\text{Chip B: } X_{22} \to Y_0 \quad \Longleftrightarrow \quad \text{Chip C: } X_3 (\text{DAC0}) \to Y_0$$
   * *Resistance:* $\sim 90\,\Omega$

4. **Trunk-Assisted / Multi-Hop Bridge (3–4 Switches):**
   Used when global Y-bus lines suffer contention. Signals route through Chip D tie-lines to reach open matrix channels.
   * *Resistance:* $\sim 135\,\Omega - 180\,\Omega$

---

## 5. Power Rail Stacking & Low-Resistance Strategy

Because each CH446Q switch exhibits $\sim 45\,\Omega$ resistance, high-current or ground return paths benefit from **path stacking (parallel connection)**.

```
                  ┌─────────────────────────────────────────┐
                  │           Parallel Rail Paths           │
                  └────────────────────┬────────────────────┘
         Y_BUS[0] ═════════════════════╧═════════════════════ Ground / Power
         Y_BUS[1] ═══════════════════════════════════════════ Ground / Power
```

* **GND Stacking:** Firmwares automatically allocate up to 2–4 parallel Y-lines for `GND` and primary power rails (`3V3`, `5V`, `TOP_RAIL`, `BOTTOM_RAIL`) when idle Y-lines are available.
* **Effective Resistance:** Stacking 2 paths drops the connection resistance from $\sim 90\,\Omega$ down to $\sim 45\,\Omega$; stacking 4 paths reduces it to $\sim 22.5\,\Omega$.

---

## 6. Pathfinding & Conflict Resolution Algorithm

When the pathfinder (`NetsToChipConnections.cpp`) routes connections across a 4x CH446Q matrix, it follows this priority sequence:

1. **Power Nets First:** Route `GND`, `SUPPLY_3V3`, `SUPPLY_5V`, and power rails first to reserve optimal parallel Y-lines.
2. **Direct Intra-Chip Paths:** Route single-chip connections that don't need Y-bus propagation.
3. **1-Hop Inter-Chip Paths:** Find available global Y-bus lines connecting source and destination chips.
4. **Alternative Tie-Line Routing (Chip D):** If a target Y-line is occupied by a different net, reroute through Chip D trunk lines.
5. **Conflict Validation:** Perform overlap checking (`checkForOverlappingPaths`) to ensure no two distinct nets share a Y-line or X-line simultaneously.

---

## 7. Verification & Diagnostic Checklist

To verify optimal interconnections in hardware or firmware tests:

1. **PIO SPI Transfer Test:** Ensure PIO state machine (`spi_ch446_multi_cs`) correctly toggles chip selects for Chips A, B, C, and D.
2. **Crosspoint Matrix Readback:** Verify matrix state arrays (`lastChipXY[4]`) accurately match the commanded net connections.
3. **Continuity & Voltage Drop Verification:** Measure voltage drops across high-current paths to verify power rail stacking is active.
