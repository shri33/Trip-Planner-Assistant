"""
Trip Planner Agent Package
Multi-agent travel planning system
"""

from .trip_planner_agent import (
    TripRequirements,
    Activity,
    DayPlan,
    BudgetBreakdown,
    BookingOption,
    TripItinerary,
    MemoryBank,
    SessionState,
    CoordinatorAgent,
    format_itinerary
)

from .evaluation import (
    AgentEvaluator,
    EvaluationMetric,
    EvaluationResult,
    run_evaluation_suite
)

__version__ = "1.0.0"
__author__ = "Trip Planner Assistant Team"
__all__ = [
    "TripRequirements",
    "Activity",
    "DayPlan",
    "BudgetBreakdown",
    "BookingOption",
    "TripItinerary",
    "MemoryBank",
    "SessionState",
    "CoordinatorAgent",
    "format_itinerary",
    "AgentEvaluator",
    "EvaluationMetric",
    "EvaluationResult",
    "run_evaluation_suite"
]
