"""
Review model.
"""

from pydantic import BaseModel, Field


class Review(BaseModel):
    """User review model"""
    review_id: str = Field(..., pattern=r"^REV\d{4}$", description="Review ID")
    title_id: str = Field(..., pattern=r"^TITLE\d{4}$", description="Title ID")
    user_name: str = Field(..., min_length=2, description="Reviewer name")
    rating: float = Field(..., ge=1.0, le=10.0, description="Rating (1.0-10.0)")
    comment: str = Field(..., min_length=5, description="Review comment")
    date: str = Field(..., description="Review date (YYYY-MM-DD)")


__all__ = ["Review"]
