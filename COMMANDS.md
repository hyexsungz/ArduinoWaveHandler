# COMMANDS.md

## ArduinoWaveHandler Command Reference

This file lists all internal commands, module functions, and runtime utilities available in the system.

---

## Console Commands (utils/console.py)

### scan_devices()
Scans system for connected devices.

### start_monitor()
Starts live monitoring loop for device changes.

### stop_monitor()
Stops live monitoring loop.

### list_ports()
Returns available COM ports.

### render_status()
Displays current system/device status.

---

## File Utilities (utils/file_utils.py)

### exists(path)
Check if file or directory exists.

### read(path)
Read file content.

### write(path, data)
Write data to file.

### append(path, data)
Append data to file.

### delete(path)
Delete file or directory.

### move(src, dst)
Move file or directory.

### copy(src, dst)
Copy file or directory.

### list_dir(path)
List directory contents.

### tree(path)
Recursive directory structure.

### size(path)
Get file or folder size.

### hash_file(path, algo)
Generate file hash.

### temp_file(data)
Create temporary file.

### random_file(folder, size)
Generate random binary file.

---

## Logger (utils/logger.py)

### info(msg)
Log informational message.

### warn(msg)
Log warning message.

### error(msg)
Log error message.

### debug(msg)
Log debug message.

### success(msg)
Log success message.

### exception(e)
Log exception with traceback.

### json(obj)
Log formatted JSON.

### uptime()
Get logger uptime.

### dump_buffer()
Return log buffer.

---

## Parser (utils/parser.py)

### parse_json(data)
Parse JSON string.

### dump_json(obj)
Convert object to JSON string.

### parse_xml(data)
Parse XML string.

### regex(pattern, data)
Run regex search.

### clean(data)
Clean whitespace.

### extract_numbers(data)
Extract numeric values.

### extract_hex(data)
Extract hex values.

### sha256(data)
Generate SHA256 hash.

### md5(data)
Generate MD5 hash.

### b64_encode(data)
Base64 encode.

### b64_decode(data)
Base64 decode.

### url_encode(data)
URL encode string.

### url_decode(data)
URL decode string.

---

## String Utilities (utils/string_utils.py)

### upper(text)
Convert to uppercase.

### lower(text)
Convert to lowercase.

### reverse(text)
Reverse string.

### capitalize(text)
Capitalize first letter.

### title(text)
Title case string.

### strip(text)
Trim whitespace.

### replace(text, old, new)
Replace substring.

### random_string(length)
Generate random string.

### random_hex(length)
Generate random hex.

### sha256(text)
Hash string with SHA256.

### md5(text)
Hash string with MD5.

### b64_encode(text)
Base64 encode.

### b64_decode(text)
Base64 decode.

### regex(pattern, text)
Regex search.

---

## Time Utilities (utils/time_utils.py)

### now()
Get current datetime.

### now_time()
Get current time string.

### now_date()
Get current date.

### timestamp()
Get UNIX timestamp.

### unix_ms()
Get UNIX milliseconds.

### sleep(seconds)
Pause execution.

### format_time(fmt)
Format current time.

### year()
Get current year.

### month()
Get current month.

### day()
Get current day.

### hour()
Get current hour.

### minute()
Get current minute.

### second()
Get current second.

### weekday()
Get weekday name.

### month_name()
Get month name.

### uptime()
Get system uptime.

### countdown(seconds)
Generate countdown list.

### create_timer(name)
Create named timer.

### timer_elapsed(name)
Get timer elapsed time.

### remove_timer(name)
Remove timer.

### start_stopwatch(name)
Start stopwatch.

### stop_stopwatch(name)
Stop stopwatch.

### stopwatch_elapsed(name)
Get stopwatch time.

### parse_date(value)
Parse date string.

### future_timestamp(seconds)
Future timestamp.

### past_timestamp(seconds)
Past timestamp.

---

## Build System (build.py)

### run()
Execute full build pipeline.

### clean()
Clean build directories.

### scan_project()
Scan Python files.

### validate_syntax(files)
Check syntax validity.

### bundle(files)
Merge project into bundle.

### make_manifest(files)
Generate build manifest.

---

## Global Runtime Concepts

### logger
Global logging instance.

### file_utils
Global file handler.

### parser
Global parsing engine.

### string_utils
Global string engine.

### time_utils
Global time engine.

---

## System Flow

1. main.py starts runtime
2. Modules initialize
3. Console begins scanning loop
4. Logger captures all events
5. Parser processes incoming data
6. File system operations executed
7. Time engine tracks lifecycle

---

## Notes

- These are Python-level APIs
- No direct hardware execution commands included
- Designed for modular expansion