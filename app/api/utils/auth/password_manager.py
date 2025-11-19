from passlib.context import CryptContext
import structlog


logger = structlog.get_logger(__name__)


class PasswordManager:

    def __init__(self):
        self.pwd_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, plain_password: str) -> str:
        hashed = self.pwd_hasher.hash(plain_password)
        logger.debug("password_hashed")
        return hashed

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:

        try:
            is_valid, new_hash = self.pwd_hasher.verify_and_update(
                plain_password,
                hashed_password
            )

            return is_valid
        except Exception as e:
            logger.error("password_verification_failed", error=str(e))
            return False


