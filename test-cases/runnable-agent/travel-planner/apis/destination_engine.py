"""
Destination engine for search and filtering.
"""

from models import Attraction, Destination
from models.enums import TravelTheme


class DestinationEngine:
    """Destination search and filtering engine"""

    def __init__(self, destinations: list[Destination], attractions: list[Attraction]):
        self.destinations = destinations
        self.attractions = attractions

    def search_destinations(
        self,
        query: str | None = None,
        country: str | None = None,
        theme: str | None = None
    ) -> list[Destination]:
        """Search destinations by query, country, or theme"""
        results = self.destinations

        # Filter by country
        if country:
            results = [d for d in results if d.country.lower() == country.lower()]

        # Filter by theme
        if theme:
            try:
                theme_enum = TravelTheme(theme.lower())
                results = [d for d in results if theme_enum in d.themes]
            except ValueError:
                pass

        # Filter by query (search in name, country, description)
        if query:
            query_lower = query.lower()
            results = [
                d for d in results
                if query_lower in d.name.lower()
                or query_lower in d.country.lower()
                or query_lower in d.description.lower()
            ]

        return results[:10]  # Return top 10

    def get_destination(self, destination_id: str) -> Destination | None:
        """Get destination by ID"""
        for dest in self.destinations:
            if dest.destination_id == destination_id:
                return dest
        return None

    def get_attractions_for_destination(
        self,
        destination_id: str,
        category: str | None = None,
        min_rating: float | None = None
    ) -> list[Attraction]:
        """Get attractions for a destination with optional filters"""
        results = [a for a in self.attractions if a.destination_id == destination_id]

        # Filter by category
        if category:
            results = [a for a in results if a.category.value == category.lower()]

        # Filter by minimum rating
        if min_rating is not None:
            results = [a for a in results if a.rating >= min_rating]

        # Sort by rating (descending)
        results.sort(key=lambda a: a.rating, reverse=True)

        return results


__all__ = ["DestinationEngine"]
