# Jumperless V5-light Project Roadmap

## Progress Overview

| Phase | Description | Status |
| :---: | :--- | :---: |
| **Phase 1** | System Specification & Conceptual Architecture | ✅ |
| **Phase 2** | Detailed Technical Design & OpenAPI REST Definitions | ✅ |
| **Phase 3** | Core Matrix Routing & CLI Source Implementation | ✅ |
| **Phase 4** | Automated Testing Suite & CI/CD Setup | ✅ |
| **Phase 5** | Hardware Verification & Physical Manufacturing Prototype | ⏳ |

---

## Goals

- 🎯 **Minimal Breadboard Edge Form Factor**: Compact attachment for any 0.1" solderless breadboard border. (Status: ✅)
- 🎯 **CH446Q Crosspoint Matrix Routing**: Software-defined analog connection paths. (Status: ✅)
- 🎯 **RP2350 High-Speed Control**: Sub-microsecond PIO switch state timing. (Status: ✅)
- 🎯 **Dual CLI & REST API Interfaces**: Both interactive short/long form CLI options and JSON API. (Status: ✅)
- 🎯 **Complete CI/CD Integration**: Automated cross-platform tests and documentation workflow. (Status: ✅)

---

## Phases & Detailed Task Tracking

### Phase 1: Specifications & Concept Definition ✅
- [x] Define V5-light product goal and target use cases in `CONCEPT.md` <!-- issue-1 2025-02-15 -->
- [x] Document CH446Q, RP2350, and breadboard edge connector specifications in `/specification/` <!-- issue-2 2025-02-15 -->
- [x] Create high-level PlantUML architecture diagram `TOP_ARCHITECTURE.puml` <!-- issue-3 2025-02-15 -->

### Phase 2: Detailed Technical Design & API Definition ✅
- [x] Complete system component and interface architecture in `DESIGN.md` <!-- issue-4 2025-02-15 -->
- [x] Evaluate major hardware and software choices with 3 alternatives each <!-- issue-5 2025-02-15 -->
- [x] Define OpenAPI 3.0 specification in `api/openapi.yaml` <!-- issue-6 2025-02-15 -->

### Phase 3: Hardware Drivers & Firmware Implementation ✅
- [x] Implement CH446Q crossbar driver module in `/src/` <!-- issue-7 2025-02-15 -->
- [x] Implement CLI interface supporting both short and long form flags (`-c`/`--connect`, `-d`/`--disconnect`, etc.) in `/src/` <!-- issue-8 2025-02-15 -->
- [x] Implement REST API controller and server bridge in `/src/` <!-- issue-9 2025-02-15 -->
- [x] Create environment installation script `src/install.sh` <!-- issue-10 2025-02-15 -->

### Phase 4: Testing & CI/CD Pipeline ✅
- [x] Create test runner environment script `test/install.sh` <!-- issue-11 2025-02-15 -->
- [x] Implement unit tests for CH446Q routing matrix algorithm in `/test/` <!-- issue-12 2025-02-15 -->
- [x] Implement integration tests for CLI flags and REST API endpoints in `/test/` <!-- issue-13 2025-02-15 -->
- [x] Set up GitHub Actions workflow in `.github/workflows/ci.yml` <!-- issue-14 2025-02-15 -->

### Phase 5: Hardware Prototyping & Field Testing ⏳
- [ ] Fabricate V5-light PCB prototypes and assemble initial revision
- [ ] Perform hardware oscilloscope and signal integrity testing on CH446Q paths
- [ ] User testing on 830-point solderless breadboards with real microcontrollers
