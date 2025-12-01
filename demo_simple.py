"""
Simplified Trip Planner Agent Demo (No External Dependencies)
Demonstrates core concepts without requiring package installation
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class TripRequirements:
    """User's trip requirements"""
    destination: str
    start_date: str
    end_date: str
    budget: float
    num_travelers: int = 1
    interests: List[str] = None
    dietary_restrictions: List[str] = None
    accommodation_preference: str = "hotel"
    
    def __post_init__(self):
        if self.interests is None:
            self.interests = []
        if self.dietary_restrictions is None:
            self.dietary_restrictions = []


@dataclass
class Activity:
    """Single activity in itinerary"""
    name: str
    time: str
    duration_hours: float
    cost: float
    category: str
    description: str = ""


@dataclass
class DayPlan:
    """Plan for a single day"""
    day_number: int
    date: str
    activities: List[Activity]
    total_cost: float
    notes: str = ""


@dataclass
class BudgetBreakdown:
    """Budget analysis"""
    accommodation: float
    activities: float
    meals: float
    transportation: float
    total: float
    within_budget: bool
    savings_suggestions: List[str] = None
    
    def __post_init__(self):
        if self.savings_suggestions is None:
            self.savings_suggestions = []


@dataclass
class BookingOption:
    """Accommodation or flight option"""
    name: str
    type: str
    price: float
    rating: float
    url: str = ""
    features: List[str] = None
    
    def __post_init__(self):
        if self.features is None:
            self.features = []


@dataclass
class TripItinerary:
    """Complete trip itinerary"""
    requirements: TripRequirements
    days: List[DayPlan]
    budget: BudgetBreakdown
    bookings: List[BookingOption]
    created_at: str
    iteration_count: int = 1


class MemoryBank:
    """Simple memory implementation"""
    
    def __init__(self):
        self.preferences: Dict[str, Any] = {}
        self.past_trips: List[TripItinerary] = []
        logger.info("Memory bank initialized")
    
    def add_trip(self, itinerary: TripItinerary):
        self.past_trips.append(itinerary)
        logger.info(f"Trip stored: {itinerary.requirements.destination}")


class ItineraryPlannerAgent:
    """Creates day-by-day itinerary"""
    
    def plan(self, requirements: TripRequirements, memory: MemoryBank) -> List[DayPlan]:
        logger.info(f"Planning itinerary for {requirements.destination}")
        
        days = []
        for day_num in range(1, 4):
            activities = [
                Activity(
                    name=f"Morning: Top Attraction in {requirements.destination}",
                    time="09:00",
                    duration_hours=2.5,
                    cost=25.0,
                    category="sightseeing",
                    description="Visit iconic landmark"
                ),
                Activity(
                    name="Lunch at Local Restaurant",
                    time="12:00",
                    duration_hours=1.5,
                    cost=30.0,
                    category="meal",
                    description="Experience local cuisine"
                ),
                Activity(
                    name="Afternoon: Cultural Experience",
                    time="14:00",
                    duration_hours=2.0,
                    cost=20.0,
                    category="culture",
                    description="Museum or cultural site"
                ),
                Activity(
                    name="Evening Dining",
                    time="19:00",
                    duration_hours=2.0,
                    cost=45.0,
                    category="meal",
                    description="Dinner at recommended restaurant"
                )
            ]
            
            day_cost = sum(a.cost for a in activities)
            days.append(DayPlan(
                day_number=day_num,
                date=f"Day {day_num}",
                activities=activities,
                total_cost=day_cost,
                notes=f"Focus on {requirements.interests[0] if requirements.interests else 'exploration'}"
            ))
        
        return days


class BudgetAnalyzerAgent:
    """Analyzes budget and costs"""
    
    def analyze(self, requirements: TripRequirements, days: List[DayPlan]) -> BudgetBreakdown:
        logger.info(f"Analyzing budget: ${requirements.budget}")
        
        activities_cost = sum(day.total_cost for day in days)
        accommodation_cost = 120.0 * 3
        transport_cost = 100.0
        
        total = accommodation_cost + activities_cost + transport_cost
        within_budget = total <= requirements.budget
        
        suggestions = []
        if not within_budget:
            overage = total - requirements.budget
            suggestions.append(f"Consider budget accommodation to save ${accommodation_cost - 75*3:.2f}")
        
        return BudgetBreakdown(
            accommodation=accommodation_cost,
            activities=sum(a.cost for day in days for a in day.activities if a.category != 'meal'),
            meals=sum(a.cost for day in days for a in day.activities if a.category == 'meal'),
            transportation=transport_cost,
            total=total,
            within_budget=within_budget,
            savings_suggestions=suggestions
        )


class BookingHelperAgent:
    """Finds booking options"""
    
    def find_options(self, requirements: TripRequirements) -> List[BookingOption]:
        logger.info(f"Finding bookings for {requirements.destination}")
        
        return [
            BookingOption(
                name="Downtown Hotel",
                type="hotel",
                price=120.0,
                rating=4.5,
                features=["Free WiFi", "Breakfast included", "Central location"]
            ),
            BookingOption(
                name="Budget Inn",
                type="hotel",
                price=75.0,
                rating=3.8,
                features=["Free parking", "Airport shuttle"]
            )
        ]


class CoordinatorAgent:
    """Main coordinator orchestrating all agents"""
    
    def __init__(self):
        self.memory = MemoryBank()
        self.itinerary_agent = ItineraryPlannerAgent()
        self.budget_agent = BudgetAnalyzerAgent()
        self.booking_agent = BookingHelperAgent()
        logger.info("Coordinator agent initialized")
    
    def process_request(self, requirements: TripRequirements, max_iterations: int = 3) -> TripItinerary:
        logger.info(f"Processing request: {requirements.destination}")
        
        # Run agents
        days = self.itinerary_agent.plan(requirements, self.memory)
        budget = self.budget_agent.analyze(requirements, days)
        bookings = self.booking_agent.find_options(requirements)
        
        itinerary = TripItinerary(
            requirements=requirements,
            days=days,
            budget=budget,
            bookings=bookings,
            created_at=datetime.now().isoformat(),
            iteration_count=1
        )
        
        self.memory.add_trip(itinerary)
        logger.info(f"Trip planning completed: ${budget.total:.2f}")
        
        return itinerary


def format_itinerary(itinerary: TripItinerary) -> str:
    """Format itinerary for display"""
    lines = []
    lines.append("=" * 60)
    lines.append(f"TRIP TO {itinerary.requirements.destination.upper()}")
    lines.append("=" * 60)
    lines.append(f"Budget: ${itinerary.requirements.budget}")
    lines.append(f"Travelers: {itinerary.requirements.num_travelers}")
    lines.append(f"Interests: {', '.join(itinerary.requirements.interests)}")
    lines.append("")
    
    for day in itinerary.days:
        lines.append(f"\n{day.date} - ${day.total_cost:.2f}")
        lines.append("-" * 60)
        for activity in day.activities:
            lines.append(f"  {activity.time} | {activity.name} (${activity.cost})")
            lines.append(f"           {activity.description}")
    
    lines.append("\n" + "=" * 60)
    lines.append("BUDGET BREAKDOWN")
    lines.append("=" * 60)
    lines.append(f"Accommodation: ${itinerary.budget.accommodation:.2f}")
    lines.append(f"Activities:    ${itinerary.budget.activities:.2f}")
    lines.append(f"Meals:         ${itinerary.budget.meals:.2f}")
    lines.append(f"Transport:     ${itinerary.budget.transportation:.2f}")
    lines.append("-" * 60)
    lines.append(f"TOTAL:         ${itinerary.budget.total:.2f}")
    lines.append(f"Within Budget: {'✓ YES' if itinerary.budget.within_budget else '✗ NO'}")
    
    lines.append("\n" + "=" * 60)
    lines.append("BOOKING OPTIONS")
    lines.append("=" * 60)
    for booking in itinerary.bookings:
        lines.append(f"{booking.name} ({booking.type})")
        lines.append(f"  Price: ${booking.price} | Rating: {booking.rating}★")
        lines.append(f"  Features: {', '.join(booking.features)}")
    
    lines.append(f"\nGenerated in {itinerary.iteration_count} iteration(s)")
    lines.append("=" * 60)
    
    return "\n".join(lines)


if __name__ == "__main__":
    print("🌍 Trip Planner Assistant - Demo (Simplified)\n")
    
    # Create sample trip
    requirements = TripRequirements(
        destination="Paris, France",
        start_date="2025-06-01",
        end_date="2025-06-03",
        budget=1500.0,
        num_travelers=2,
        interests=["art", "food", "history"]
    )
    
    # Process request
    coordinator = CoordinatorAgent()
    itinerary = coordinator.process_request(requirements)
    
    # Display
    print(format_itinerary(itinerary))
    
    # Export
    output = "trip_itinerary_simple.json"
    with open(output, "w") as f:
        json.dump(asdict(itinerary), f, indent=2, default=str)
    print(f"\n✓ Itinerary saved to {output}")
