# AGDAC – Arduino Gas Data Acquisition and Control System

**AGDAC (Arduino Gas Data Acquisition and Control)** is an open-source, low-cost, multi-channel data acquisition system designed to record gas production from **Ritter MilliGascounters (MGC)** in anaerobic digestion, microbial electrolysis, and biochemical reactor experiments.

AGDAC replaces the proprietary **Rigamo + National Instruments** acquisition stack with a fully open **Arduino + Python** architecture while preserving metrological reliability and scalability.

This repository contains:
- The **Arduino firmware** for pulse detection and volume calculation
- The **Python acquisition software** for real-time visualization and CSV logging
- The **data handling pipeline** used in laboratory biogas experiments

The system is scientifically validated and described in:
> Flores-Rodriguez, C. & Mockaitis, G.  
> *The AGDAC: An Innovative Market-Oriented, Open-Source Multiplexing System for Advanced Biogas Volume Measurements in Research Experiments*  
> SSRN preprint 4942112 :contentReference[oaicite:0]{index=0}

---

## 1. System architecture

AGDAC measures gas production using the **tilting bucket principle** of Ritter MilliGascounters (MGCs).  
Each MGC contains a magnetically actuated tilt mechanism that produces a **binary pulse** (HIGH → LOW → HIGH) every time a calibrated gas volume passes through the chamber.

AGDAC works as follows:

1. Each MGC sends a **binary pulse** to an Arduino digital input
2. The Arduino counts pulses for each channel
3. Each pulse is converted into **true gas volume** using the MGC-specific calibration factor
4. Volume data is streamed via **USB serial**
5. Python receives, displays, and stores the data in **CSV format**

This workflow is illustrated in **Figure 2** of the hardware paper :contentReference[oaicite:1]{index=1}.

The mathematical conversion is:

\[
V_{j,i} = CF_j \times NT_i
\]

Where:
- \(V_{j,i}\) = gas volume of channel *j* at time *i*
- \(CF_j\) = calibration factor (mL per pulse) of MGC *j*
- \(NT_i\) = cumulative number of tilt pulses :contentReference[oaicite:2]{index=2}

---

## 2. Repository structure

This repository follows the official AGDAC data pipeline:

AGDAC/
│
├── Cod_Gas.py
├── AGDAC_AR.ino
│
├── temporary_measurements/
│ └── (buffered raw serial data)
│
└── measurements/
└── (validated CSV experiment logs)


The directory roles are defined as:

| Folder | Function |
|------|---------|
| `temporary_measurements/` | Holds raw serial data during active acquisition before validation |
| `measurements/` | Stores finalized experiment datasets for scientific analysis |

This design prevents corruption of real-time acquisition while enabling safe long-term storage :contentReference[oaicite:3]{index=3}.

---

## 3. Arduino firmware (`AGDAC_AR.ino`)

The Arduino firmware is responsible for:

- Configuring digital pins as **INPUT_PULLUP**
- Detecting **HIGH → LOW transitions** (tilting events)
- Counting pulses per channel
- Converting pulses to gas volume
- Streaming data via **Serial**

Each MGC is connected to:
- **One digital pin** (signal)
- **One common GND**

The pull-up resistor ensures that the line remains HIGH unless a magnetic pulse pulls it LOW during bucket tilt :contentReference[oaicite:4]{index=4}.

Key parameters defined in the firmware:

| Variable | Meaning |
|--------|--------|
| `PinSensors[]` | Digital pins connected to each MGC |
| `VolChamber[]` | Volume (mL) per tilt of each MGC |
| `period` | Reporting interval in milliseconds |
| `Serial.begin(9600)` | Communication speed |

Each pulse increments a counter `NT_i`, which is multiplied by `VolChamber` to compute true gas volume :contentReference[oaicite:5]{index=5}.

---

## 4. Python acquisition software (`Cod_Gas.py`)

The Python program is the **control and data-logging layer**.

Its responsibilities are:

- Open the serial port
- Read incoming volume streams
- Display time-resolved gas production
- Store CSV files at user-defined intervals

User-defined inputs:

| Parameter | Function |
|---------|--------|
| `arduino_port` | COM port where Arduino is connected |
| `baud_rate` | Must match Arduino (default: 9600) |
| `SavingPeriod` | Interval for writing CSV snapshots |

Before starting, all files inside `temporary_measurements/` must be cleared to prevent mixing experiments :contentReference[oaicite:6]{index=6}.

---

## 5. Hardware requirements

A minimal 3-channel AGDAC requires:

| Component | Quantity |
|---------|----------|
| Arduino Uno (ATmega328P) | 1 |
| Stereo jack sockets | 3 |
| USB cable | 1 |
| 12 V power supply | 1 |
| Wiring, PCB, enclosure | As needed |

Total cost: **~$106 USD for 3 channels**, **~$113 for >3 channels** :contentReference[oaicite:7]{index=7}.

The system scales up to **13 MGC channels** per Arduino.

---

## 6. Why AGDAC instead of Rigamo?

| Feature | Rigamo (Commercial) | AGDAC |
|-------|-------------------|-------|
| Hardware | NI DAQ | Arduino Uno |
| Software | LabVIEW (licensed) | Python (free) |
| Channels | License-limited | 13 per board |
| OS | Windows only | Windows, Linux, macOS |
| Cost | > $2,000 | < $120 |
| File format | Excel | CSV |
| Parallel systems | No | Yes |

---

## 7. Scientific validation

AGDAC was validated against commercial **Ritter MGC + Rigamo** systems using three anaerobic digesters.

The recorded gas volumes matched in real time, except in cases where MGC batteries failed, where AGDAC **outperformed** the proprietary logger by detecting pulses lost by the MGC electronics :contentReference[oaicite:9]{index=9}.

---

## 8. Citation

If you use this system in scientific work, cite:

> Flores-Rodriguez, C., & Mockaitis, G.  
> *The AGDAC: An Innovative Market-Oriented, Open-Source Multiplexing System for Advanced Biogas Volume Measurements in Research Experiments*  
> SSRN 4942112

---

## 9. License

Hardware: **CC BY-NC-SA 4.0**  
Software: Open-source (Arduino + Python)
