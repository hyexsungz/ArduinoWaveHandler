# Contributing.md

## ArduinoWaveHandler Contribution Guide

This project is modular, and contributions are welcome in any of the core utility systems, build tools, or device layers.

---

## Code Philosophy

- Keep modules independent
- Avoid unnecessary dependencies
- Maintain consistent logging behavior
- Ensure all functions are testable in isolation
- Prefer clarity over complexity

---

## Project Structure Awareness

Before contributing, understand the architecture:

- `utils/` → Core functional modules
- `build.py` → Build and packaging system
- `logs/` → Runtime logs and debugging output
- `dist/` → Final bundled output
- `core/` → Future runtime engine layer

---

## Contribution Types

You can contribute in the following areas:

### 1. Utility Enhancements
Improve or extend:
- console.py
- file_utils.py
- logger.py
- parser.py
- string_utils.py
- time_utils.py

### 2. Device Layer Expansion
- USB detection improvements
- COM port scanning upgrades
- Driver identification (CH340, CP210x, FTDI)
- Real-time disconnect detection

### 3. Build System Improvements
- Faster scanning
- Better bundling system
- Multi-format output support
- Packaging enhancements

### 4. Core Engine Development
- Event system
- Plugin architecture
- Runtime dispatcher
- Async processing layer

---

## Coding Standards

- Python 3.10+
- No external libraries unless necessary
- Use clear function naming
- Keep functions modular (<100–150 lines preferred)
- Always include error handling
- Maintain consistent logging via logger module

---

## Logging Rules

All contributions MUST use the global logging system:

- info()
- warn()
- error()
- debug()
- success()

No print() in production modules.

---

## Testing Requirements

Before submitting:

- Run `build.py`
- Ensure no syntax errors
- Test module independently
- Validate imports
- Check logs output

---

## Commit Style

Use clear commit messages:

- feat: add new parser feature
- fix: resolve logger crash issue
- update: improve string utilities
- refactor: simplify file utils logic

---

## Pull Request Rules

Include:

- Description of changes
- Affected modules
- Test results
- Any known limitations

---

## Security Notes

- Do NOT introduce network code without review
- Do NOT add external execution features
- Keep system local-first
- Avoid unsafe file operations

---

## Roadmap Awareness

Before contributing, review planned features:

- GUI dashboard
- Real-time device graphing
- Plugin system
- Cross-platform support
- Arduino handshake protocol

---

## Thank You

Every contribution helps evolve ArduinoWaveHandler into a full modular hardware monitoring framework.