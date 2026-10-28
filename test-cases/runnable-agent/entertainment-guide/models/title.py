"""
Title model for movies and TV shows.
"""

from pydantic import BaseModel, Field

from models.enums import Genre, Mood, TitleType


class Title(BaseModel):
    """Movie or TV show model"""
    title_id: str = Field(..., pattern=r"^TITLE\d{4}$", description="Title ID")
    title: str = Field(..., min_length=1, max_length=200, description="Title name")
    type: TitleType = Field(..., description="Content type")
    year: int = Field(..., ge=1900, le=2100, description="Release year")
    genres: list[Genre] = Field(..., min_length=1, description="Genres")
    director: str = Field(..., min_length=2, description="Director name")
    cast: list[str] = Field(default_factory=list, description="Main cast")
    synopsis: str = Field(..., min_length=10, description="Plot synopsis")
    rating: float = Field(..., ge=1.0, le=10.0, description="Average rating (1.0-10.0)")
    runtime_minutes: int | None = Field(None, gt=0, description="Runtime in minutes (movies)")
    seasons: int | None = Field(None, gt=0, description="Number of seasons (TV shows)")
    episodes_per_season: list[int] | None = Field(None, description="Episodes per season (TV shows)")
    mood_tags: list[Mood] = Field(default_factory=list, description="Mood tags")


__all__ = ["Title"]
