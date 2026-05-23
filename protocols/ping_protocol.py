import time
import struct
import hashlib
import zlib
import os
import random

class PingProtocol:
    def __init__(self):
        self.session = self._session()
        self.seq = 0
        self.sent = 0
        self.received = 0
        self.latencies = []
        self.errors = 0

    def _session(self):
        return hashlib.sha256(os.urandom(32)).hexdigest()[:16]

    def _next_seq(self):
        self.seq += 1
        return self.seq

    def _crc(self, data):
        if isinstance(data, str):
            data = data.encode()
        return zlib.crc32(data) & 0xFFFFFFFF

    def _sha(self, data):
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha256(data).digest()

    def build_ping(self, payload="PING"):
        seq = self._next_seq()
        ts = int(time.time() * 1000)

        if isinstance(payload, str):
            payload = payload.encode()

        crc = self._crc(payload)
        sha = self._sha(payload)

        header = struct.pack(">HIQ", seq, 1, ts)

        packet = (
            header +
            struct.pack(">I", len(payload)) +
            payload +
            struct.pack(">I", crc) +
            sha +
            self.session.encode()
        )

        self.sent += 1
        return packet

    def parse_pong(self, packet):
        try:
            header_size = struct.calcsize(">HIQ")

            seq, flag, ts = struct.unpack(">HIQ", packet[:header_size])

            offset = header_size
            length = struct.unpack(">I", packet[offset:offset+4])[0]

            offset += 4
            payload = packet[offset:offset+length]

            offset += length
            crc = struct.unpack(">I", packet[offset:offset+4])[0]

            offset += 4
            sha = packet[offset:offset+32]

            offset += 32
            session = packet[offset:offset+16].decode(errors="ignore")

            valid_crc = self._crc(payload) == crc
            valid_sha = self._sha(payload) == sha
            valid_session = session == self.session

            valid = valid_crc and valid_sha and valid_session

            if valid:
                self.received += 1
                latency = int(time.time() * 1000) - ts
                self.latencies.append(latency)
            else:
                self.errors += 1

            return {
                "seq": seq,
                "payload": payload,
                "latency": latency if valid else None,
                "crc_ok": valid_crc,
                "sha_ok": valid_sha,
                "session_ok": valid_session,
                "valid": valid
            }

        except Exception as e:
            self.errors += 1
            return {"valid": False, "error": str(e)}

    def ping(self):
        return self.build_ping("PING")

    def random_ping(self, size=16):
        data = bytes(random.getrandbits(8) for _ in range(size))
        return self.build_ping(data)

    def avg_latency(self):
        return sum(self.latencies) / len(self.latencies) if self.latencies else 0

    def status(self):
        return {
            "session": self.session,
            "seq": self.seq,
            "sent": self.sent,
            "received": self.received,
            "avg_latency_ms": self.avg_latency(),
            "errors": self.errors
        }

    def reset(self):
        self.seq = 0
        self.sent = 0
        self.received = 0
        self.latencies = []
        self.errors = 0
        self.session = self._session()


if __name__ == "__main__":
    pp = PingProtocol()

    pkt = pp.ping()
    print(pp.parse_pong(pkt))
    print(pp.status())