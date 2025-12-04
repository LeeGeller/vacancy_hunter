from dataclasses import (
    dataclass,
    field
)

from datetime import (
    datetime,
)
from typing import (
    Optional,
)


@dataclass
class User:
    """User entity."""
    id: int
    telegram_id: int
    username: Optional[str] = None
    is_active: bool = True
    notifications_enabled: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    search_preferences: Optional[SearchPreferences] = None
    vip: bool = False
    vip_until: Optional[datetime] = None

    def get_id(self) -> int:
        """Get user id."""
        return self.id

    def get_telegram_id(self) -> int:
        """Get user Telegram id."""
        return self.telegram_id

    def get_telegram_link(self) -> str:
        """Get user Telegram link."""
        return f'https://t.me/{self.username}'

    def get_username(self) -> str:
        """Get user username."""
        return self.username or f'@{self.username}'

    def is_active_user(self) -> bool:
        """Check if user is active."""
        return self.is_active

    def is_notifications_enabled(self) -> bool:
        """Check if notifications are enabled."""
        return self.notifications_enabled

    def is_vip(self) -> bool:
        """Check if user is VIP."""
        return datetime.now() < self.vip_until if self.vip_until else False
