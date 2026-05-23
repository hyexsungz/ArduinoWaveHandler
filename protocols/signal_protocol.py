import time
import struct
import hashlib
import zlib
import os
import math
import random

class SignalProtocol:
    def __init__(self):
        self.session = self._session()
        self.seq = 0
        self.sent = 0
        self.received = 0
        self.errors = 0
        self.signal_history = []

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

    def _generate_wave(self, amplitude=1.0, frequency=1.0, samples=32):
        wave = []
        for i in range(samples):
            value = amplitude * math.sin(2 * math.pi * frequency * (i / samples))
            wave.append(int((value + 1) * 127))
        return bytes(wave)

    def build_signal(self, payload, signal_type=1, flags=0):
        if isinstance(payload, str):
            payload = payload.encode()

        seq = self._next_seq()
        ts = int(time.time() * 1000)

        crc = self._crc(payload)
        sha = self._sha(payload)

        header = struct.pack(">BHIQ", signal_type, flags, seq, ts)

        packet = (
            header +
            struct.pack(">I", len(payload)) +
            payload +
            struct.pack(">I", crc) +
            sha +
            self.session.encode()
        )

        self.sent += 1
        self.signal_history.append({
            "seq": seq,
            "type": signal_type,
            "ts": ts
        })

        return packet

    def parse_signal(self, packet):
        try:
            header_size = struct.calcsize(">BHIQ")

            signal_type, flags, seq, ts = struct.unpack(">BHIQ", packet[:header_size])

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
            else:
                self.errors += 1

            return {
                "type": signal_type,
                "flags": flags,
                "seq": seq,
                "timestamp": ts,
                "payload": payload,
                "crc_ok": valid_crc,
                "sha_ok": valid_sha,
                "session_ok": valid_session,
                "valid": valid
            }

        except Exception as e:
            self.errors += 1
            return {"valid": False, "error": str(e)}

    def generate_wave_signal(self):
        wave = self._generate_wave(amplitude=1.0, frequency=random.uniform(0.5, 5.0))
        return self.build_signal(wave, signal_type=2)

    def send_digital_signal(self, state):
        payload = b"HIGH" if state else b"LOW"
        return self.build_signal(payload, signal_type=3)

    def send_analog_signal(self, value):
        payload = str(int(value)).encode()
        return self.build_signal(payload, signal_type=4)

    def status(self):
        return {
            "session": self.session,
            "seq": self.seq,
            "sent": self.sent,
            "received": self.received,
            "errors": self.errors
        }

    def reset(self):
        self.session = self._session()
        self.seq = 0
        self.sent = 0
        self.received = 0
        self.errors = 0
        self.signal_history = []


if __name__ == "__main__":
    sp = SignalProtocol()

    pkt = sp.generate_wave_signal()
    print(sp.parse_signal(pkt))
    print(sp.status())