import sys
import time
import json
import serial
import serial.tools.list_ports
from datetime import datetime

class BaudrateScanner:
    def __init__(self):
        self.common_baudrates = [
            300,
            1200,
            2400,
            4800,
            9600,
            14400,
            19200,
            28800,
            31250,
            38400,
            56000,
            57600,
            74880,
            115200,
            128000,
            230400,
            250000,
            460800,
            500000,
            576000,
            921600,
            1000000,
            1152000,
            1500000,
            2000000
        ]
        self.timeout = 2
        self.scan_delay = 1.0
        self.output_data = []

    def timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def log(self, message):
        print(f"[{self.timestamp()}] {message}")

    def list_ports(self):
        ports = serial.tools.list_ports.comports()
        available = []

        for port in ports:
            available.append({
                "device": port.device,
                "description": port.description,
                "manufacturer": port.manufacturer,
                "hwid": port.hwid
            })

        return available

    def display_ports(self):
        ports = self.list_ports()

        if not ports:
            self.log("No serial devices found")
            return False

        self.log("Detected serial ports")

        for idx, port in enumerate(ports):
            print("")
            print(f"Index         : {idx}")
            print(f"Device        : {port['device']}")
            print(f"Description   : {port['description']}")
            print(f"Manufacturer  : {port['manufacturer']}")
            print(f"HWID          : {port['hwid']}")

        return True

    def choose_port(self):
        ports = self.list_ports()

        if not ports:
            return None

        while True:
            try:
                value = input("\nSelect port index: ").strip()

                if value.lower() == "exit":
                    return None

                index = int(value)

                if index < 0 or index >= len(ports):
                    self.log("Invalid selection")
                    continue

                return ports[index]["device"]

            except KeyboardInterrupt:
                return None

            except:
                self.log("Invalid input")

    def analyze_response(self, data):
        if not data:
            return False

        printable = 0

        for byte in data:
            if 32 <= byte <= 126 or byte in [10, 13, 9]:
                printable += 1

        ratio = printable / len(data)

        return ratio > 0.6

    def normalize_text(self, data):
        try:
            return data.decode(errors="ignore").strip()
        except:
            return repr(data)

    def scan_baudrate(self, port, baudrate):
        result = {
            "port": port,
            "baudrate": baudrate,
            "success": False,
            "data": "",
            "bytes": 0,
            "timestamp": self.timestamp()
        }

        try:
            self.log(f"Opening {port} at {baudrate}")

            ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=self.timeout,
                write_timeout=self.timeout
            )

            time.sleep(self.scan_delay)

            ser.reset_input_buffer()
            ser.reset_output_buffer()

            try:
                ser.write(b'\n')
                ser.flush()
            except:
                pass

            time.sleep(0.5)

            collected = bytearray()

            start = time.time()

            while time.time() - start < self.timeout:
                waiting = ser.in_waiting

                if waiting > 0:
                    data = ser.read(waiting)
                    collected.extend(data)

                time.sleep(0.05)

            ser.close()

            result["bytes"] = len(collected)

            if collected:
                result["data"] = self.normalize_text(collected)

                if self.analyze_response(collected):
                    result["success"] = True

            return result

        except serial.SerialException as e:
            result["data"] = str(e)
            return result

        except Exception as e:
            result["data"] = str(e)
            return result

    def full_scan(self, port):
        self.log(f"Starting baudrate scan on {port}")

        success_count = 0

        for baudrate in self.common_baudrates:
            result = self.scan_baudrate(port, baudrate)

            self.output_data.append(result)

            print("")
            print("=" * 70)
            print(f"PORT        : {result['port']}")
            print(f"BAUDRATE    : {result['baudrate']}")
            print(f"SUCCESS     : {result['success']}")
            print(f"BYTES       : {result['bytes']}")
            print(f"TIMESTAMP   : {result['timestamp']}")
            print("-" * 70)

            if result["data"]:
                print(result["data"])
            else:
                print("No readable data")

            print("=" * 70)

            if result["success"]:
                success_count += 1

            time.sleep(0.5)

        self.log(f"Finished scanning with {success_count} successful baudrate matches")

    def save_results(self, filename="baudrate_results.json"):
        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(self.output_data, file, indent=4)

            self.log(f"Results saved to {filename}")

        except Exception as e:
            self.log(f"Failed to save results: {e}")

    def interactive_monitor(self, port, baudrate):
        try:
            ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=0.1
            )

            self.log(f"Connected to {port} at {baudrate}")
            self.log("Press CTRL+C to exit")

            while True:
                if ser.in_waiting:
                    data = ser.read(ser.in_waiting)

                    try:
                        text = data.decode(errors="ignore")
                        sys.stdout.write(text)
                        sys.stdout.flush()

                    except:
                        print(repr(data))

                time.sleep(0.01)

        except KeyboardInterrupt:
            self.log("Monitor stopped")

        except Exception as e:
            self.log(f"Monitor error: {e}")

    def menu(self):
        while True:
            print("")
            print("=" * 60)
            print("SERIAL BAUDRATE TOOL")
            print("=" * 60)
            print("1. List serial ports")
            print("2. Scan baudrates")
            print("3. Monitor serial device")
            print("4. Save last results")
            print("5. Exit")
            print("=" * 60)

            choice = input("Select option: ").strip()

            if choice == "1":
                self.display_ports()

            elif choice == "2":
                if not self.display_ports():
                    continue

                port = self.choose_port()

                if not port:
                    continue

                self.full_scan(port)

            elif choice == "3":
                if not self.display_ports():
                    continue

                port = self.choose_port()

                if not port:
                    continue

                baud = input("Enter baudrate: ").strip()

                try:
                    baud = int(baud)
                    self.interactive_monitor(port, baud)

                except:
                    self.log("Invalid baudrate")

            elif choice == "4":
                filename = input("Filename: ").strip()

                if not filename:
                    filename = "baudrate_results.json"

                self.save_results(filename)

            elif choice == "5":
                self.log("Exiting")
                break

            else:
                self.log("Unknown option")

def main():
    scanner = BaudrateScanner()
    scanner.menu()

if __name__ == "__main__":
    main()