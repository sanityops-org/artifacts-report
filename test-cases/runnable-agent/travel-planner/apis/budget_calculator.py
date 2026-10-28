"""
Budget calculator for trip cost estimation.
"""

from models import Destination
from models.enums import BudgetLevel


class BudgetCalculator:
    """Trip budget estimation engine"""

    # Base costs per day per person (in USD)
    BASE_COSTS = {
        BudgetLevel.BUDGET: {
            "accommodation": 30,
            "food": 20,
            "activities": 15,
            "transport": 10,
        },
        BudgetLevel.MODERATE: {
            "accommodation": 100,
            "food": 50,
            "activities": 40,
            "transport": 25,
        },
        BudgetLevel.LUXURY: {
            "accommodation": 300,
            "food": 120,
            "activities": 100,
            "transport": 60,
        },
    }

    # Destination budget multipliers
    DESTINATION_MULTIPLIERS = {
        "France": 1.3,
        "Japan": 1.4,
        "Indonesia": 0.8,
        "USA": 1.5,
        "Spain": 1.1,
        "Australia": 1.4,
        "Italy": 1.2,
        "Thailand": 0.7,
        "Canada": 1.3,
        "Greece": 1.2,
    }

    def estimate_budget(
        self,
        destination: Destination,
        duration_days: int,
        budget_level: BudgetLevel = BudgetLevel.MODERATE,
        travelers_count: int = 1
    ) -> dict[str, float]:
        """Estimate trip budget"""
        # Get base costs
        base = self.BASE_COSTS[budget_level]

        # Get destination multiplier
        multiplier = self.DESTINATION_MULTIPLIERS.get(destination.country, 1.0)

        # Calculate costs
        accommodation = base["accommodation"] * duration_days * travelers_count * multiplier
        food = base["food"] * duration_days * travelers_count * multiplier
        activities = base["activities"] * duration_days * travelers_count * multiplier
        transport = base["transport"] * duration_days * travelers_count * multiplier

        # Fixed costs
        visa_fees = 50 * travelers_count  # Estimate
        insurance = 10 * duration_days * travelers_count

        # Total
        total = accommodation + food + activities + transport + visa_fees + insurance

        return {
            "accommodation_usd": round(accommodation, 2),
            "food_usd": round(food, 2),
            "activities_usd": round(activities, 2),
            "transport_usd": round(transport, 2),
            "visa_fees_usd": round(visa_fees, 2),
            "insurance_usd": round(insurance, 2),
            "total_usd": round(total, 2),
            "disclaimer": "Estimates are approximate and may vary based on season, availability, and personal choices."
        }


__all__ = ["BudgetCalculator"]
