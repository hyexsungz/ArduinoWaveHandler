import time
import struct
import hashlib
import zlib
import os
import uuid

class USBSerialProtocol:
    def __init__(self):
        self.device_id = self._device_id()
        self.session = self._session()
        self.seq = 0
        self.sent = 0
        self.received = 0
        self.errors = 0
        self.buffer = bytearray()

    def _device_id(self):
        return uuid.uuid4().hex[:12]

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
            self.device_id.encode() +
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
        self.buffer.extend(data)

    def parse(self):
        results = []

        while True:
            header_size = struct.calcsize(">BHIQ")

            if len(self.buffer) < header_size + 4:
                break

            try:
                frame_type, flags, seq, ts = struct.unpack(
                    ">BHIQ",
                    self.buffer[:header_size]
                )
            except:
                self.errors += 1
                break

            length_offset = header_size
            length = struct.unpack(">I", self.buffer[length_offset:length_offset+4])[0]

            total_size = header_size + 4 + 12 + length + 4 + 32 + 16

            if len(self.buffer) < total_size:
                break

            offset = header_size + 4

            device_id = self.buffer[offset:offset+12].decode(errors="ignore")
            offset += 12

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
                "type": frame_type,
                "flags": flags,
                "seq": seq,
                "timestamp": ts,
                "device_id": device_id,
                "payload": payload,
                "crc_ok": valid_crc,
                "sha_ok": valid_sha,
                "session_ok": valid_session,
                "valid": valid
            })

            self.buffer = self.buffer[total_size:]

        return results

    def send(self, text):
        return self.build_frame(text, frame_type=1)

    def send_binary(self, data):
        return self.build_frame(data, frame_type=2)

    def handshake(self):
        return self.build_frame("HANDSHAKE", frame_type=8)

    def heartbeat(self):
        return self.build_frame("HEARTBEAT", frame_type=9)

    def status(self):
        return {
            "device_id": self.device_id,
            "session": self.session,
            "seq": self.seq,
            "sent": self.sent,
            "received": self.received,
            "errors": self.errors,
            "buffer_size": len(self.buffer)
        }

    def reset(self):
        self.device_id = self._device_id()
        self.session = self._session()
        self.seq = 0
        self.sent = 0
        self.received = 0
        self.errors = 0
        self.buffer = bytearray()


if __name__ == "__main__":
    usb = USBSerialProtocol()

    frame = usb.send("HELLO USB SERIAL")
    usb.feed(frame)

    print(usb.parse())
    print(usb.status())