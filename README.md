🌍 Trip Planner Assistant
Multi-Agent AI System for Intelligent Travel Planning










Reducing trip planning from 20 hours to 30 minutes with 100% budget accuracy

Created by: ShriHero

Repository: Trip-Planner-Assistant

Demo Video: Watch on YouTube

🔗 Navigation

Features
 • Quick Start
 • Architecture
 • Evaluation
 • Documentation

🎯 Overview

Trip Planner Assistant is an intelligent multi-agent system that automates travel planning using Google ADK and Gemini 2.5 Flash, built for the Kaggle AI Agents Intensive Capstone (Concierge Agents Track).

💡 The Problem

Planning a multi-day trip involves:

🔍 Researching 100+ attractions

💰 Budgeting with spreadsheets

🚗 Accounting for travel time

😩 Result: 10–20 hours + decision fatigue

✨ The Solution — 4 Specialized AI Agents
Agent	Role	Capabilities
🎯 Coordinator	Orchestrator	Manages workflow, merges results, iterative refinement
🗺️ Itinerary Planner	Researcher	Discovers attractions, builds day plans, optimizes routes
💰 Budget Analyzer	Financial Guard	Ensures spending stays within budget
🏨 Booking Helper	Deal Finder	Suggests hotels, compares prices
🎖️ Achievements

✅ 92.2% average evaluation score

✅ 100% budget adherence

✅ 95% reduction in planning time

✅ 1-iteration solutions

🎓 Capstone Features Implementation
Requirement	Implemented
🤖 Multi-Agent System	4 agents + coordinator (parallel execution)
🛠️ Tools	Google Search, Code Execution
💾 Memory & Sessions	SessionState + MemoryBank
📊 Observability	structlog + metrics + JSON traces
🧪 Evaluation	Automated scoring with 5 KPIs

📖 Detailed implementation: ARCHITECTURE.md

🚀 Quick Start
Prerequisites

Python 3.9+

Google AI API Key → https://aistudio.google.com/app/apikey

Installation
# Clone repository
git clone https://github.com/shri33/Trip-Planner-Assistant.git
cd Trip-Planner-Assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your Google API key:
# GOOGLE_API_KEY=your_key_here

Run Demo
python demo_simple.py

Full training evaluation
python train_agent.py

Run tests
pytest tests/ -v

Example Usage
from src.trip_planner_agent import CoordinatorAgent
from dataclasses import dataclass

@dataclass
class TripRequirements:
    destination: str = "Paris, France"
    start_date: str = "2025-06-01"
    end_date: str = "2025-06-03"
    budget: float = 1500.0
    num_travelers: int = 2
    interests: list = ("art", "food", "history")

coordinator = CoordinatorAgent()
result = coordinator.plan_trip(TripRequirements())

print(f"✅ Trip planned! Total cost: ${result['total_cost']}")
print(f"📅 {len(result['days'])} days with {result['total_activities']} activities")

📊 Evaluation Results

Automated evaluation across 3 scenarios:

Scenario	Destination	Budget	Actual Cost	Score	Status
💰 Budget-Conscious	Tokyo, Japan	$800	$754	92%	✅ Pass
✨ Luxury Experience	Paris, France	$2,500	$2,340	96%	✅ Pass
👨‍👩‍👧‍👦 Family Trip	Orlando, USA	$1,500	$1,425	89%	✅ Pass
🎯 Performance Metrics
Metric	Result	Target	Status
Overall Score	92.2%	≥85%	✅
Budget Adherence	100%	±5%	✅
Iteration Efficiency	1.0	≤3	✅
Planning Time	~30 sec	<60 sec	✅
Activity Density	4.2/day	≥3/day	✅

📄 Full Results: TRAINING_RESULTS.md

🏗️ Architecture
┌───────────────────────────────────────────────┐
│ User Interface                                 │
└───────────────┬───────────────────────────────┘
                ↓
┌───────────────────────────────────────────────┐
│ 🎯 Coordinator Agent (Gemini 2.5)              │
└───────┬───────────────┬───────────────┬───────┘
        ↓               ↓               ↓
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 🗺️ Itinerary  │ │ 💰 Budget    │ │ 🏨 Booking   │
│ Planner       │ │ Analyzer     │ │ Helper       │
└─────┬────────┘ └──────┬───────┘ └──────┬───────┘
      │                  │                │
      └──────────┬───────┴────────────────┘
                 ↓
      🛠️ Tools: Search, Code Execution,
          Memory, Structured Logging


📖 Deep Dive:

ARCHITECTURE.md

PITCH.md

📁 Project Structure
Trip-Planner-Assistant/
├── src/
│   ├── trip_planner_agent.py
│   ├── evaluation.py
├── tests/
│   └── test_trip_planner.py
├── notebooks/
│   ├── demo.ipynb
│   └── kaggle_training_notebook.ipynb
├── Documentation/
│   ├── ARCHITECTURE.md
│   ├── SUBMISSION.md
│   ├── PITCH.md
│   ├── QUICKSTART.md
│   ├── TRAINING_RESULTS.md
│   └── VIDEO_SCRIPT.md
├── requirements.txt
├── .env.example
├── LICENSE
├── train_agent.py
└── demo_simple.py

🧪 Testing & Validation
pytest tests/ -v
pytest tests/ -v --cov=src --cov-report=term
python src/evaluation.py
python train_agent_fast.py

🛠️ Technology Stack
Component	Technology
AI Framework	Google Agent Development Kit (ADK)
LLM	Gemini 2.5 Flash
Language	Python 3.9+
Logging	structlog
Validation	pydantic
Testing	pytest
Tools	Google Search API, Code Execution
💡 Key Learnings
Challenges

Agent coordination

Budget accuracy

Context limits

Evaluation objectivity

Solutions

Coordinator pattern

Dedicated budget agent

Smart context compaction

Automated metric-based evaluation

🚀 Future Enhancements
v2.0

Real-time booking APIs

Weather-aware scheduling

Multi-city trips

Flight search

Restaurant reservations

v3.0

Multi-user collaborative planning

Continuous price monitoring

Carbon footprint optimization

Mobile app

📝 License

Licensed under CC BY-SA 4.0.
See LICENSE
.

🙏 Acknowledgments

Built for the Kaggle AI Agents Intensive Capstone

Using Google ADK & Gemini AI

📧 Contact

Kaggle: Add your profile link

GitHub Issues: Repo issues link

🎥 Demo

🎬 3-minute demo video:
https://www.youtube.com/watch?v=your-video-id

Built with ❤️ using Google ADK and Gemini AI
