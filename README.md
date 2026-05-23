# ArduinoWaveHandler

ArduinoWaveHandler is a modular Python-based hardware monitoring and runtime utility framework focused on live USB/COM device tracking, logging, parsing, and real-time terminal monitoring.

The project is designed around a layered architecture where utility modules operate independently while sharing a unified runtime environment.

---

# Features

- Live USB and COM monitoring
- Real-time terminal device engine
- Disconnect and reconnect tracking
- File utility abstraction layer
- Multi-level logging system
- Parsing and encoding toolkit
- String processing utilities
- Time and stopwatch engine
- Modular build system
- Threaded monitoring runtime
- Configurable runtime settings
- JSON-based configuration layer

---

# Live Monitoring Engine

The monitoring engine continuously scans connected hardware devices and tracks:

- COM ports
- USB serial adapters
- CH340 devices
- CP210x devices
- FTDI adapters
- Runtime device changes

The terminal stays active while scanning and updates in real-time.

Example:

```text id="live01"
ArduinoWaveHandler LIVE DEVICE ENGINE
TIME 21:38:18
UPTIME 110s
SCAN 94
EVENT STABLE LINK

DEVICES
COMM
COM3
CH340 USB SERIAL