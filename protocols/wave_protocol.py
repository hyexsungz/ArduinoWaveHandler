import time
import math
import struct
import hashlib
import zlib
import os
import random

class WaveProtocol:
    def __init__(self):
        self.session = self._session()
        self.seq = 0
        self.sent = 0
        self.received = 0
        self.errors = 0
        self.wave_history = []
        self.buffer = bytearray()

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

    def generate_wave(self, amplitude=1.0, frequency=1.0, samples=64):
        values = []

        for i in range(samples):
            angle = 2 * math.pi * frequency * (i / samples)
            wave = amplitude * math.sin(angle)
            normalized = int((wave + 1.0) * 127)
            values.append(normalized)

        return bytes(values)

    def build_wave_packet(self, payload, wave_type=1, flags=0):
        if isinstance(payload, str):
            payload = payload.encode()

        seq = self._next_seq()
        ts = int(time.time() * 1000)

        crc = self._crc(payload)
        sha = self._sha(payload)

        header = struct.pack(">BHIQ", wave_type, flags, seq, ts)

        packet = (
            header +
            struct.pack(">I", len(payload)) +
            payload +
            struct.pack(">I", crc) +
            sha +
            self.session.encode()
        )

        self.sent += 1

        self.wave_history.append({
            "seq": seq,
            "type": wave_type,
            "size": len(payload),
            "timestamp": ts
        })

        return packet

    def feed(self, data):
        if isinstance(data, str):
            data = data.encode()

        self.buffer.extend(data)

    def parse_stream(self):
        results = []

        while True:
            header_size = struct.calcsize(">BHIQ")

            if len(self.buffer) < header_size + 4:
                break

            try:
                wave_type, flags, seq, ts = struct.unpack(
                    ">BHIQ",
                    self.buffer[:header_size]
                )
            except:
                self.errors += 1
                break

            length = struct.unpack(
                ">I",
                self.buffer[header_size:header_size+4]
            )[0]

            total_size = header_size + 4 + length + 4 + 32 + 16

            if len(self.buffer) < total_size:
                break

            offset = header_size + 4

            payload = self.buffer[offset:offset+length]
            offset += length

            crc = struct.unpack(">I", self.buffer[offset:offset+4])[0]
            offset += 4

            sha = self.buffer[offset:offset+32]
            offset += 32

            session = self.buffer[offset:offset+16].decode(errors="ignore")

            valid_crc = self._crc(payload) == crc
            valid_sha = self._sha(payload) == sha
            valid_session = session == self.session

            valid = valid_crc and valid_sha and valid_session

            if valid:
                self.received += 1
            else:
                self.errors += 1

            results.append({
                "type": wave_type,
                "flags": flags,
                "seq": seq,
                "timestamp": ts,
                "payload": payload,
                "crc_ok": valid_crc,
                "sha_ok": valid_sha,
                "session_ok": valid_session,
                "valid": valid
            })

            self.buffer = self.buffer[total_size:]

        return results

    def send_wave(self, amplitude=1.0, frequency=1.0, samples=64):
        wave = self.generate_wave(
            amplitude=amplitude,
            frequency=frequency,
            samples=samples
        )

        return self.build_wave_packet(wave, wave_type=2)

    def send_text(self, text):
        return self.build_wave_packet(text, wave_type=1)

    def send_random_wave(self):
        amp = random.uniform(0.5, 5.0)
        freq = random.uniform(0.5, 10.0)

        return self.send_wave(
            amplitude=amp,
            frequency=freq,
            samples=128
        )

    def heartbeat(self):
        return self.build_wave_packet("HEARTBEAT", wave_type=9)

    def status(self):
        return {
            "session": self.session,
            "seq": self.seq,
            "sent": self.sent,
            "received": self.received,
            "errors": self.errors,
            "buffer_size": len(self.buffer),
            "history_size": len(self.wave_history)
        }

    def reset(self):
        self.session = self._session()
        self.seq = 0
        self.sent = 0
        self.received = 0
        self.errors = 0
        self.wave_history = []
        self.buffer = bytearray()


if __name__ == "__main__":
    wp = WaveProtocol()

    pkt = wp.send_wave(amplitude=2.0, frequency=3.0, samples=32)

    wp.feed(pkt)

    print(wp.parse_stream())
    print(wp.status())