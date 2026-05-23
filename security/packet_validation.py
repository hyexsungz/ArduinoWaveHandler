import struct
import time
import hashlib
import zlib

class PacketValidator:
    def __init__(self):
        self.log = []
        self.errors = []
        self.valid_packets = 0
        self.invalid_packets = 0

    def _crc(self, data):
        if isinstance(data, str):
            data = data.encode()
        return zlib.crc32(data) & 0xFFFFFFFF

    def _hash(self, data):
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha256(data).hexdigest()

    def build_packet(self, payload, packet_type=1, seq=0):
        if isinstance(payload, str):
            payload = payload.encode()

        length = len(payload)
        crc = self._crc(payload)
        sha = self._hash(payload)

        header = struct.pack(">BHI", packet_type, seq, length)

        packet = header + payload + struct.pack(">I", crc) + sha.encode()

        return packet

    def parse_packet(self, packet):
        try:
            if len(packet) < 11:
                self.invalid_packets += 1
                return {"valid": False, "error": "too_short"}

            packet_type = struct.unpack(">B", packet[0:1])[0]
            seq = struct.unpack(">H", packet[1:3])[0]
            length = struct.unpack(">I", packet[3:7])[0]

            payload_start = 7
            payload_end = payload_start + length

            payload = packet[payload_start:payload_end]
            crc_start = payload_end
            crc_end = crc_start + 4
            sha_start = crc_end

            if len(packet) < sha_start + 64:
                self.invalid_packets += 1
                return {"valid": False, "error": "corrupt_packet"}

            crc = struct.unpack(">I", packet[crc_start:crc_end])[0]
            sha = packet[sha_start:sha_start+64].decode(errors="ignore")

            calc_crc = self._crc(payload)
            calc_sha = self._hash(payload)

            valid = (crc == calc_crc) and (sha == calc_sha)

            result = {
                "valid": valid,
                "type": packet_type,
                "seq": seq,
                "length": length,
                "payload": payload,
                "crc_ok": crc == calc_crc,
                "sha_ok": sha == calc_sha
            }

            self.log.append(result)

            if valid:
                self.valid_packets += 1
            else:
                self.invalid_packets += 1
                self.errors.append(result)

            return result

        except Exception as e:
            self.invalid_packets += 1
            self.errors.append({"valid": False, "error": str(e)})
            return {"valid": False, "error": str(e)}

    def validate_stream(self, packets):
        results = []
        for p in packets:
            results.append(self.parse_packet(p))
        return results

    def stats(self):
        total = self.valid_packets + self.invalid_packets
        return {
            "total": total,
            "valid": self.valid_packets,
            "invalid": self.invalid_packets,
            "success_rate": (self.valid_packets / total * 100) if total else 0
        }

    def replay_log(self):
        return self.log

    def clear(self):
        self.log = []
        self.errors = []
        self.valid_packets = 0
        self.invalid_packets = 0

    def fuzz_packet(self, payload):
        if isinstance(payload, str):
            payload = payload.encode()

        corrupted = bytearray(payload)

        for i in range(len(corrupted)):
            corrupted[i] ^= 0xAA

        return self.parse_packet(self.build_packet(bytes(corrupted)))


if __name__ == "__main__":
    v = PacketValidator()

    pkt = v.build_packet("ArduinoWavePacket", seq=1)
    print(v.parse_packet(pkt))
    print(v.stats())