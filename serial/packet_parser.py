import struct
import zlib
import hashlib
import time

class PacketParser:
    def __init__(self):
        self.errors = []
        self.parsed = []
        self.stats_data = {
            "total": 0,
            "valid": 0,
            "invalid": 0
        }

    def _crc(self, data):
        if isinstance(data, str):
            data = data.encode()
        return zlib.crc32(data) & 0xFFFFFFFF

    def _sha(self, data):
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha256(data).digest()

    def parse(self, packet):
        self.stats_data["total"] += 1

        try:
            if len(packet) < 20:
                self.stats_data["invalid"] += 1
                return {"valid": False, "error": "too_short"}

            header_size = struct.calcsize(">BHIQ")
            packet_type, flags, seq, ts = struct.unpack(">BHIQ", packet[:header_size])

            length_offset = header_size
            length = struct.unpack(">I", packet[length_offset:length_offset + 4])[0]

            payload_start = length_offset + 4
            payload_end = payload_start + length

            payload = packet[payload_start:payload_end]

            crc = struct.unpack(">I", packet[payload_end:payload_end + 4])[0]
            sha = packet[payload_end + 4:payload_end + 36]

            calc_crc = self._crc(payload)
            calc_sha = self._sha(payload)

            crc_ok = (crc == calc_crc)
            sha_ok = (sha == calc_sha)

            valid = crc_ok and sha_ok

            result = {
                "valid": valid,
                "type": packet_type,
                "flags": flags,
                "seq": seq,
                "timestamp": ts,
                "payload": payload,
                "crc_ok": crc_ok,
                "sha_ok": sha_ok
            }

            self.parsed.append(result)

            if valid:
                self.stats_data["valid"] += 1
            else:
                self.stats_data["invalid"] += 1
                self.errors.append(result)

            return result

        except Exception as e:
            self.stats_data["invalid"] += 1
            err = {"valid": False, "error": str(e)}
            self.errors.append(err)
            return err

    def parse_stream(self, stream):
        results = []
        for packet in stream:
            results.append(self.parse(packet))
        return results

    def is_valid(self, packet):
        return self.parse(packet).get("valid", False)

    def get_payload(self, packet):
        result = self.parse(packet)
        return result.get("payload", None)

    def stats(self):
        total = self.stats_data["total"]
        valid = self.stats_data["valid"]
        invalid = self.stats_data["invalid"]

        return {
            "total": total,
            "valid": valid,
            "invalid": invalid,
            "success_rate": (valid / total * 100) if total else 0
        }

    def reset(self):
        self.errors = []
        self.parsed = []
        self.stats_data = {"total": 0, "valid": 0, "invalid": 0}

    def replay(self):
        return self.parsed

    def debug_dump(self):
        return {
            "errors": self.errors,
            "parsed": self.parsed,
            "stats": self.stats()
        }


if __name__ == "__main__":
    p = PacketParser()

    fake = b"\x01\x00\x01\x00\x00\x00\x05hello" + b"\x00\x00\x00\x00" + b"\x00"*32
    print(p.parse(fake))
    print(p.stats())