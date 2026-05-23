import time
import struct
import hashlib
import zlib
import os

class AVRProtocol:
    def __init__(self):
        self.seq = 0
        self.session = self._session_id()
        self.sent = 0
        self.received = 0
        self.errors = 0

    def _session_id(self):
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

    def build_frame(self, payload, frame_type=1, flags=0):
        if isinstance(payload, str):
            payload = payload.encode()

        seq = self._next_seq()
        ts = int(time.time() * 1000)
        length = len(payload)

        crc = self._crc(payload)
        sha = self._sha(payload)

        header = struct.pack(">BHIQ", frame_type, flags, seq, ts)

        frame = (
            header +
            struct.pack(">I", length) +
            payload +
            struct.pack(">I", crc) +
            sha +
            self.session.encode()
        )

        self.sent += 1
        return frame

    def parse_frame(self, frame):
        try:
            header_size = struct.calcsize(">BHIQ")

            frame_type, flags, seq, ts = struct.unpack(">BHIQ", frame[:header_size])

            offset = header_size
            length = struct.unpack(">I", frame[offset:offset+4])[0]

            offset += 4
            payload = frame[offset:offset+length]

            offset += length
            crc = struct.unpack(">I", frame[offset:offset+4])[0]

            offset += 4
            sha = frame[offset:offset+32]

            offset += 32
            session = frame[offset:offset+16].decode(errors="ignore")

            valid_crc = self._crc(payload) == crc
            valid_sha = self._sha(payload) == sha
            valid_session = session == self.session

            valid = valid_crc and valid_sha and valid_session

            if valid:
                self.received += 1
            else:
                self.errors += 1

            return {
                "type": frame_type,
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

    def heartbeat(self):
        return self.build_frame("HEARTBEAT", frame_type=9)

    def ping(self):
        return self.build_frame("PING", frame_type=10)

    def status(self):
        return {
            "session": self.session,
            "seq": self.seq,
            "sent": self.sent,
            "received": self.received,
            "errors": self.errors
        }

    def reset(self):
        self.seq = 0
        self.sent = 0
        self.received = 0
        self.errors = 0
        self.session = self._session_id()

    def stress_test(self, count=1000):
        start = time.time()
        for _ in range(count):
            self.build_frame("TEST_PAYLOAD", frame_type=1)
        return time.time() - start


if __name__ == "__main__":
    avr = AVRProtocol()

    f = avr.build_frame("ARDUINO AVR TEST")
    print(avr.parse_frame(f))
    print(avr.status())