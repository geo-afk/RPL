from datetime import timedelta, datetime, timezone
from typing import Dict, Any, Optional
import structlog
import jwt


logger = structlog.get_logger(__name__)



class TokenManager:

    def __init__(self,
                 secret_key: str,
                 algorithm: str,
                 access_token_expire_minutes: int,
                 refresh_token_expire_days: int
        ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire = timedelta(minutes=access_token_expire_minutes)
        self.refresh_token_expire = timedelta(days=refresh_token_expire_days)
        self.blacklist = set()

    def create_access_token(
            self,
            username: str,
            user_id: int,
            expires_delta: Optional[timedelta] = None
    ) -> str:

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + self.access_token_expire

        to_encode = {
            "sub": username,
            "id": user_id,
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "type": "access"
        }

        encoded_jwt = jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )

        logger.debug(
            "access_token_created",
            subject=username,
            expires_at=expire.isoformat()
        )

        return encoded_jwt

    def create_refresh_token(
            self,
            username: str,
            user_id: int
    ) -> str:

        expire = datetime.now(timezone.utc) + self.refresh_token_expire

        to_encode = {
            "sub": username,
            "id": user_id,
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "type": "refresh"
        }

        encoded_jwt = jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )

        logger.debug(
            "refresh_token_created",
            subject=username,
            expires_at=expire.isoformat()
        )

        return encoded_jwt

    def verify_token(self, token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        try:
            # Check blacklist
            if token in self.blacklist:
                logger.warning("blacklisted_token_used")
                return None

            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )

            # Verify token type
            if payload.get("type") != token_type:
                logger.warning(
                    "token_type_mismatch",
                    expected=token_type,
                    actual=payload.get("type")
                )
                return None

            return payload

        except jwt.ExpiredSignatureError:
            logger.warning("token_expired")
            return None
        except jwt.PyJWTError as e:
            logger.warning("token_invalid", error=str(e))
            return None

    def blacklist_token(self, token: str):
        """
        Add token to blacklist (for logout).
        In production, store in Redis with TTL.
        """
        self.blacklist.add(token)
        logger.info("token_blacklisted")


