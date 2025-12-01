"""
Evaluation harness for Trip Planner Agent
Tests constraint satisfaction and agent performance
"""

import json
from typing import List, Dict
from dataclasses import dataclass
import structlog

from trip_planner_agent import (
    CoordinatorAgent, TripRequirements, TripItinerary,
    format_itinerary
)

logger = structlog.get_logger()


@dataclass
class EvaluationMetric:
    """Single evaluation metric"""
    name: str
    score: float  # 0.0 to 1.0
    max_score: float
    passed: bool
    details: str = ""


@dataclass
class EvaluationResult:
    """Complete evaluation result"""
    scenario_name: str
    metrics: List[EvaluationMetric]
    overall_score: float
    passed: bool
    itinerary: TripItinerary


class AgentEvaluator:
    """Evaluates agent performance against test scenarios"""
    
    def __init__(self):
        self.coordinator = CoordinatorAgent()
        logger.info("evaluator.initialized")
    
    def evaluate_budget_adherence(self, itinerary: TripItinerary) -> EvaluationMetric:
        """Check if itinerary stays within budget"""
        budget = itinerary.requirements.budget
        actual = itinerary.budget.total
        
        if actual <= budget:
            score = 1.0
            passed = True
            details = f"Within budget: ${actual:.2f} ≤ ${budget:.2f}"
        else:
            overage_pct = ((actual - budget) / budget) * 100
            # Allow 5% overage for partial credit
            if overage_pct <= 5:
                score = 0.7
                passed = True
            else:
                score = max(0, 1.0 - (overage_pct / 100))
                passed = False
            details = f"Over budget by ${actual - budget:.2f} ({overage_pct:.1f}%)"
        
        return EvaluationMetric(
            name="Budget Adherence",
            score=score,
            max_score=1.0,
            passed=passed,
            details=details
        )
    
    def evaluate_day_coverage(self, itinerary: TripItinerary) -> EvaluationMetric:
        """Check if all 3 days are planned"""
        num_days = len(itinerary.days)
        expected_days = 3
        
        score = num_days / expected_days
        passed = num_days == expected_days
        details = f"{num_days}/{expected_days} days planned"
        
        return EvaluationMetric(
            name="Day Coverage",
            score=score,
            max_score=1.0,
            passed=passed,
            details=details
        )
    
    def evaluate_activity_density(self, itinerary: TripItinerary) -> EvaluationMetric:
        """Check if each day has sufficient activities"""
        min_activities_per_day = 3
        
        activities_per_day = [len(day.activities) for day in itinerary.days]
        avg_activities = sum(activities_per_day) / len(activities_per_day) if activities_per_day else 0
        
        score = min(1.0, avg_activities / min_activities_per_day)
        passed = all(count >= min_activities_per_day for count in activities_per_day)
        details = f"Average {avg_activities:.1f} activities/day (min {min_activities_per_day})"
        
        return EvaluationMetric(
            name="Activity Density",
            score=score,
            max_score=1.0,
            passed=passed,
            details=details
        )
    
    def evaluate_preference_matching(self, itinerary: TripItinerary) -> EvaluationMetric:
        """Check if activities match user interests"""
        interests = itinerary.requirements.interests
        if not interests:
            return EvaluationMetric(
                name="Preference Matching",
                score=1.0,
                max_score=1.0,
                passed=True,
                details="No specific interests to match"
            )
        
        # Count activities that match interests (simplified check)
        all_activities = [a for day in itinerary.days for a in day.activities]
        matching_count = 0
        
        for activity in all_activities:
            activity_text = (activity.name + activity.description).lower()
            if any(interest.lower() in activity_text for interest in interests):
                matching_count += 1
        
        match_rate = matching_count / len(all_activities) if all_activities else 0
        score = match_rate
        passed = match_rate >= 0.3  # At least 30% should match
        details = f"{matching_count}/{len(all_activities)} activities match interests ({match_rate*100:.0f}%)"
        
        return EvaluationMetric(
            name="Preference Matching",
            score=score,
            max_score=1.0,
            passed=passed,
            details=details
        )
    
    def evaluate_iteration_efficiency(self, itinerary: TripItinerary) -> EvaluationMetric:
        """Check if solution was found within iteration limit"""
        max_iterations = 3
        actual_iterations = itinerary.iteration_count
        
        score = max(0, 1.0 - ((actual_iterations - 1) / max_iterations))
        passed = actual_iterations <= max_iterations
        details = f"Completed in {actual_iterations}/{max_iterations} iterations"
        
        return EvaluationMetric(
            name="Iteration Efficiency",
            score=score,
            max_score=1.0,
            passed=passed,
            details=details
        )
    
    def evaluate_scenario(self, scenario_name: str, 
                         requirements: TripRequirements) -> EvaluationResult:
        """Evaluate a single test scenario"""
        logger.info("evaluator.scenario_started", scenario=scenario_name)
        
        # Run the agent
        itinerary = self.coordinator.process_request(requirements)
        
        # Compute all metrics
        metrics = [
            self.evaluate_budget_adherence(itinerary),
            self.evaluate_day_coverage(itinerary),
            self.evaluate_activity_density(itinerary),
            self.evaluate_preference_matching(itinerary),
            self.evaluate_iteration_efficiency(itinerary)
        ]
        
        # Calculate overall score
        total_score = sum(m.score * m.max_score for m in metrics)
        max_total = sum(m.max_score for m in metrics)
        overall_score = total_score / max_total if max_total > 0 else 0
        
        # Check if passed (all critical metrics must pass)
        critical_metrics = ["Budget Adherence", "Day Coverage"]
        passed = all(
            m.passed for m in metrics 
            if m.name in critical_metrics
        )
        
        result = EvaluationResult(
            scenario_name=scenario_name,
            metrics=metrics,
            overall_score=overall_score,
            passed=passed,
            itinerary=itinerary
        )
        
        logger.info("evaluator.scenario_completed",
                   scenario=scenario_name,
                   score=overall_score,
                   passed=passed)
        
        return result


def run_evaluation_suite() -> List[EvaluationResult]:
    """Run complete evaluation test suite"""
    print("\n" + "=" * 70)
    print("TRIP PLANNER AGENT - EVALUATION SUITE")
    print("=" * 70 + "\n")
    
    evaluator = AgentEvaluator()
    results = []
    
    # Test Scenario 1: Budget-conscious trip
    print("📊 Scenario 1: Budget-Conscious Trip")
    print("-" * 70)
    scenario1 = TripRequirements(
        destination="Barcelona, Spain",
        start_date="2025-07-01",
        end_date="2025-07-03",
        budget=800.0,  # Tight budget
        num_travelers=1,
        interests=["architecture", "beach"],
        accommodation_preference="hostel"
    )
    result1 = evaluator.evaluate_scenario("Budget-Conscious Trip", scenario1)
    results.append(result1)
    print_evaluation_result(result1)
    
    # Test Scenario 2: Luxury trip
    print("\n📊 Scenario 2: Luxury Experience")
    print("-" * 70)
    scenario2 = TripRequirements(
        destination="Tokyo, Japan",
        start_date="2025-08-15",
        end_date="2025-08-17",
        budget=3000.0,  # High budget
        num_travelers=2,
        interests=["food", "culture", "shopping"],
        dietary_restrictions=["no shellfish"],
        accommodation_preference="luxury hotel"
    )
    result2 = evaluator.evaluate_scenario("Luxury Experience", scenario2)
    results.append(result2)
    print_evaluation_result(result2)
    
    # Test Scenario 3: Family trip
    print("\n📊 Scenario 3: Family Vacation")
    print("-" * 70)
    scenario3 = TripRequirements(
        destination="Orlando, Florida",
        start_date="2025-09-10",
        end_date="2025-09-12",
        budget=1500.0,
        num_travelers=4,
        interests=["theme parks", "entertainment"],
        accommodation_preference="family hotel"
    )
    result3 = evaluator.evaluate_scenario("Family Vacation", scenario3)
    results.append(result3)
    print_evaluation_result(result3)
    
    # Summary
    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)
    
    passed_count = sum(1 for r in results if r.passed)
    avg_score = sum(r.overall_score for r in results) / len(results)
    
    print(f"\nTotal Scenarios: {len(results)}")
    print(f"Passed: {passed_count}/{len(results)}")
    print(f"Average Score: {avg_score*100:.1f}%")
    print(f"Overall Status: {'✓ PASS' if passed_count == len(results) else '✗ FAIL'}")
    
    # Save results
    save_evaluation_results(results)
    
    return results


def print_evaluation_result(result: EvaluationResult):
    """Print formatted evaluation result"""
    print(f"\nScenario: {result.scenario_name}")
    print(f"Overall Score: {result.overall_score*100:.1f}%")
    print(f"Status: {'✓ PASSED' if result.passed else '✗ FAILED'}\n")
    
    print("Metrics:")
    for metric in result.metrics:
        status = "✓" if metric.passed else "✗"
        print(f"  {status} {metric.name}: {metric.score*100:.0f}%")
        print(f"     {metric.details}")
    
    print(f"\nItinerary Summary:")
    print(f"  Destination: {result.itinerary.requirements.destination}")
    print(f"  Budget: ${result.itinerary.requirements.budget:.2f}")
    print(f"  Actual Cost: ${result.itinerary.budget.total:.2f}")
    print(f"  Days Planned: {len(result.itinerary.days)}")
    print(f"  Iterations: {result.itinerary.iteration_count}")


def save_evaluation_results(results: List[EvaluationResult]):
    """Save evaluation results to JSON"""
    output = {
        "evaluation_date": "2025-11-17",
        "total_scenarios": len(results),
        "passed": sum(1 for r in results if r.passed),
        "average_score": sum(r.overall_score for r in results) / len(results),
        "scenarios": []
    }
    
    for result in results:
        scenario_data = {
            "name": result.scenario_name,
            "passed": result.passed,
            "overall_score": result.overall_score,
            "metrics": [
                {
                    "name": m.name,
                    "score": m.score,
                    "passed": m.passed,
                    "details": m.details
                }
                for m in result.metrics
            ],
            "destination": result.itinerary.requirements.destination,
            "budget": result.itinerary.requirements.budget,
            "actual_cost": result.itinerary.budget.total,
            "iterations": result.itinerary.iteration_count
        }
        output["scenarios"].append(scenario_data)
    
    filename = "evaluation_results.json"
    with open(filename, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✓ Evaluation results saved to {filename}")


if __name__ == "__main__":
    results = run_evaluation_suite()
