"""
Trip Planner Assistant - Multi-Agent System
Demonstrates ADK concepts: parallel agents, tools, memory, observability
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()


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
    type: str  # 'hotel', 'flight', 'rental'
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
    """Simple memory implementation for user preferences"""
    
    def __init__(self):
        self.preferences: Dict[str, Any] = {}
        self.past_trips: List[TripItinerary] = []
        logger.info("memory_bank.initialized")
    
    def store_preference(self, key: str, value: Any):
        """Store a user preference"""
        self.preferences[key] = value
        logger.info("memory_bank.preference_stored", key=key)
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Retrieve a stored preference"""
        return self.preferences.get(key, default)
    
    def add_trip(self, itinerary: TripItinerary):
        """Store a completed trip"""
        self.past_trips.append(itinerary)
        logger.info("memory_bank.trip_stored", 
                   destination=itinerary.requirements.destination,
                   total_trips=len(self.past_trips))
    
    def get_similar_trips(self, destination: str) -> List[TripItinerary]:
        """Find similar past trips"""
        return [t for t in self.past_trips 
                if destination.lower() in t.requirements.destination.lower()]


class SessionState:
    """Manages conversation state - simplified version of InMemorySessionService"""
    
    def __init__(self):
        self.conversation_history: List[Dict[str, str]] = []
        self.current_requirements: Optional[TripRequirements] = None
        self.iteration: int = 0
        self.intermediate_results: Dict[str, Any] = {}
        logger.info("session_state.initialized")
    
    def add_message(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        logger.debug("session_state.message_added", role=role)
    
    def update_requirements(self, requirements: TripRequirements):
        """Update trip requirements"""
        self.current_requirements = requirements
        logger.info("session_state.requirements_updated", 
                   destination=requirements.destination)
    
    def store_intermediate(self, agent_name: str, result: Any):
        """Store intermediate agent results"""
        self.intermediate_results[agent_name] = result
        logger.debug("session_state.intermediate_stored", agent=agent_name)
    
    def compact_context(self, max_messages: int = 10):
        """Context compaction - keep recent messages"""
        if len(self.conversation_history) > max_messages:
            original_len = len(self.conversation_history)
            self.conversation_history = self.conversation_history[-max_messages:]
            logger.info("session_state.context_compacted",
                       original=original_len,
                       compacted=len(self.conversation_history))


class MockGoogleSearchTool:
    """Mock Google Search tool for demo purposes"""
    
    def search(self, query: str, interests: List[str] = None, num_results: int = 5) -> List[Dict[str, str]]:
        """Simulate search results"""
        logger.info("tool.google_search.called", query=query)
        
        # Return mock results based on query
        if "restaurant" in query.lower() or "food" in query.lower():
            return [
                {"title": "Top Local Restaurant", "snippet": "Highly rated local cuisine, $30-50 per person"},
                {"title": "Casual Dining Spot", "snippet": "Family-friendly, $15-25 per person"},
                {"title": "Food Market", "snippet": "Local specialties, $10-20 per person"}
            ]
        elif "hotel" in query.lower():
            return [
                {"title": "Downtown Hotel", "snippet": "$120/night, 4.5 stars"},
                {"title": "Budget Inn", "snippet": "$75/night, 3.5 stars"},
                {"title": "Luxury Resort", "snippet": "$250/night, 5 stars"}
            ]
        elif "things to do" in query.lower():
            base_attractions = [
                {"title": "Main Museum", "snippet": "Popular attraction, $25 entry"},
                {"title": "Historic District Walking Tour", "snippet": "Free self-guided tour"},
                {"title": "Local Park", "snippet": "Beautiful gardens, free entry"}
            ]
            if interests and "art" in interests:
                base_attractions.insert(0, {"title": "Modern Art Gallery", "snippet": "Contemporary art, $20 entry"})
            if interests and "history" in interests:
                base_attractions.insert(1, {"title": "Castle Ruins", "snippet": "Historic site, $15 entry"})
            return base_attractions[:num_results]
        else: # Generic fallback
            return [
                {"title": "Generic Search Result", "snippet": "Details about your query."}
            ]


class MockCodeExecutionTool:
    """Mock code execution for calculations"""
    
    def execute(self, code: str) -> Any:
        """Execute Python code safely (mock)"""
        logger.info("tool.code_execution.called")
        
        # For demo, simulate budget calculations
        if "budget" in code.lower():
            return {
                "accommodation": 360.0,  # 3 nights × $120
                "meals": 270.0,  # 3 days × $90
                "activities": 150.0,
                "transport": 100.0,
                "total": 880.0
            }
        return {"result": "calculated"}


class ItineraryPlannerAgent:
    """Agent responsible for creating day-by-day itinerary"""
    
    def __init__(self, search_tool: MockGoogleSearchTool, 
                 code_tool: MockCodeExecutionTool):
        self.search_tool = search_tool
        self.code_tool = code_tool
        self.name = "ItineraryPlanner"
        logger.info("agent.itinerary_planner.initialized")
    
    def plan(self, requirements: TripRequirements, 
             memory: MemoryBank) -> List[DayPlan]:
        """Create itinerary based on requirements"""
        logger.info("agent.itinerary_planner.planning_started",
                   destination=requirements.destination)
        
        # Check memory for similar trips
        similar = memory.get_similar_trips(requirements.destination)
        if similar:
            logger.info("agent.itinerary_planner.found_similar_trips",
                       count=len(similar))
        
        # Search for attractions
        attractions = self.search_tool.search(
            f"top things to do in {requirements.destination}",
            interests=requirements.interests
        )
        restaurants = self.search_tool.search(
            f"best restaurants in {requirements.destination}"
        )
        
        # Create 3-day plan
        days = []
        for day_num in range(1, 4):
            activities = [
                Activity(
                    name=f"Morning: {attractions[0]['title']}",
                    time="09:00",
                    duration_hours=2.5,
                    cost=25.0,
                    category="sightseeing",
                    description="Start the day with popular attraction"
                ),
                Activity(
                    name=f"Lunch at {restaurants[0]['title']}",
                    time="12:00",
                    duration_hours=1.5,
                    cost=30.0,
                    category="meal",
                    description="Experience local cuisine"
                ),
                Activity(
                    name=f"Afternoon: {attractions[1]['title']}",
                    time="14:00",
                    duration_hours=2.0,
                    cost=20.0,
                    category="culture",
                    description="Cultural exploration"
                ),
                Activity(
                    name=f"Dinner at {restaurants[1]['title']}",
                    time="19:00",
                    duration_hours=2.0,
                    cost=45.0,
                    category="meal",
                    description="Dinner with local flavors"
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
        
        logger.info("agent.itinerary_planner.planning_completed",
                   num_days=len(days))
        return days


class BudgetAnalyzerAgent:
    """Agent responsible for budget analysis and optimization"""
    
    def __init__(self, code_tool: MockCodeExecutionTool):
        self.code_tool = code_tool
        self.name = "BudgetAnalyzer"
        logger.info("agent.budget_analyzer.initialized")
    
    def analyze(self, requirements: TripRequirements,
                days: List[DayPlan]) -> BudgetBreakdown:
        """Analyze budget and suggest optimizations"""
        logger.info("agent.budget_analyzer.analysis_started",
                   budget=requirements.budget)
        
        # Calculate costs using code execution tool
        budget_calc = self.code_tool.execute("calculate_budget()")
        
        # Calculate from itinerary
        activities_cost = sum(day.total_cost for day in days)
        accommodation_cost = 120.0 * 3  # 3 nights
        transport_cost = 100.0
        
        total = accommodation_cost + activities_cost + transport_cost
        within_budget = total <= requirements.budget
        
        suggestions = []
        if not within_budget:
            overage = total - requirements.budget
            suggestions.append(f"Consider budget accommodation to save ${accommodation_cost - 75*3:.2f}")
            suggestions.append(f"Reduce dining expenses by ${overage * 0.3:.2f}")
        
        breakdown = BudgetBreakdown(
            accommodation=accommodation_cost,
            activities=sum(a.cost for day in days for a in day.activities if a.category != 'meal'),
            meals=sum(a.cost for day in days for a in day.activities if a.category == 'meal'),
            transportation=transport_cost,
            total=total,
            within_budget=within_budget,
            savings_suggestions=suggestions
        )
        
        logger.info("agent.budget_analyzer.analysis_completed",
                   total=total,
                   within_budget=within_budget)
        return breakdown


class BookingHelperAgent:
    """Agent responsible for finding booking options"""
    
    def __init__(self, search_tool: MockGoogleSearchTool):
        self.search_tool = search_tool
        self.name = "BookingHelper"
        logger.info("agent.booking_helper.initialized")
    
    def find_options(self, requirements: TripRequirements) -> List[BookingOption]:
        """Find accommodation and transport options"""
        logger.info("agent.booking_helper.search_started",
                   destination=requirements.destination)
        
        # Search for hotels
        hotels = self.search_tool.search(
            f"hotels in {requirements.destination}"
        )
        
        options = [
            BookingOption(
                name="Downtown Hotel",
                type="hotel",
                price=120.0,
                rating=4.5,
                url="https://example.com/booking",
                features=["Free WiFi", "Breakfast included", "Central location"]
            ),
            BookingOption(
                name="Budget Inn",
                type="hotel",
                price=75.0,
                rating=3.8,
                url="https://example.com/booking",
                features=["Free parking", "Airport shuttle"]
            ),
            BookingOption(
                name="Return Flight",
                type="flight",
                price=450.0,
                rating=4.2,
                url="https://example.com/flights",
                features=["Direct flight", "2 checked bags"]
            )
        ]
        
        logger.info("agent.booking_helper.search_completed",
                   num_options=len(options))
        return options


class CoordinatorAgent:
    """Main coordinator that orchestrates all specialist agents"""
    
    def __init__(self):
        self.session = SessionState()
        self.memory = MemoryBank()
        
        # Initialize tools
        search_tool = MockGoogleSearchTool()
        code_tool = MockCodeExecutionTool()
        
        # Initialize specialist agents
        self.itinerary_agent = ItineraryPlannerAgent(search_tool, code_tool)
        self.budget_agent = BudgetAnalyzerAgent(code_tool)
        self.booking_agent = BookingHelperAgent(search_tool)
        
        logger.info("agent.coordinator.initialized")
    
    def process_request(self, requirements: TripRequirements,
                       max_iterations: int = 3) -> TripItinerary:
        """Process trip planning request with iterative refinement"""
        logger.info("agent.coordinator.request_started",
                   destination=requirements.destination,
                   budget=requirements.budget)
        
        self.session.update_requirements(requirements)
        self.session.add_message("user", f"Plan trip to {requirements.destination}")
        
        for iteration in range(1, max_iterations + 1):
            self.session.iteration = iteration
            logger.info("agent.coordinator.iteration_started", iteration=iteration)
            
            # Run agents in parallel (simulated)
            days = self.itinerary_agent.plan(requirements, self.memory)
            self.session.store_intermediate("itinerary", days)
            
            budget = self.budget_agent.analyze(requirements, days)
            self.session.store_intermediate("budget", budget)
            
            bookings = self.booking_agent.find_options(requirements)
            self.session.store_intermediate("bookings", bookings)
            
            # Check if requirements are met
            if budget.within_budget and len(days) == 3:
                logger.info("agent.coordinator.requirements_met", iteration=iteration)
                break
            
            # Context compaction if needed
            self.session.compact_context()
        
        # Create final itinerary
        itinerary = TripItinerary(
            requirements=requirements,
            days=days,
            budget=budget,
            bookings=bookings,
            created_at=datetime.now().isoformat(),
            iteration_count=self.session.iteration
        )
        
        # Store in memory
        self.memory.add_trip(itinerary)
        
        logger.info("agent.coordinator.request_completed",
                   iterations=self.session.iteration,
                   total_cost=budget.total)
        
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
        if day.notes:
            lines.append(f"  Notes: {day.notes}")
    
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
    
    if itinerary.budget.savings_suggestions:
        lines.append("\nSavings Suggestions:")
        for suggestion in itinerary.budget.savings_suggestions:
            lines.append(f"  • {suggestion}")
    
    lines.append("\n" + "=" * 60)
    lines.append("BOOKING OPTIONS")
    lines.append("=" * 60)
    for booking in itinerary.bookings:
        lines.append(f"{booking.name} ({booking.type})")
        lines.append(f"  Price: ${booking.price} | Rating: {booking.rating}★")
        lines.append(f"  Features: {', '.join(booking.features)}")
        lines.append("")
    
    lines.append(f"Generated in {itinerary.iteration_count} iteration(s)")
    lines.append("=" * 60)
    
    return "\n".join(lines)


if __name__ == "__main__":
    # Demo usage
    print("🌍 Trip Planner Assistant - Multi-Agent Demo\n")
    
    # Create sample trip request
    requirements = TripRequirements(
        destination="Paris, France",
        start_date="2025-06-01",
        end_date="2025-06-03",
        budget=1500.0,
        num_travelers=2,
        interests=["art", "food", "history"],
        dietary_restrictions=["vegetarian options"],
        accommodation_preference="hotel"
    )
    
    # Create coordinator and process request
    coordinator = CoordinatorAgent()
    itinerary = coordinator.process_request(requirements)
    
    # Display results
    print(format_itinerary(itinerary))
    
    # Export to JSON
    output_file = "trip_itinerary.json"
    with open(output_file, "w") as f:
        json.dump(asdict(itinerary), f, indent=2, default=str)
    print(f"\n✓ Itinerary saved to {output_file}")
