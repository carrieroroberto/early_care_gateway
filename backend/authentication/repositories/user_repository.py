from abc import ABC, abstractmethod
from typing import Optional
from ..models.user_model import User

class IUserRepository(ABC):
    @abstractmethod
    def findByEmail(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def findByResetToken(self, tokenHash: str) -> Optional[User]:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass

class UserRepositoryImpl(IUserRepository):
    def __init__(self):
        self._db = {}  # mock db

    def findByEmail(self, email: str) -> Optional[User]:
        return next((u for u in self._db.values() if u.email == email), None)

    def findByResetToken(self, tokenHash: str) -> Optional[User]:
        return next((u for u in self._db.values() if u.reset_token_hash == tokenHash), None)

    def save(self, user: User) -> User:
        self._db[user.id] = user
        return user

    def update(self, user: User) -> User:
        self._db[user.id] = user
        return user