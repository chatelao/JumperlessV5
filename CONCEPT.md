# Jumperless Concept & Architectural Progression

## Project Goal
The primary goal of **Jumperless** is to transform hardware prototyping into a seamless, software-scriptable, "God Mode" experience—an Integrated Development Environment (IDE) built directly into a physical breadboard.

Traditional hardware prototyping suffers from significant friction: tangled jumper wires clutter the workspace, obscure circuit topology, introduce intermittent physical connection errors, and make real-time circuit state diagnosis tedious. Jumperless eliminates this friction by substituting physical jumper wires with a software-controlled matrix of analog crossbar switches controlled by a microcontroller (RP2350B).

Key objectives include:
- **Software-Defined Wiring**: Connecting any pair of breadboard rows, Nano header pins, power rails, or internal special function peripherals (ADCs, DACs, GPIOs, current sensors) programmatically or via a physical probe.
- **Real-Time Visual Feedback**: Illuminating addressable RGB LEDs under every hole on the breadboard to indicate voltages, node connections, logic levels, and active net topologies directly at the site of operation.
- **Scriptable Hardware**: Enabling automated hardware testing, evolvable hardware algorithms, dynamic audio route switching, chip characterization, and remote circuit configuration without touching physical wires.
- **Embedded Test Bench**: Integrating programmable power supplies (±8V), high-current DACs, buffered ADCs, current/resistance sensors, logic analyzer capability, and routable GPIOs within a single self-contained unit.

---

## Evolution of the Matrix Architecture

Connecting every point on a 60-row breadboard to any other point—along with power rails and internal measurement instruments—requires a crossbar array. The evolution from a single chip concept to the production Jumperless V5 architecture progressed through two critical intermediate steps:

```
[ Step 1: One CH446Q ] ---> [ Step 2: Four CH446Q ] ---> [ Final: Twelve CH446Q (Jumperless V5) ]
```

---

### Step 1: One CH446Q

#### Architecture & Concept
The CH446Q is a CMOS analog crosspoint switch chip providing a **16 × 8 array** (16 X-axis pins, 8 Y-axis pins, totaling 128 internal switches). In the initial single-chip concept, the objective was to evaluate whether an analog crossbar array could function as an acceptable substitute for physical breadboard jumper wires.

```
            One CH446Q Crosspoint Matrix (16 x 8)
                Y0  Y1  Y2  Y3  Y4  Y5  Y6  Y7  (8 Y Bus Lines)
               ┌───┬───┬───┬───┬───┬───┬───┬───┐
            X0 │ o │ o │ o │ o │ o │ o │ o │ o │
            X1 │ o │ o │ o │ o │ o │ o │ o │ o │
            ...│   │   │   │   │   │   │   │   │
           X15 │ o │ o │ o │ o │ o │ o │ o │ o │
               └───┴───┴───┴───┴───┴───┴───┴───┘
               (16 X Pins connected to Breadboard Rows)
```

#### Characteristics & Capabilities
- **Direct Switching**: Any X pin can be connected to any Y pin by turning on the crosspoint switch at address `(X, Y)`.
- **Bridge Creation**: Connecting `X_a` to `X_b` requires routing through a shared Y bus line (`X_a -> Y_k -> X_b`).
- **Maximum Concurrent Nets**: Up to 8 independent signal nets can exist simultaneously (since there are only 8 Y bus lines).

#### Limitations
- **Severely Restricted Row Coverage**: 16 X pins can only cover 16 rows out of 60 on a standard breadboard.
- **Limited Net Capacity**: Only 8 concurrent nets/busses available.
- **No Peripheral Support**: No remaining pins to route dedicated power supplies, ADCs, DACs, or GPIOs without sacrificing breadboard row connections.
- **High On-Resistance ($R_{on}$)**: Standard 5V operation results in ~$100–125\Omega$ per switch pass (totalling $>200\Omega$ per jumper connection).

---

### Step 2: Four CH446Q

#### Architecture & Concept
To expand coverage across more breadboard rows and allow basic power and GPIO integration, four CH446Q chips are arranged into a combined 4-chip crossbar array.

```
       ┌────────────────────────┐        ┌────────────────────────┐
       │     CH446Q Chip A      │        │     CH446Q Chip B      │
       │ X: Rows 1–12, GND, VCC │        │ X: Rows 13–24, GPIOs   │
       │ Y: Inter-chip Bus Y0–Y7│        │ Y: Inter-chip Bus Y0–Y7│
       └───────────┬────────────┘        └───────────┬────────────┘
                   │                                 │
                   └───────────────┬─────────────────┘
                                   │ Shared Y Bus / Bounce Lines
                   ┌───────────────┴─────────────────┐
                   │                                 │
       ┌───────────┴────────────┐        ┌───────────┴────────────┐
       │     CH446Q Chip C      │        │     CH446Q Chip D      │
       │ X: Rows 25–36, ADCs    │        │ X: Rows 37–48, DACs    │
       │ Y: Inter-chip Bus Y0–Y7│        │ Y: Inter-chip Bus Y0–Y7│
       └────────────────────────┘        └────────────────────────┘
```

#### Characteristics & Capabilities
- **Expanded Breadboard Reach**: 64 X pins total across 4 chips, covering ~48 breadboard rows plus dedicated power/GPIO nodes.
- **Inter-Chip Bouncing**: Routing between rows on different chips (e.g., Row 5 on Chip A to Row 30 on Chip C) is achieved by utilizing shared Y bus lines or inter-chip "bounce" lines (`Chip A (X_row5 -> Y_k) -> Chip C (Y_k -> X_row30)`).
- **Basic Peripheral Routing**: Dedicated X lines allocated for power, ADCs, and GPIOs.

#### Limitations
- **Y-Bus Bottlenecks**: As the number of chips increases, the 8 Y-lines per chip quickly become congested, leading to routing conflicts when attempting complex multi-net circuits.
- **Single-Stage Hierarchy**: Direct chip-to-chip bouncing lacks dedicated routing chips for peripheral aggregation, causing routing starvation for special functions.
- **Incomplete Coverage**: Still unable to cover all 60 breadboard rows, 30 Arduino Nano header pins, 4 power rails, and 10+ hardware peripherals simultaneously.

---

### Final Architecture: Twelve CH446Q Chips (Jumperless V5)

#### Architecture & Concept
Jumperless V5 utilizes **12 CH446Q chips** (designated Chip A through Chip L) arranged in a two-tier hybrid topology: 8 Breadboard Chips (A–H) and 4 Special Function / Interconnect Chips (I–L).

```
 ┌─────────────────────────────────────────────────────────────────────────────────┐
 │                            JUMPERLESS V5 CROSSBAR ARRAY                         │
 └─────────────────────────────────────────────────────────────────────────────────┘

   BREADBOARD CHIPS (Chips A – H): 8 × (16 X × 8 Y)
   ├── Chip A: Rows 1–7, Top/Bottom Rails, Inter-chip ties (AB, AC, AD, AE, AK, AF, AG, AL, AH)
   ├── Chip B: Rows 8–14, Inter-chip ties (AB, BI, BJ, BC, BD, BE, BF, BK, BG, BL)
   ├── Chip C: Rows 15–21, Inter-chip ties (AC, BC, CI, CJ, CD, CE, CL, CF, CK, CG, CH)
   ├── Chip D: Rows 22–28, Inter-chip ties (AD, BD, CD, DI, DJ, DF, DL, DG, DK, DH)
   ├── Chip E: Rows 31–37, Inter-chip ties (AE, BE, CE, DE, EK, EL, DE, EI, EJ, EF, EG, EH)
   ├── Chip F: Rows 38–44, Inter-chip ties (AF, BF, CF, DF, FK, FL, EF, FI, FJ, FG, FH)
   ├── Chip G: Rows 45–51, Inter-chip ties (AG, BG, CG, DG, GL, GK, EG, FG, GI, GJ, GH)
   └── Chip H: Rows 52–58, Inter-chip ties (AH, BH, CH, DH, HL, HK, EH, FH, GH, HI, HJ)

   SPECIAL FUNCTION CHIPS (Chips I – L): 4 × (16 X × 8 Y)
   ├── Chip I: Nano Header Pins (nA0, nD1..nD9), Current Sensors (I+, IL), Inter-chip ties (IJ, IK), UART RX
   ├── Chip J: Nano Header Pins (nA1, nD0..nD6), Current Sensors (I-, JL), Inter-chip ties (IJ, JK), UART TX
   ├── Chip K: Routable Buffers (BFi), Rails, DACs (Da0, Da1), ADCs (Ad0..Ad3), Inter-chip ties (KL, KI, KJ), GND
   └── Chip L: 5V Supply, GPIOs (GP1..GP8), Inter-chip ties (LI, LJ, LK), GND
```

#### Key Architecture Innovations in V5
1. **Overdriven Supply Voltage ($\pm 9\text{V}$ Charge Pump)**:
   - CH446Q switches are powered by an **LT1054CP charge pump** delivering $\sim\pm 9\text{V}$ rails (well beyond the 5V nominal specification).
   - High supply voltage drastically reduces switch $R_{on}$ to $\sim 45\Omega$ per crosspoint ($\sim 90\Omega$ total per 2-hop bridge) and allows passing signals in the range of $-8\text{V}$ to $+8\text{V}$.
2. **Dedicated Special Function Subsystem (Chips I–L)**:
   - Aggregates all internal hardware: 4 × 12-bit DACs (MCP4728), 3 × 12-bit buffered ADCs, 2 × INA219 current/voltage sensors, 10 × GPIOs (RP2350B & MCP23S17), op-amp buffers, and daisy-chain expansion headers.
   - Prevents peripheral routing from stealing Y-bus capacity from breadboard row-to-row connections.
3. **Multi-Hop Bouncing Algorithm**:
   - The firmware's `NetManager` and `NetsToChipConnections` algorithms compute path graphs through inter-chip ties (e.g. `Chip A -> Chip E -> Chip K`) in microseconds.
4. **RP2350 Dual-Core & High-Speed PIO Engine**:
   - **Core 0**: Handles CLI, TUI, MicroPython interpreter, file management, and netlist parsing.
   - **Core 2**: Dedicated to driving the 445 RGB LEDs and executing low-latency PIO SPI updates to the 12 CH446Q chip select/data lines via custom PIO state machines (`ch446.pio`).

---

## Summary Comparison Matrix

| Feature / Metric | Step 1: One CH446Q | Step 2: Four CH446Q | Final: Twelve CH446Q (Jumperless V5) |
| :--- | :--- | :--- | :--- |
| **Total Chips** | 1 | 4 | 12 (A–L) |
| **Crosspoint Switches** | 128 | 512 | 1,536 |
| **Breadboard Rows Covered** | 16 | ~48 | All 60 rows + Nano Header (30 pins) |
| **Concurrent Net Busses** | 8 | 16 | Unrestricted via multi-chip graph bouncing |
| **Switch Power Supply** | +5V / 0V | +5V / 0V | $\pm 9\text{V}$ (LT1054CP Charge Pump) |
| **Signal Voltage Range** | 0V to 5V | 0V to 5V | **$-8\text{V}$ to $+8\text{V}$** |
| **On-Resistance ($R_{on}$ per jumper)** | $>200\Omega$ | $>180\Omega$ | **$\sim 90\Omega$** ($45\Omega$ per switch pass) |
| **Peripheral Integration** | None | Limited | Full (4 DACs, 3 ADCs, 2 INA219, 10 GPIOs, OpAmp) |
| **Visual Feedback** | External | Basic LEDs | **445 Addressable RGB LEDs** under every row/rail |
