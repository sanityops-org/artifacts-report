"""
Itinerary planner for generating travel plans.
"""

from datetime import datetime, timedelta

from models import Attraction, Destination, Itinerary, DailyPlan, Activity
from models.enums import AttractionCategory


class ItineraryPlanner:
    """Itinerary generation engine"""

    def __init__(self, attractions: list[Attraction]):
        self.attractions = attractions
        self._itinerary_counter = 1

    def create_itinerary(
        self,
        destination: Destination,
        duration_days: int,
        theme: str | None = None,
        start_date: str | None = None,
        itinerary_id: str | None = None
    ) -> Itinerary:
        """
        Create a travel itinerary.

        Args:
            destination: Resolved destination
            duration_days: Trip length in days
            theme: Optional theme used to bias attraction selection
            start_date: Optional start date (YYYY-MM-DD)
            itinerary_id: Explicit ID; the caller supplies one from the data store
                so IDs stay unique across planner instances. Falls back to an
                instance-local counter when omitted.
        """
        # Get attractions for this destination
        dest_attractions = [a for a in self.attractions if a.destination_id == destination.destination_id]

        # Filter by theme if provided
        if theme:
            theme_category_map = {
                "beach": [AttractionCategory.BEACH, AttractionCategory.NATURE, AttractionCategory.RELAXATION],
                "mountain": [AttractionCategory.NATURE, AttractionCategory.ADVENTURE],
                "city": [AttractionCategory.CITY, AttractionCategory.CULTURE, AttractionCategory.SHOPPING],
                "culture": [AttractionCategory.CULTURE],
                "adventure": [AttractionCategory.ADVENTURE],
                "family": [AttractionCategory.NATURE, AttractionCategory.CULTURE, AttractionCategory.BEACH],
                "romantic": [AttractionCategory.RELAXATION, AttractionCategory.FOOD],
                "foodie": [AttractionCategory.FOOD],
                "nature": [AttractionCategory.NATURE, AttractionCategory.ADVENTURE],
                "relaxation": [AttractionCategory.RELAXATION, AttractionCategory.BEACH],
                "shopping": [AttractionCategory.SHOPPING],
            }

            if theme in theme_category_map:
                categories = theme_category_map[theme]
                dest_attractions = [a for a in dest_attractions if a.category in categories]

        # Sort by rating
        dest_attractions.sort(key=lambda a: a.rating, reverse=True)

        # Generate daily plans
        start = datetime.strptime(start_date, "%Y-%m-%d") if start_date else datetime.now()
        daily_plans = []
        attraction_index = 0

        for day in range(duration_days):
            current_date = start + timedelta(days=day)
            activities = []
            daily_cost = 0.0

            # Plan 2-4 activities per day
            activities_per_day = min(4, len(dest_attractions) - attraction_index)

            for _ in range(activities_per_day):
                if attraction_index >= len(dest_attractions):
                    break

                attraction = dest_attractions[attraction_index]
                attraction_index += 1

                # Determine start time based on recommended time
                time_map = {
                    "morning": "09:00",
                    "afternoon": "13:00",
                    "evening": "18:00",
                    "full_day": "09:00",
                }
                start_time = time_map.get(attraction.recommended_time, "10:00")

                activity = Activity(
                    activity_id=f"ACT{len(activities) + 1:03d}",
                    attraction_id=attraction.attraction_id,
                    attraction_name=attraction.name,
                    start_time=start_time,
                    duration_hours=attraction.visit_duration_hours,
                    notes=f"Rating: {attraction.rating}/5.0"
                )
                activities.append(activity)
                daily_cost += attraction.entrance_fee_usd

            daily_plan = DailyPlan(
                day_number=day + 1,
                date=current_date.strftime("%Y-%m-%d"),
                activities=activities,
                estimated_cost_usd=daily_cost
            )
            daily_plans.append(daily_plan)

        # Calculate total cost
        total_cost = sum(dp.estimated_cost_usd for dp in daily_plans)

        # Generate itinerary ID
        if itinerary_id is None:
            itinerary_id = f"ITIN{self._itinerary_counter:04d}"
            self._itinerary_counter += 1

        return Itinerary(
            itinerary_id=itinerary_id,
            destination_id=destination.destination_id,
            destination_name=destination.name,
            duration_days=duration_days,
            theme=theme,
            start_date=start_date or start.strftime("%Y-%m-%d"),
            daily_plans=daily_plans,
            total_estimated_cost_usd=total_cost
        )


__all__ = ["ItineraryPlanner"]
