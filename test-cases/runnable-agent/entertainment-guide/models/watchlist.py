"""
Watchlist model.
"""

from pydantic import BaseModel, Field

from models.enums import WatchlistStatus


class WatchlistItem(BaseModel):
    """Watchlist item model"""
    item_id: str = Field(..., pattern=r"^WL\d{4}$", description="Watchlist item ID")
    title_id: str = Field(..., pattern=r"^TITLE\d{4}$", description="Title ID")
    status: WatchlistStatus = Field(default=WatchlistStatus.TO_WATCH, description="Watch status")
    added_date: str = Field(..., description="Date added (YYYY-MM-DD)")
    watched_date: str | None = Field(None, description="Date watched (YYYY-MM-DD)")
    user_rating: float | None = Field(None, ge=1.0, le=10.0, description="User rating (1.0-10.0)")


__all__ = ["WatchlistItem"]
