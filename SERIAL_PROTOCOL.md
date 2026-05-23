````md id="serial001"
# SERIAL_PROTOCOL.md

# ArduinoWaveHandler Serial Protocol Specification

This document defines the internal and external serial communication structure used in ArduinoWaveHandler for Arduino and USB serial devices.

---

# Overview

The Serial Protocol is designed to provide a lightweight, structured communication format between:

- Arduino devices
- USB serial adapters (CH340, CP210x, FTDI)
- Host runtime system (Python engine)

It supports both raw and structured message modes.

---

# Connection Model

## Handshake Flow

1. Host opens serial port
2. Device responds with ID packet
3. Host acknowledges connection
4. Streaming begins

---

# Handshake Packet

## Device → Host

```text id="handshake001"
[AWH:HELLO]
DEVICE=ARDUINO
ID=XXXX
FIRMWARE=1.0
MODE=SERIAL
````

## Host → Device

```text id="handshake002"
[AWH:ACK]
STATUS=OK
MODE=LIVE
INTERVAL=1000
```

---

# Message Format

All messages follow a structured key-value format.

## Standard Packet

```text id="packet001"
[AWH:DATA]
TYPE=EVENT
SOURCE=DEVICE
VALUE=123
TIME=1700000000
```

---

# Event Types

| Type       | Description                 |
| ---------- | --------------------------- |
| CONNECT    | Device connected            |
| DISCONNECT | Device removed              |
| DATA       | Incoming sensor/data stream |
| ERROR      | Device error                |
| HEARTBEAT  | Keep-alive signal           |

---

# Raw Mode

Raw mode sends unstructured serial data:

```text id="raw001"
> 123,456,789
> TEMP:25.6
> OK
```

Used for:

* Sensor streams
* Debug output
* Legacy Arduino sketches

---

# Structured Mode

Structured mode enforces key-value packets:

```text id="structured001"
[AWH:DATA]
TEMP=25.6
HUMID=60
PRESSURE=1013
```

---

# Encoding Rules

* UTF-8 encoding required
* Line-based transmission
* No binary headers by default
* Optional binary mode in future versions

---

# Timing Rules

* Default interval: 1000ms
* Heartbeat interval: 5000ms
* Timeout threshold: 10 seconds

---

# Error Handling

Common errors:

| Code | Meaning          |
| ---- | ---------------- |
| E01  | Device timeout   |
| E02  | Invalid packet   |
| E03  | Connection lost  |
| E04  | Unsupported mode |

---

# Device Identification

Devices may report:

```text id="device001"
VID=xxxx
PID=xxxx
NAME=Arduino Uno
DRIVER=CH340
```

---

# Security Notes

* Protocol is local-only
* No encryption by default
* Intended for trusted environments
* Future versions may include optional encryption layer

---

# Future Extensions

Planned upgrades:

* Binary packet mode
* Encrypted serial mode
* Multi-device multiplexing
* Auto-reconnect system
* Packet compression
* Streaming analytics layer

---

# Integration

This protocol is used by:

* console.py (device display)
* monitor.py (event tracking)
* runtime engine (main loop)

---

# Example Full Session

```text id="session001"
HOST:  [AWH:HELLO]
DEVICE:[AWH:HELLO]

HOST:  [AWH:ACK]
DEVICE:OK

DEVICE:[AWH:DATA]
TEMP=26.1
HUMID=55
```

---

# Status

Current implementation: **Prototype / Structured Text Mode**

```
```
