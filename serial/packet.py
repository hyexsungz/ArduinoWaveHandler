import struct
import time
import zlib
import hashlib
import os
import random

class Packet:
    def __init__(self):
        self.counter = 0
        self.created_packets = []
        self.version = 1
        self.secret = self._gen_secret()

    def _gen_secret(self):
        return hashlib.sha256(os.urandom(32)).digest()

    def _crc(self, data):
        if isinstance(data, str):
            data = data.encode()
        return zlib.crc32(data) & 0xFFFFFFFF

    def _sha(self, data):
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha256(data).digest()

    def _time(self):
        return int(time.time() * 1000)

    def _seq(self):
        self.counter += 1
        return self.counter

    def build(self, payload, ptype=1, flags=0):
        if isinstance(payload, str):
            payload = payload.encode()

        seq = self._seq()
        ts = self._time()
        length = len(payload)

        crc = self._crc(payload)
        sha = self._sha(payload)

        auth = self._sha(payload + self.secret)[:16]

        header = struct.pack(">BHIQ", ptype, flags, seq, ts)

        packet = (
            header +
            struct.pack(">I", length) +
            payload +
            struct.pack(">I", crc) +
            sha +
            auth
        )

        self.created_packets.append({
            "seq": seq,
            "type": ptype,
            "length": length,
            "timestamp": ts
        })

        return packet

    def decode(self, packet):
        try:
            header_size = struct.calcsize(">BHIQ")

            ptype, flags, seq, ts = struct.unpack(">BHIQ", packet[:header_size])

            offset = header_size
            length = struct.unpack(">I", packet[offset:offset+4])[0]

            offset += 4
            payload = packet[offset:offset+length]

            offset += length
            crc = struct.unpack(">I", packet[offset:offset+4])[0]

            offset += 4
            sha = packet[offset:offset+32]

            offset += 32
            auth = packet[offset:offset+16]

            valid_crc = (self._crc(payload) == crc)
            valid_sha = (self._sha(payload) == sha)
            valid_auth = (self._sha(payload + self.secret)[:16] == auth)

            return {
                "type": ptype,
                "flags": flags,
                "seq": seq,
                "timestamp": ts,
                "payload": payload,
                "crc_ok": valid_crc,
                "sha_ok": valid_sha,
                "auth_ok": valid_auth,
                "valid": valid_crc and valid_sha and valid_auth
            }

        except:
            return {"valid": False, "error": "decode_failed"}

    def build_text(self, text):
        return self.build(text, ptype=1)

    def build_binary(self, data):
        return self.build(data, ptype=2)

    def build_heartbeat(self):
        return self.build("HEARTBEAT", ptype=9)

    def build_random(self, size=32):
        data = os.urandom(size)
        return self.build(data, ptype=3)

    def stress(self, n=1000):
        start = time.time()
        for _ in range(n):
            self.build_random(64)
        return time.time() - start

    def replay(self):
        return self.created_packets

    def reset(self):
        self.counter = 0
        self.created_packets = []

    def verify_packet(self, packet):
        return self.decode(packet).get("valid", False)


if __name__ == "__main__":
    p = Packet()

    pkt = p.build_text("ArduinoWaveSystemSecure")
    print(p.decode(pkt))
    print(p.verify_packet(pkt))
    print(p.stress(500))