
# RootWatch AI: AI-Assisted Linux Rootkit Indicator Detector

RootWatch AI is a defensive Linux security project that detects rootkit-like indicators by monitoring kernel module changes, collecting forensic evidence, and using AI-assisted SOC analysis to explain suspicious findings.

The project focuses on **rootkit indicator detection**, not rootkit creation. It uses a harmless custom kernel module inside an isolated VM to safely simulate an unexpected kernel-level change.

---

## Project Overview

Rootkits often operate at a low level and may attempt to hide processes, files, network activity, or kernel modules. Instead of creating or running a real rootkit, this project safely detects **unexpected kernel-level changes** using baseline comparison.

RootWatch AI compares the currently loaded Linux kernel modules against a clean baseline. If a new module appears, the tool collects evidence and sends it to an AI model for SOC-style explanation.

---

## Key Features

- Kernel module baseline creation
- Current loaded module scanning
- New/unknown kernel module detection
- Removed module detection
- Evidence collection from:
  - `lsmod`
  - `/proc/modules`
  - `modinfo`
- Gemini AI-assisted module analysis
- Streamlit dashboard
- Safe harmless kernel module for testing
- SOC-style investigation guidance

---

## Tech Stack

- Python
- Linux
- Bash
- Linux Kernel Modules
- C
- Streamlit
- Gemini API
- `lsmod`
- `/proc/modules`
- `modinfo`

---

## Project Architecture

```txt
Clean Linux VM
      ↓
Create module baseline
      ↓
Load harmless test kernel module
      ↓
Scan current kernel modules
      ↓
Compare current modules with baseline
      ↓
Detect new/unknown module
      ↓
Collect evidence
      ↓
AI-assisted SOC analysis
      ↓
Dashboard/report