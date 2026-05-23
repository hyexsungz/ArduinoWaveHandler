import time
import hashlib
import hmac
import random
import string

class DeviceAuth:
    def __init__(self):
        self.devices = {}
        self.sessions = {}
        self.failed_attempts = {}
        self.secret = self._generate_secret()
        self.blocked = set()

    def _generate_secret(self):
        seed = str(time.time()).encode()
        return hashlib.sha256(seed).digest()

    def _hash_device(self, device_id):
        return hashlib.sha256(device_id.encode()).hexdigest()

    def register_device(self, device_id, metadata=None):
        did = self._hash_device(device_id)
        self.devices[did] = {
            "device_id": device_id,
            "metadata": metadata or {},
            "registered_at": time.time(),
            "trusted": False
        }
        self.failed_attempts[did] = 0
        return did

    def trust_device(self, device_id):
        did = self._hash_device(device_id)
        if did in self.devices:
            self.devices[did]["trusted"] = True
            return True
        return False

    def _generate_token(self, device_hash):
        payload = f"{device_hash}:{time.time()}:{random.random()}".encode()
        return hmac.new(self.secret, payload, hashlib.sha256).hexdigest()

    def authenticate(self, device_id, signature=None):
        did = self._hash_device(device_id)

        if did in self.blocked:
            return {"status": "blocked", "reason": "device_blocked"}

        if did not in self.devices:
            self.failed_attempts[did] = self.failed_attempts.get(did, 0) + 1
            if self.failed_attempts[did] > 5:
                self.blocked.add(did)
            return {"status": "fail", "reason": "unknown_device"}

        if self.devices[did]["trusted"]:
            token = self._generate_token(did)
            self.sessions[did] = {
                "token": token,
                "created": time.time()
            }
            return {"status": "ok", "token": token}

        if signature:
            expected = hmac.new(self.secret, device_id.encode(), hashlib.sha256).hexdigest()
            if hmac.compare_digest(expected, signature):
                token = self._generate_token(did)
                self.sessions[did] = {
                    "token": token,
                    "created": time.time()
                }
                self.failed_attempts[did] = 0
                return {"status": "ok", "token": token}

        self.failed_attempts[did] = self.failed_attempts.get(did, 0) + 1

        if self.failed_attempts[did] > 3:
            self.blocked.add(did)

        return {"status": "fail", "reason": "invalid_auth"}

    def verify_token(self, device_id, token):
        did = self._hash_device(device_id)

        if did not in self.sessions:
            return False

        session = self.sessions[did]
        if session["token"] != token:
            return False

        if time.time() - session["created"] > 3600:
            del self.sessions[did]
            return False

        return True

    def revoke(self, device_id):
        did = self._hash_device(device_id)
        self.sessions.pop(did, None)
        return True

    def reset_device(self, device_id):
        did = self._hash_device(device_id)
        self.failed_attempts[did] = 0
        self.blocked.discard(did)
        self.sessions.pop(did, None)

    def device_status(self, device_id):
        did = self._hash_device(device_id)
        if did not in self.devices:
            return {"status": "unknown"}

        return {
            "registered": True,
            "trusted": self.devices[did]["trusted"],
            "failed_attempts": self.failed_attempts.get(did, 0),
            "blocked": did in self.blocked,
            "active_session": did in self.sessions
        }

    def list_devices(self):
        return list(self.devices.values())

    def cleanup_sessions(self):
        now = time.time()
        expired = []

        for did, session in self.sessions.items():
            if now - session["created"] > 3600:
                expired.append(did)

        for did in expired:
            del self.sessions[did]


if __name__ == "__main__":
    auth = DeviceAuth()

    d1 = auth.register_device("arduino_uno_001")
    auth.trust_device("arduino_uno_001")

    print(auth.authenticate("arduino_uno_001"))
    print(auth.device_status("arduino_uno_001"))