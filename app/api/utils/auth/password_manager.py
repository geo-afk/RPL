from passlib.context import CryptContext
import hashlib
import structlog

logger = structlog.get_logger(__name__)

class PasswordManager:
    def __init__(self):
        self.pwd_hasher = CryptContext(schemes=["argon2"], deprecated="auto")

    def _prehash(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def hash_password(self, plain_password: str) -> str:
        prehashed = self._prehash(plain_password)
        hashed = self.pwd_hasher.hash(prehashed)
        logger.debug("password_hashed")
        return hashed

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        try:
            prehashed = self._prehash(plain_password)
            is_valid, new_hash = self.pwd_hasher.verify_and_update(prehashed, hashed_password)

            # Optional: update hash if upgraded
            if new_hash:
                logger.debug("password_hash_upgraded")
                # save new_hash to database if needed

            return is_valid
        except Exception as e:
            logger.error("password_verification_failed", error=str(e))
            return False
