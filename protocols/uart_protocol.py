import time
import struct
import hashlib
import zlib
import os

class UARTProtocol:
    def __init__(self):
        self.session = self._session()
        self.seq = 0
        self.sent = 0
        self.received = 0
        self.errors = 0
        self.rx_buffer = bytearray()

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

    def build_frame(self, payload, frame_type=1, flags=0):
        if isinstance(payload, str):
            payload = payload.encode()

        seq = self._next_seq()
        ts = int(time.time() * 1000)

        crc = self._crc(payload)
        sha = self._sha(payload)

        header = struct.pack(">BHIQ", frame_type, flags, seq, ts)

        frame = (
            header +
            struct.pack(">I", len(payload)) +
            payload +
            struct.pack(">I", crc) +
            sha +
            self.session.encode()
        )

        self.sent += 1
        return frame

    def feed(self, data):
        if isinstance(data, str):
            data = data.encode()
        self.rx_buffer.extend(data)

    def parse_stream(self):
        results = []

        while True:
            if len(self.rx_buffer) < struct.calcsize(">BHIQ") + 4:
                break

            header_size = struct.calcsize(">BHIQ")
            try:
                frame_type, flags, seq, ts = struct.unpack(
                    ">BHIQ",
                    self.rx_buffer[:header_size]
                )
            except:
                break

            if len(self.rx_buffer) < header_size + 4:
                break

            length = struct.unpack(">I", self.rx_buffer[header_size:header_size+4])[0]

            total_size = header_size + 4 + length + 4 + 32 + 16

            if len(self.rx_buffer) < total_size:
                break

            offset = header_size + 4
            payload = self.rx_buffer[offset:offset+length]

            offset += length
            crc = struct.unpack(">I", self.rx_buffer[offset:offset+4])[0]

            offset += 4
            sha = self.rx_buffer[offset:offset+32]

            offset += 32
            session = self.rx_buffer[offset:offset+16].decode(errors="ignore")

            valid_crc = self._crc(payload) == crc
            valid_sha = self._sha(payload) == sha
            valid_session = session == self.session

            valid = valid_crc and valid_sha and valid_session

            if valid:
                self.received += 1
            else:
                self.errors += 1

            results.append({
                "type": frame_type,
                "flags": flags,
                "seq": seq,
                "timestamp": ts,
                "payload": payload,
                "crc_ok": valid_crc,
                "sha_ok": valid_sha,
                "session_ok": valid_session,
                "valid": valid
            })

            self.rx_buffer = self.rx_buffer[total_size:]

        return results

    def send_text(self, text):
        return self.build_frame(text, frame_type=1)

    def send_binary(self, data):
        return self.build_frame(data, frame_type=2)

    def heartbeat(self):
        return self.build_frame("HEARTBEAT", frame_type=9)

    def status(self):
        return {
            "session": self.session,
            "seq": self.seq,
            "sent": self.sent,
            "received": self.received,
            "errors": self.errors,
            "buffer_size": len(self.rx_buffer)
        }

    def reset(self):
        self.session = self._session()
        self.seq = 0
        self.sent = 0
        self.received = 0
        self.errors = 0
        self.rx_buffer = bytearray()


if __name__ == "__main__":
    uart = UARTProtocol()

    frame = uart.send_text("HELLO UART")
    uart.feed(frame)

    print(uart.parse_stream())
    print(uart.status())