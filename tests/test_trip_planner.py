"""
Unit tests for Trip Planner Agent
"""

import pytest
from trip_planner_agent import (
    TripRequirements, MemoryBank, SessionState,
    ItineraryPlannerAgent, BudgetAnalyzerAgent, BookingHelperAgent,
    CoordinatorAgent, MockGoogleSearchTool, MockCodeExecutionTool
)


class TestTripRequirements:
    """Test TripRequirements dataclass"""
    
    def test_basic_creation(self):
        req = TripRequirements(
            destination="Paris",
            start_date="2025-06-01",
            end_date="2025-06-03",
            budget=1000.0
        )
        assert req.destination == "Paris"
        assert req.budget == 1000.0
        assert req.num_travelers == 1
        assert req.interests == []
    
    def test_with_interests(self):
        req = TripRequirements(
            destination="Paris",
            start_date="2025-06-01",
            end_date="2025-06-03",
            budget=1000.0,
            interests=["art", "food"]
        )
        assert len(req.interests) == 2
        assert "art" in req.interests


class TestMemoryBank:
    """Test memory management"""
    
    def test_initialization(self):
        memory = MemoryBank()
        assert memory.preferences == {}
        assert memory.past_trips == []
    
    def test_store_preference(self):
        memory = MemoryBank()
        memory.store_preference("favorite_city", "Paris")
        assert memory.get_preference("favorite_city") == "Paris"
    
    def test_get_preference_default(self):
        memory = MemoryBank()
        assert memory.get_preference("unknown", "default") == "default"


class TestSessionState:
    """Test session state management"""
    
    def test_initialization(self):
        session = SessionState()
        assert session.iteration == 0
        assert len(session.conversation_history) == 0
    
    def test_add_message(self):
        session = SessionState()
        session.add_message("user", "Hello")
        assert len(session.conversation_history) == 1
        assert session.conversation_history[0]["role"] == "user"
    
    def test_context_compaction(self):
        session = SessionState()
        for i in range(20):
            session.add_message("user", f"Message {i}")
        
        session.compact_context(max_messages=10)
        assert len(session.conversation_history) == 10


class TestMockTools:
    """Test mock tool implementations"""
    
    def test_google_search_restaurants(self):
        tool = MockGoogleSearchTool()
        results = tool.search("restaurants in Paris")
        assert len(results) > 0
        assert "restaurant" in results[0]["title"].lower() or "food" in results[0]["snippet"].lower()
    
    def test_google_search_hotels(self):
        tool = MockGoogleSearchTool()
        results = tool.search("hotels in Paris")
        assert len(results) > 0
    
    def test_code_execution(self):
        tool = MockCodeExecutionTool()
        result = tool.execute("calculate budget")
        assert "total" in result or "result" in result


class TestItineraryPlannerAgent:
    """Test itinerary planner agent"""
    
    def test_agent_creation(self):
        search_tool = MockGoogleSearchTool()
        code_tool = MockCodeExecutionTool()
        agent = ItineraryPlannerAgent(search_tool, code_tool)
        assert agent.name == "ItineraryPlanner"
    
    def test_plan_creation(self):
        search_tool = MockGoogleSearchTool()
        code_tool = MockCodeExecutionTool()
        agent = ItineraryPlannerAgent(search_tool, code_tool)
        memory = MemoryBank()
        
        requirements = TripRequirements(
            destination="Paris",
            start_date="2025-06-01",
            end_date="2025-06-03",
            budget=1500.0,
            interests=["art"]
        )
        
        days = agent.plan(requirements, memory)
        assert len(days) == 3
        assert all(len(day.activities) > 0 for day in days)
        assert all(day.total_cost > 0 for day in days)


class TestBudgetAnalyzerAgent:
    """Test budget analyzer agent"""
    
    def test_agent_creation(self):
        code_tool = MockCodeExecutionTool()
        agent = BudgetAnalyzerAgent(code_tool)
        assert agent.name == "BudgetAnalyzer"
    
    def test_budget_analysis(self):
        from trip_planner_agent import DayPlan, Activity
        
        code_tool = MockCodeExecutionTool()
        agent = BudgetAnalyzerAgent(code_tool)
        
        requirements = TripRequirements(
            destination="Paris",
            start_date="2025-06-01",
            end_date="2025-06-03",
            budget=1500.0
        )
        
        days = [
            DayPlan(
                day_number=1,
                date="Day 1",
                activities=[
                    Activity("Activity 1", "09:00", 2.0, 50.0, "sightseeing")
                ],
                total_cost=50.0
            )
        ]
        
        breakdown = agent.analyze(requirements, days)
        assert breakdown.total > 0
        assert isinstance(breakdown.within_budget, bool)


class TestBookingHelperAgent:
    """Test booking helper agent"""
    
    def test_agent_creation(self):
        search_tool = MockGoogleSearchTool()
        agent = BookingHelperAgent(search_tool)
        assert agent.name == "BookingHelper"
    
    def test_find_options(self):
        search_tool = MockGoogleSearchTool()
        agent = BookingHelperAgent(search_tool)
        
        requirements = TripRequirements(
            destination="Paris",
            start_date="2025-06-01",
            end_date="2025-06-03",
            budget=1500.0
        )
        
        options = agent.find_options(requirements)
        assert len(options) > 0
        assert all(hasattr(opt, 'price') for opt in options)
        assert all(hasattr(opt, 'rating') for opt in options)


class TestCoordinatorAgent:
    """Test coordinator agent"""
    
    def test_coordinator_creation(self):
        coordinator = CoordinatorAgent()
        assert coordinator.itinerary_agent is not None
        assert coordinator.budget_agent is not None
        assert coordinator.booking_agent is not None
    
    def test_process_request(self):
        coordinator = CoordinatorAgent()
        
        requirements = TripRequirements(
            destination="Paris",
            start_date="2025-06-01",
            end_date="2025-06-03",
            budget=1500.0,
            interests=["art", "food"]
        )
        
        itinerary = coordinator.process_request(requirements, max_iterations=2)
        
        assert itinerary is not None
        assert len(itinerary.days) == 3
        assert itinerary.budget.total > 0
        assert len(itinerary.bookings) > 0
        assert itinerary.iteration_count <= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
