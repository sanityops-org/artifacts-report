"""
Enumerations for Entertainment Guide domain models.
"""

from enum import Enum


class TitleType(str, Enum):
    """Title types"""
    MOVIE = "movie"          # Film
    TV_SHOW = "tv_show"      # Television drama


class WatchlistStatus(str, Enum):
    """Watchlist item status"""
    TO_WATCH = "to_watch"    # To be watched
    WATCHED = "watched"      # Watched


class Genre(str, Enum):
    """Content genres"""
    ACTION = "action"              # Action
    COMEDY = "comedy"              # Comedy
    DRAMA = "drama"                # Plot of a play or opera
    HORROR = "horror"              # Terrifying
    ROMANCE = "romance"            # Love
    SCI_FI = "sci_fi"              # Science fiction
    THRILLER = "thriller"          # Thriller
    DOCUMENTARY = "documentary"    # Documentary
    ANIMATION = "animation"        # Anime
    FANTASY = "fantasy"            # Fantastic


class Mood(str, Enum):
    """Viewing moods"""
    HAPPY = "happy"              # Happy
    SAD = "sad"                  # Sad
    EXCITED = "excited"          # Excited
    RELAXED = "relaxed"          # Relax
    THRILLED = "thrilled"        # Stimulate
    THOUGHTFUL = "thoughtful"    # Contemplate


__all__ = [
    "TitleType",
    "WatchlistStatus",
    "Genre",
    "Mood",
]
