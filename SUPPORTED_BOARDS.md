````md id="boards001"
# SUPPORTED_BOARDS.md

# ArduinoWaveHandler Supported Boards

This document lists supported and partially supported boards for ArduinoWaveHandler's device detection, serial monitoring, and runtime integration layer.

---

# Overview

ArduinoWaveHandler does not flash firmware or modify boards. It only detects, identifies, and communicates with them through serial/USB interfaces.

Support is based on:

- USB VID/PID detection
- Serial port enumeration
- Driver identification
- Communication stability

---

# Fully Supported Boards

## Arduino Official Boards

### Arduino Uno
- USB: ATmega16U2 / CH340 (clone variants)
- Serial: Fully supported
- Detection: HIGH accuracy

### Arduino Mega 2560
- USB: ATmega16U2 / CH340
- Serial: Fully supported
- Detection: HIGH accuracy

### Arduino Nano
- USB: FTDI / CH340 (clone dependent)
- Serial: Fully supported
- Detection: HIGH accuracy

### Arduino Leonardo
- USB: Native USB (ATmega32u4)
- Serial: Supported via HID + serial bridge

### Arduino Micro
- USB: Native USB (ATmega32u4)
- Serial: Supported

---

# Common Clone Chips

## CH340 / CH341
- Most common Arduino clone USB bridge
- Fully supported
- Auto-detected via driver signature

## CP210x (Silicon Labs)
- Widely used in dev boards
- Fully supported
- Stable detection

## FTDI (FT232 series)
- Older but reliable USB-serial bridge
- Fully supported
- High compatibility

---

# Semi-Supported Boards

## ESP8266
- Serial communication supported
- WiFi features not handled
- Detection: MEDIUM accuracy

## ESP32
- Serial + debug monitoring supported
- Advanced features not included yet
- Detection: MEDIUM accuracy

## STM32 Boards
- Basic serial support only
- Requires manual COM selection sometimes
- Detection: LOW to MEDIUM accuracy

---

# Experimental Support

## Raspberry Pi Pico (RP2040)
- USB serial supported
- UF2 flashing NOT supported
- Detection: LOW accuracy

## Generic USB Devices
- Any serial-compliant device
- Detection based on COM enumeration only

---

# Unsupported Devices

- JTAG-only debuggers
- Proprietary encrypted USB devices
- Bluetooth-only embedded systems (without serial bridge)
- Non-serial HID devices (unless extended module added)

---

# Detection Methods

ArduinoWaveHandler uses:

## 1. COM Port Scanning
- Detects available serial ports

## 2. Driver Identification
- CH340
- CP210x
- FTDI
- Windows device descriptors

## 3. VID/PID Matching (planned expansion)
- More accurate hardware classification

---

# Device Classification Levels

| Level | Meaning |
|------|--------|
| HIGH | Fully identified board |
| MEDIUM | Partially identified device |
| LOW | Generic serial device |

---

# Example Detection Output

```text id="detect001"
COM3 → Arduino Uno (CH340)
COM4 → USB Serial Device (CP210x)
COM7 → Unknown Serial Device
````

---

# Limitations

* No firmware flashing support
* No deep hardware control
* No JTAG debugging
* No GPIO control layer yet
* Limited ESP integration

---

# Future Improvements

## Planned Features

* VID/PID full database integration
* Auto board classification engine
* Firmware handshake detection
* ESP32 deep integration layer
* Raspberry Pi Pico full support
* USB topology mapping

---

# Architecture Link

This module integrates with:

* console.py (display layer)
* monitor.py (device tracking)
* signals.json (event system)
* runtime engine (event processing)

---

# Status

Current support level:

```text id="status001"
Prototype Hardware Detection Layer
```

```
```
