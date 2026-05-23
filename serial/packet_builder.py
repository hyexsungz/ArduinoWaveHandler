import struct
import time
import hashlib
import zlib
import random

class PacketBuilder:
    def __init__(self):
        self.sequence = 0
        self.history = []
        self.version = 1

    def _crc(self, data):
        if isinstance(data, str):
            data = data.encode()
        return zlib.crc32(data) & 0xFFFFFFFF

    def _sha(self, data):
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha256(data).digest()

    def _timestamp(self):
        return int(time.time() * 1000)

    def _next_seq(self):
        self.sequence += 1
        return self.sequence

    def build(self, payload, packet_type=1, flags=0):
        if isinstance(payload, str):
            payload = payload.encode()

        seq = self._next_seq()
        ts = self._timestamp()
        length = len(payload)

        crc = self._crc(payload)
        sha = self._sha(payload)

        header = struct.pack(">BHIQ", packet_type, flags, seq, ts)

        packet = (
            header +
            struct.pack(">I", length) +
            payload +
            struct.pack(">I", crc) +
            sha
        )

        self.history.append({
            "seq": seq,
            "type": packet_type,
            "length": length,
            "timestamp": ts
        })

        return packet

    def build_text(self, text):
        return self.build(text, packet_type=1)

    def build_binary(self, data):
        return self.build(data, packet_type=2)

    def build_heartbeat(self):
        return self.build("HEARTBEAT", packet_type=9)

    def build_random(self, size=32):
        data = bytes(random.getrandbits(8) for _ in range(size))
        return self.build(data, packet_type=3)

    def decode(self, packet):
        try:
            header_size = struct.calcsize(">BHIQ")

            packet_type, flags, seq, ts = struct.unpack(">BHIQ", packet[:header_size])

            length_offset = header_size
            length = struct.unpack(">I", packet[length_offset:length_offset+4])[0]

            payload_start = length_offset + 4
            payload_end = payload_start + length

            payload = packet[payload_start:payload_end]

            crc = struct.unpack(">I", packet[payload_end:payload_end+4])[0]
            sha = packet[payload_end+4:payload_end+36]

            valid_crc = (self._crc(payload) == crc)
            valid_sha = (self._sha(payload) == sha)

            return {
                "type": packet_type,
                "flags": flags,
                "seq": seq,
                "timestamp": ts,
                "payload": payload,
                "crc_valid": valid_crc,
                "sha_valid": valid_sha,
                "valid": valid_crc and valid_sha
            }

        except:
            return {"valid": False, "error": "decode_failed"}

    def replay(self):
        return self.history

    def reset(self):
        self.sequence = 0
        self.history = []

    def stress_build(self, count=1000):
        start = time.time()
        for _ in range(count):
            self.build_random(64)
        return time.time() - start


if __name__ == "__main__":
    pb = PacketBuilder()

    pkt = pb.build_text("ArduinoWaveSystem")
    print(pb.decode(pkt))
    print(pb.stress_build(500))