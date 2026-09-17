
![](https://jumperless-docs.readthedocs.io/en/latest/assets/JNameLogo.png)

###### The next generation [jumperless](https://github.com/Architeuthis-Flux/Jumperless) breadboard & **Jumperless V5-light**
---

## Documentation & Pages
- **[ReadTheDocs Documentation Site](https://jumperless-docs.readthedocs.io/en/latest)**
- **[GitHub Pages Documentation & API Reference](https://Architeuthis-Flux.github.io/JumperlessV5)**
- **[OpenAPI REST Specification](api/openapi.yaml)**

---

# Jumperless V5-light Overview

**Jumperless V5-light** is a minimal, modular edition of the Jumperless V5 architecture engineered to attach directly to the border/edge of any standard solderless breadboard.

By leveraging an array of **CH446Q high-speed CMOS analog crosspoint switches** driven by an **RP2350 microcontroller**, V5-light provides software-defined jumper wires, dynamic netlist reconfigurations, and remote hardware API control without cluttering your physical breadboard area.

---

## Key Features

- **Universal Edge Attachment**: Modular 0.1" (2.54mm) pin header interface mounts to the border of any 830-point or 400-point breadboard.
- **RP2350 High-Speed PIO Driver**: Hardware-accelerated crosspoint switch strobing and address decoding.
- **Dual CLI & REST API Interfaces**: Flexible control via interactive command line or JSON REST web services.
- **Programmable Power Rails & Sensing**: Integrated $\pm 8\text{V}$ rail overdriving and 12-bit ADC voltage monitoring.

---

## Project Documentation & Specifications

- **[CONCEPT.md](CONCEPT.md)**: Product goals, business & use cases, top-level architecture, and conceptual alternative evaluations.
- **[DESIGN.md](DESIGN.md)**: Detailed technical design, tech stack choices, schematic interfaces, and architectural trade-offs.
- **[TOP_ARCHITECTURE.puml](TOP_ARCHITECTURE.puml)**: PlantUML component and dataflow diagram.
- **[ROADMAP.md](ROADMAP.md)**: Project implementation roadmap and task tracking.
- **[TECHNICAL_DEBTS.md](TECHNICAL_DEBTS.md)**: Known constraints and logged technical debts.
- **[/specification/](specification/)**: Hardware datasheets converted to Markdown (`CH446Q_datasheet.md`, `RP2350_datasheet_summary.md`, `Breadboard_Interface_Spec.md`).

---

## Quickstart & Installation

1. **Install Dependencies**:
   ```bash
   ./src/install.sh
   ./test/install.sh
   ```

2. **Run CLI Commands**:
   The `v5light` CLI tool supports both short and long form flags for every option:
   ```bash
   # Connect node 1 to node 15
   python3 -m src.v5light_cli -c "1-15"
   python3 -m src.v5light_cli --connect "TOP_RAIL,5"

   # List active crosspoint routes
   python3 -m src.v5light_cli -l
   python3 -m src.v5light_cli --list

   # Query board status
   python3 -m src.v5light_cli -s
   python3 -m src.v5light_cli --status

   # Disconnect route or reset matrix
   python3 -m src.v5light_cli -d "1-15"
   python3 -m src.v5light_cli --reset
   ```

3. **Start REST API Bridge Server**:
   ```bash
   python3 src/rest_server.py
   ```
   Endpoints will be available at `http://localhost:8080/api/v1/`.

4. **Run Automated Test Suite**:
   ```bash
   PYTHONPATH=. python3 -m pytest -v test/
   ```

---

Watch the launch video here:
[![Launch Video](https://img.youtube.com/vi/fJTE7R_CV8w/maxresdefault.jpg)](https://www.youtube.com/watch?v=fJTE7R_CV8w)

---

# Jumperless V5 Full IDE

Jumperless V5 lets you prototype like a nerdy wizard who can see electricity and conjure jumpers with a magic wand. It’s an Integrated Development Environment (IDE) for hardware, with an analog-by-nature RP2350B dev board, a drawer full of wires, and a workbench full of test equipment (including a power supply, a multimeter, an oscilloscope, a function generator, and a logic analyzer) all crammed inside a breadboard.

### **These are the docs where you will learn how to wield your new powers**

![](https://github.com/user-attachments/assets/3f0584fd-2cc1-4036-bf2b-6a18eb98a6d5)

## [Get a Jumperless V5 on Crowd Supply](https://www.crowdsupply.com/architeuthis-flux/jumperless-v5)

---

## Find Me On The Internet

Join the [Discord](https://discord.gg/bvacV7r3FP) for pretty much instant answers to your questions!
