import time
import hashlib
import secrets
import struct
import zlib
import os

class Handshake:
    def __init__(self):
        self.session_id = self._session()
        self.challenge = None
        self.established = False

        self.sent = 0
        self.received = 0
        self.failed = 0

        self.history = []

    def _session(self):
        return hashlib.sha256(os.urandom(32)).hexdigest()[:16]

    def _crc(self, data):
        if isinstance(data, str):
            data = data.encode()

        return zlib.crc32(data) & 0xFFFFFFFF

    def _sha(self, data):
        if isinstance(data, str):
            data = data.encode()

        return hashlib.sha256(data).digest()

    def _timestamp(self):
        return int(time.time() * 1000)

    def create_challenge(self):
        token = secrets.token_hex(16)

        self.challenge = {
            "token": token,
            "timestamp": self._timestamp()
        }

        payload = token.encode()

        crc = self._crc(payload)
        sha = self._sha(payload)

        packet = (
            struct.pack(">Q", self.challenge["timestamp"]) +
            struct.pack(">I", len(payload)) +
            payload +
            struct.pack(">I", crc) +
            sha +
            self.session_id.encode()
        )

        self.sent += 1

        self.history.append({
            "event": "challenge_created",
            "timestamp": self._timestamp()
        })

        return packet

    def verify_response(self, packet):
        try:
            offset = 0

            timestamp = struct.unpack(">Q", packet[offset:offset+8])[0]
            offset += 8

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
            valid_session = session == self.session_id

            expected = hashlib.sha256(
                self.challenge["token"].encode()
            ).hexdigest().encode()

            valid_response = payload == expected

            valid = (
                valid_crc and
                valid_sha and
                valid_session and
                valid_response
            )

            if valid:
                self.established = True
                self.received += 1

                self.history.append({
                    "event": "handshake_established",
                    "timestamp": self._timestamp()
                })

            else:
                self.failed += 1

                self.history.append({
                    "event": "handshake_failed",
                    "timestamp": self._timestamp()
                })

            return {
                "valid": valid,
                "crc_ok": valid_crc,
                "sha_ok": valid_sha,
                "session_ok": valid_session,
                "response_ok": valid_response,
                "established": self.established
            }

        except Exception as e:
            self.failed += 1

            return {
                "valid": False,
                "error": str(e)
            }

    def generate_response(self, challenge_packet):
        try:
            offset = 0

            timestamp = struct.unpack(">Q", challenge_packet[offset:offset+8])[0]
            offset += 8

            length = struct.unpack(">I", challenge_packet[offset:offset+4])[0]
            offset += 4

            payload = challenge_packet[offset:offset+length]
            offset += length

            token = payload.decode()

            response_payload = hashlib.sha256(
                token.encode()
            ).hexdigest().encode()

            crc = self._crc(response_payload)
            sha = self._sha(response_payload)

            response = (
                struct.pack(">Q", self._timestamp()) +
                struct.pack(">I", len(response_payload)) +
                response_payload +
                struct.pack(">I", crc) +
                sha +
                self.session_id.encode()
            )

            self.sent += 1

            self.history.append({
                "event": "response_generated",
                "timestamp": self._timestamp()
            })

            return response

        except:
            self.failed += 1
            return b""

    def reset(self):
        self.session_id = self._session()
        self.challenge = None
        self.established = False

        self.sent = 0
        self.received = 0
        self.failed = 0

        self.history = []

    def status(self):
        return {
            "session_id": self.session_id,
            "established": self.established,
            "sent": self.sent,
            "received": self.received,
            "failed": self.failed,
            "history": len(self.history)
        }

    def pretty_print(self):
        print("============================================================")
        print("               ARDUINOWAVEHANDLER HANDSHAKE")
        print("============================================================")
        print("SESSION ID  :", self.session_id)
        print("ESTABLISHED :", self.established)
        print("SENT        :", self.sent)
        print("RECEIVED    :", self.received)
        print("FAILED      :", self.failed)
        print("============================================================")


if __name__ == "__main__":
    server = Handshake()
    client = Handshake()

    client.session_id = server.session_id

    challenge = server.create_challenge()

    response = client.generate_response(challenge)

    result = server.verify_response(response)

    print(result)

    server.pretty_print()