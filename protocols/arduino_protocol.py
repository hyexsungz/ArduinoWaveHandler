import time
import struct
import hashlib
import zlib

class ArduinoProtocol:
    def __init__(self):
        self.version = 1
        self.sequence = 0
        self.session_id = self._gen_session()
        self.sent = 0
        self.received = 0
        self.errors = 0

    def _gen_session(self):
        return hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]

    def _next_seq(self):
        self.sequence += 1
        return self.sequence

    def _crc(self, data):
        if isinstance(data, str):
            data = data.encode()
        return zlib.crc32(data) & 0xFFFFFFFF

    def _sha(self, data):
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha256(data).digest()

    def build_packet(self, payload, ptype=1, flags=0):
        if isinstance(payload, str):
            payload = payload.encode()

        seq = self._next_seq()
        ts = int(time.time() * 1000)
        length = len(payload)

        crc = self._crc(payload)
        sha = self._sha(payload)

        header = struct.pack(">BHIQ", ptype, flags, seq, ts)

        packet = (
            header +
            struct.pack(">I", length) +
            payload +
            struct.pack(">I", crc) +
            sha +
            self.session_id.encode()
        )

        self.sent += 1
        return packet

    def parse_packet(self, packet):
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
            session = packet[offset:offset+16].decode(errors="ignore")

            valid_crc = (self._crc(payload) == crc)
            valid_sha = (self._sha(payload) == sha)
            valid_session = (session == self.session_id)

            if not (valid_crc and valid_sha and valid_session):
                self.errors += 1

            else:
                self.received += 1

            return {
                "type": ptype,
                "flags": flags,
                "seq": seq,
                "timestamp": ts,
                "payload": payload,
                "crc_ok": valid_crc,
                "sha_ok": valid_sha,
                "session_ok": valid_session,
                "valid": valid_crc and valid_sha and valid_session
            }

        except Exception as e:
            self.errors += 1
            return {"valid": False, "error": str(e)}

    def heartbeat(self):
        return self.build_packet("HEARTBEAT", ptype=9)

    def status(self):
        return {
            "session": self.session_id,
            "sent": self.sent,
            "received": self.received,
            "errors": self.errors
        }

    def reset(self):
        self.sequence = 0
        self.sent = 0
        self.received = 0
        self.errors = 0
        self.session_id = self._gen_session()


if __name__ == "__main__":
    proto = ArduinoProtocol()

    pkt = proto.build_packet("HELLO ARDUINO")
    print(proto.parse_packet(pkt))
    print(proto.status())