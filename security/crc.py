import zlib
import struct
import random
import time

class CRC32Engine:
    def __init__(self):
        self.table = self._generate_table()
        self.history = []

    def _generate_table(self):
        table = []
        for i in range(256):
            crc = i
            for _ in range(8):
                if crc & 1:
                    crc = 0xEDB88320 ^ (crc >> 1)
                else:
                    crc >>= 1
            table.append(crc)
        return table

    def compute(self, data):
        if isinstance(data, str):
            data = data.encode()

        crc = 0xFFFFFFFF
        for b in data:
            crc = self.table[(crc ^ b) & 0xFF] ^ (crc >> 8)

        return crc ^ 0xFFFFFFFF

    def compute_zlib(self, data):
        if isinstance(data, str):
            data = data.encode()
        return zlib.crc32(data) & 0xFFFFFFFF

    def verify(self, data, expected_crc):
        calc = self.compute(data)
        return calc == expected_crc

    def packet_encode(self, payload):
        if isinstance(payload, str):
            payload = payload.encode()

        crc = self.compute(payload)
        size = len(payload)

        packet = struct.pack(">I", size) + payload + struct.pack(">I", crc)
        return packet

    def packet_decode(self, packet):
        if len(packet) < 8:
            return None

        size = struct.unpack(">I", packet[:4])[0]
        payload = packet[4:4+size]
        crc = struct.unpack(">I", packet[4+size:4+size+4])[0]

        valid = self.verify(payload, crc)

        return {
            "size": size,
            "payload": payload,
            "crc": crc,
            "valid": valid
        }

    def fuzz_test(self, iterations=100):
        results = []
        for _ in range(iterations):
            data = bytes([random.randint(0, 255) for _ in range(random.randint(5, 50))])
            crc = self.compute(data)
            check = self.verify(data, crc)
            results.append(check)
        return all(results)

    def stress_test(self, iterations=1000):
        start = time.time()
        for _ in range(iterations):
            data = str(random.randint(0, 999999)).encode()
            self.compute(data)
        return time.time() - start

    def compare(self, data):
        if isinstance(data, str):
            data = data.encode()

        return {
            "custom_crc": self.compute(data),
            "zlib_crc": self.compute_zlib(data)
        }

    def corrupt_test(self, data):
        if isinstance(data, str):
            data = bytearray(data.encode())
        else:
            data = bytearray(data)

        original_crc = self.compute(data)

        for i in range(len(data)):
            mutated = data[:]
            mutated[i] ^= 0xFF
            if self.verify(mutated, original_crc):
                return False

        return True

    def batch_crc(self, data_list):
        return [self.compute(d) for d in data_list]

    def integrity_report(self, data):
        crc = self.compute(data)
        zlib_crc = self.compute_zlib(data)

        return {
            "data_length": len(data) if isinstance(data, (bytes, str)) else 0,
            "crc32": crc,
            "zlib_crc32": zlib_crc,
            "match": crc == zlib_crc
        }

    def history_log(self, data):
        crc = self.compute(data)
        self.history.append({
            "timestamp": time.time(),
            "data": data,
            "crc": crc
        })
        return crc

    def replay_history(self):
        return [
            {
                "data": h["data"],
                "crc": self.compute(h["data"])
            }
            for h in self.history
        ]


if __name__ == "__main__":
    engine = CRC32Engine()

    test_data = "ArduinoWaveHandle"

    print(engine.integrity_report(test_data))
    print(engine.packet_decode(engine.packet_encode(test_data)))
    print(engine.fuzz_test(200))
    print(engine.stress_test(2000))