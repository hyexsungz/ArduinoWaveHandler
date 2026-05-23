import time
import struct
import hashlib
import zlib
import os

class BootloaderProtocol:
    def __init__(self):
        self.session = self._session()
        self.seq = 0
        self.state = "IDLE"
        self.sent = 0
        self.ack = 0
        self.nack = 0
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

    def build_packet(self, command, payload=b"", flags=0):
        if isinstance(payload, str):
            payload = payload.encode()
        if isinstance(command, str):
            command = command.encode()

        seq = self._next_seq()
        ts = int(time.time() * 1000)

        body = command + b":" + payload

        length = len(body)
        crc = self._crc(body)
        sha = self._sha(body)

        header = struct.pack(">BHIQ", 1, flags, seq, ts)

        packet = (
            header +
            struct.pack(">I", length) +
            body +
            struct.pack(">I", crc) +
            sha +
            self.session.encode()
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
            body = packet[offset:offset+length]

            offset += length
            crc = struct.unpack(">I", packet[offset:offset+4])[0]

            offset += 4
            sha = packet[offset:offset+32]

            offset += 32
            session = packet[offset:offset+16].decode(errors="ignore")

            valid_crc = self._crc(body) == crc
            valid_sha = self._sha(body) == sha
            valid_session = session == self.session

            valid = valid_crc and valid_sha and valid_session

            if not valid:
                self.errors += 1

            return {
                "seq": seq,
                "flags": flags,
                "timestamp": ts,
                "body": body,
                "crc_ok": valid_crc,
                "sha_ok": valid_sha,
                "session_ok": valid_session,
                "valid": valid
            }

        except Exception as e:
            self.errors += 1
            return {"valid": False, "error": str(e)}

    def command(self, cmd, payload=""):
        return self.build_packet(cmd, payload)

    def start_boot(self):
        self.state = "BOOT"
        return self.command("BOOT_START")

    def send_chunk(self, data):
        return self.command("CHUNK", data)

    def end_boot(self):
        self.state = "DONE"
        return self.command("BOOT_END")

    def ack_packet(self, seq):
        self.ack += 1
        return self.command("ACK", str(seq))

    def nack_packet(self, seq):
        self.nack += 1
        return self.command("NACK", str(seq))

    def status(self):
        return {
            "session": self.session,
            "state": self.state,
            "seq": self.seq,
            "sent": self.sent,
            "ack": self.ack,
            "nack": self.nack,
            "errors": self.errors
        }

    def reset(self):
        self.session = self._session()
        self.seq = 0
        self.state = "IDLE"
        self.sent = 0
        self.ack = 0
        self.nack = 0
        self.errors = 0

    def stress_test(self, n=500):
        start = time.time()
        for _ in range(n):
            self.build_packet("CHUNK", b"DATA")
        return time.time() - start


if __name__ == "__main__":
    bp = BootloaderProtocol()

    pkt = bp.start_boot()
    print(bp.parse_packet(pkt))
    print(bp.status())