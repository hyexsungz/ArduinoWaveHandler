import time
import os
import hmac
import hashlib
import random
import struct

class SecureHandshake:
    def __init__(self):
        self.sessions = {}
        self.nonces = {}
        self.keys = {}
        self.expiry = 300

    def _gen_key(self):
        return hashlib.sha256(os.urandom(32)).digest()

    def _gen_nonce(self):
        return os.urandom(16)

    def _sign(self, key, msg):
        return hmac.new(key, msg, hashlib.sha256).digest()

    def init_handshake(self, device_id):
        key = self._gen_key()
        nonce = self._gen_nonce()

        self.keys[device_id] = key
        self.nonces[device_id] = nonce

        packet = struct.pack(">I", len(device_id)) + device_id.encode() + nonce

        return {
            "step": "challenge",
            "device_id": device_id,
            "nonce": nonce,
            "packet": packet
        }

    def respond_handshake(self, device_id, client_nonce=None):
        if device_id not in self.keys:
            return {"status": "error", "reason": "no_init"}

        server_key = self.keys[device_id]
        server_nonce = self.nonces[device_id]

        client_nonce = client_nonce or self._gen_nonce()

        signature = self._sign(server_key, server_nonce + client_nonce)

        session_token = hashlib.sha256(server_nonce + client_nonce + server_key).hexdigest()

        self.sessions[device_id] = {
            "token": session_token,
            "created": time.time()
        }

        return {
            "step": "response",
            "device_id": device_id,
            "client_nonce": client_nonce,
            "signature": signature,
            "session": session_token
        }

    def verify_session(self, device_id, token):
        if device_id not in self.sessions:
            return False

        session = self.sessions[device_id]

        if time.time() - session["created"] > self.expiry:
            del self.sessions[device_id]
            return False

        return hmac.compare_digest(session["token"], token)

    def revoke(self, device_id):
        self.sessions.pop(device_id, None)
        self.keys.pop(device_id, None)
        self.nonces.pop(device_id, None)

    def status(self, device_id):
        return {
            "active": device_id in self.sessions,
            "has_key": device_id in self.keys,
            "has_nonce": device_id in self.nonces
        }

    def cleanup(self):
        now = time.time()
        expired = []

        for device_id, session in self.sessions.items():
            if now - session["created"] > self.expiry:
                expired.append(device_id)

        for d in expired:
            del self.sessions[d]


if __name__ == "__main__":
    sh = SecureHandshake()

    init = sh.init_handshake("arduino_uno_001")
    print(init["step"])

    resp = sh.respond_handshake("arduino_uno_001")
    print(sh.verify_session("arduino_uno_001", resp["session"]))