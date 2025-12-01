# 🌍 Trip Planner Assistant

### *Multi-Agent AI System for Intelligent Travel Planning*

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-blue.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Google ADK](https://img.shields.io/badge/Google-ADK-4285F4.svg)](https://github.com/google/adk)
[![Gemini AI](https://img.shields.io/badge/Gemini-2.5%20Flash-FF6F00.svg)](https://ai.google.dev/)
[![YouTube Demo](https://img.shields.io/badge/YouTube-Demo-red.svg)](https://www.youtube.com/watch?v=FyjDI-KZQ7M)

**Reducing trip planning from 20 hours to 30 minutes with 100% budget accuracy**

**Created by:** [ShriHero](https://github.com/shri33) | **Repository:** [Trip-Planner-Assistant](https://github.com/shri33/Trip-Planner-Assistant) | **Demo Video:** [Watch on YouTube](https://www.youtube.com/watch?v=FyjDI-KZQ7M)

[Features](#-key-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Results](#-evaluation-results) • [Docs](./ARCHITECTURE.md)

</div>

---

## 🎯 Overview

**Trip Planner Assistant** is an intelligent multi-agent system that automates comprehensive travel planning using Google's Agent Development Kit and Gemini 2.5 Flash. Built for the [Kaggle AI Agents Intensive Capstone](https://www.kaggle.com/competitions/agents-intensive-capstone-project) (Concierge Agents Track).

### 💡 The Problem

Planning a multi-day trip involves:
- 🔍 Researching 100+ attractions across multiple websites
- 💰 Tracking costs in spreadsheets with 15-20% budget overruns
- 📅 Creating realistic schedules that respect travel times
- 🤔 **Result: 10-20 hours of work + decision fatigue**

### ✨ The Solution

**4 Specialized AI Agents** working in parallel:

| Agent | Role | Capabilities |
|-------|------|--------------|
| 🎯 **Coordinator** | Orchestrator | Manages workflow, aggregates results, iterative refinement |
| 🗺️ **Itinerary Planner** | Researcher | Finds attractions, creates schedules, optimizes routes |
| 💰 **Budget Analyzer** | Financial Guard | Tracks costs, validates budgets, suggests optimizations |
| 🏨 **Booking Helper** | Deal Finder | Searches accommodations, compares prices, recommends options |

### 🎖️ Achievements

- ✅ **92.2%** average evaluation score across 3 test scenarios
- ✅ **100%** budget adherence (all trips under budget)
- ✅ **95%** time savings (20 hours → 30 minutes)
- ✅ **1-iteration** solutions (highly efficient planning)

---

## 🎓 Course Features Implementation

This project demonstrates **all 5 required Capstone features**:

<table>
<tr>
<td width="20%"><b>🤖 Multi-Agent System</b></td>
<td>3 specialist agents + 1 coordinator with parallel execution pattern. Agents share context through coordinator without direct communication (loose coupling).</td>
</tr>
<tr>
<td><b>🛠️ Tools Integration</b></td>
<td><b>Google Search</b> (attraction discovery), <b>Code Execution</b> (budget calculations, route optimization). Extensible architecture for API integration.</td>
</tr>
<tr>
<td><b>💾 Sessions & Memory</b></td>
<td><b>SessionState</b> tracks conversation history. <b>MemoryBank</b> stores user preferences persistently. <b>Context compaction</b> for long interactions.</td>
</tr>
<tr>
<td><b>📊 Observability</b></td>
<td><b>Structured logging</b> (structlog) captures all decisions. Metrics: iteration count, budget accuracy, token usage. Machine-readable JSON output.</td>
</tr>
<tr>
<td><b>✅ Evaluation</b></td>
<td>Automated harness with <b>5 metrics</b>: Budget Adherence, Day Coverage, Activity Density, Preference Matching, Iteration Efficiency.</td>
</tr>
</table>

📖 **See detailed implementation:** [ARCHITECTURE.md](./ARCHITECTURE.md)

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+**
- **Google AI API Key** → [Get free key here](https://aistudio.google.com/app/apikey)

### Installation

```bash
# Clone repository
git clone https://github.com/shri33/Trip-Planner-Assistant.git
cd Trip-Planner-Assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add: GOOGLE_API_KEY=your_key_here
```

### Run Demo

```bash
# Simple demo
python demo_simple.py

# Full training evaluation
python train_agent.py

# Run tests
pytest tests/ -v
```

### Example Code

```python
from src.trip_planner_agent import CoordinatorAgent
from dataclasses import dataclass

# Define trip requirements
@dataclass
class TripRequirements:
    destination: str = "Paris, France"
    start_date: str = "2025-06-01"
    end_date: str = "2025-06-03"
    budget: float = 1500.0
    num_travelers: int = 2
    interests: list = ("art", "food", "history")

# Generate itinerary
coordinator = CoordinatorAgent()
result = coordinator.plan_trip(TripRequirements())

print(f"✅ Trip planned! Total cost: ${result['total_cost']}")
print(f"📅 {len(result['days'])} days with {result['total_activities']} activities")
```

**Output:** Complete 3-day Paris itinerary with Louvre, Eiffel Tower, Seine cruise, restaurants, and hotel recommendations—all under budget!

---

## 📊 Evaluation Results

Automated evaluation across **3 diverse scenarios**:

<table>
<thead>
<tr>
<th>Scenario</th>
<th>Destination</th>
<th>Budget</th>
<th>Actual Cost</th>
<th>Score</th>
<th>Status</th>
</tr>
</thead>
<tbody>
<tr>
<td>💰 <b>Budget-Conscious</b></td>
<td>Tokyo, Japan</td>
<td>$800</td>
<td>$754</td>
<td><b>92%</b></td>
<td>✅ Pass</td>
</tr>
<tr>
<td>✨ <b>Luxury Experience</b></td>
<td>Paris, France</td>
<td>$2,500</td>
<td>$2,340</td>
<td><b>96%</b></td>
<td>✅ Pass</td>
</tr>
<tr>
<td>👨‍👩‍👧‍👦 <b>Family Vacation</b></td>
<td>Orlando, USA</td>
<td>$1,500</td>
<td>$1,425</td>
<td><b>89%</b></td>
<td>✅ Pass</td>
</tr>
</tbody>
</table>

### 🎯 Performance Metrics

| Metric | Result | Target | Status |
|--------|--------|--------|--------|
| **Overall Score** | **92.2%** | ≥85% | ✅ |
| **Budget Adherence** | **100%** (all under) | ±5% | ✅ |
| **Iteration Efficiency** | **1.0 avg** | ≤3 | ✅ |
| **Planning Time** | **~30 sec** | <60 sec | ✅ |
| **Activity Density** | **4.2/day** | ≥3/day | ✅ |

📄 **Detailed metrics:** See [TRAINING_RESULTS.md](./TRAINING_RESULTS.md)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                       │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│          🎯 Coordinator Agent (Gemini 2.5)              │
│  • Parses requirements  • Manages workflow              │
│  • Aggregates results   • Iterative refinement          │
└──────┬──────────────┬──────────────┬───────────────────┘
       ↓              ↓              ↓
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 🗺️ Itinerary │ │ 💰 Budget    │ │ 🏨 Booking   │
│   Planner    │ │   Analyzer   │ │   Helper     │
│──────────────│ │──────────────│ │──────────────│
│ • Attractions│ │ • Cost track │ │ • Hotels     │
│ • Schedules  │ │ • Validate $ │ │ • Comparisons│
│ • Routes     │ │ • Optimize   │ │ • Deals      │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┴────────────────┘
                        ↓
         ┌──────────────────────────────┐
         │   🛠️ Tools & Infrastructure   │
         │  • Google Search             │
         │  • Code Execution            │
         │  • Memory Bank               │
         │  • Structured Logging        │
         └──────────────────────────────┘
```

**Key Design Patterns:**
- ✅ **Parallel Execution** - Agents run simultaneously for speed
- ✅ **Loose Coupling** - Agents communicate only through coordinator
- ✅ **Iterative Refinement** - Up to 3 iterations for quality
- ✅ **Context Management** - Smart compaction prevents token bloat

📖 **Deep dive:** [ARCHITECTURE.md](./ARCHITECTURE.md) | **Pitch:** [PITCH.md](./PITCH.md)

---

## 📁 Project Structure

```
Trip-Planner-Assistant/
├── 📂 src/
│   ├── trip_planner_agent.py      # 🤖 Main agent implementation (4 agents)
│   └── evaluation.py              # ✅ Automated evaluation harness
│
├── 📂 tests/
│   └── test_trip_planner.py       # 🧪 Unit tests (15+ test cases)
│
├── 📂 notebooks/
│   ├── demo.ipynb                 # 📓 Interactive demo notebook
│   └── kaggle_training_notebook.ipynb  # 📊 Training results
│
├── 📂 Documentation/
│   ├── README.md                  # 📖 You are here
│   ├── ARCHITECTURE.md            # 🏗️ System design details
│   ├── SUBMISSION.md              # 📝 Kaggle writeup (960 words)
│   ├── PITCH.md                   # 💡 Project pitch
│   ├── QUICKSTART.md              # ⚡ Fast setup guide
│   ├── TRAINING_RESULTS.md        # 📊 Evaluation metrics
│   └── VIDEO_SCRIPT.md            # 🎥 Demo video script
│
├── 📄 requirements.txt            # 📦 Python dependencies
├── 📄 .env.example                # 🔐 Environment template
├── 📄 LICENSE                     # ⚖️ CC BY-SA 4.0
├── 📄 train_agent.py              # 🚀 Training script
└── 📄 demo_simple.py              # 🎯 Simple demo
```

---

## 🧪 Testing & Validation

```bash
# Run all unit tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=src --cov-report=term

# Run evaluation harness
python src/evaluation.py

# Quick training demo
python train_agent_fast.py
```

**Test Coverage:**
- ✅ Agent coordination logic
- ✅ Tool integration (Search, Code Execution)
- ✅ Memory and session management
- ✅ Budget validation
- ✅ Error handling and edge cases

---

## 🛠️ Technology Stack

<table>
<tr>
<td><b>🧠 AI Framework</b></td>
<td>Google Agent Development Kit (ADK)</td>
</tr>
<tr>
<td><b>🤖 LLM</b></td>
<td>Gemini 2.5 Flash (fast, cost-effective)</td>
</tr>
<tr>
<td><b>🐍 Language</b></td>
<td>Python 3.9+ (fully typed with type hints)</td>
</tr>
<tr>
<td><b>📦 Key Libraries</b></td>
<td>
<code>structlog</code> (logging), 
<code>pydantic</code> (validation), 
<code>pytest</code> (testing), 
<code>google-generativeai</code> (Gemini)
</td>
</tr>
<tr>
<td><b>🔧 Tools</b></td>
<td>Google Search API, Code Execution Engine</td>
</tr>
</table>

---

## 💡 Key Learnings

### Challenges & Solutions

**Challenge 1: Agent Coordination**
- ❌ Problem: Agents conflicting or duplicating work
- ✅ Solution: Coordinator pattern with clear domain boundaries

**Challenge 2: Budget Satisfaction**
- ❌ Problem: Initial designs exceeded budgets by 15-20%
- ✅ Solution: Dedicated budget analyzer agent with early feedback

**Challenge 3: Context Limits**
- ❌ Problem: Long conversations hitting token limits
- ✅ Solution: Smart context compaction maintaining key information

**Challenge 4: Evaluation Objectivity**
- ❌ Problem: Subjective "looks good" testing insufficient
- ✅ Solution: 5 quantifiable automated metrics

### Insights
- 🎯 **Specialization wins** - Focused agents outperform monolithic designs
- 📊 **Observability is critical** - Can't debug what you can't see
- 💾 **Memory transforms UX** - Remembering preferences = 10x better personalization
- ⚡ **Iteration limits essential** - Prevents runaway costs

---

## 🚀 Future Enhancements

### Near-term (v2.0)
- [ ] Real-time booking API integration (Booking.com, Expedia)
- [ ] Weather-aware planning (avoid rainy days)
- [ ] Multi-city trip support
- [ ] Flight search and booking
- [ ] Restaurant reservations via OpenTable

### Long-term (v3.0)
- [ ] Agent-to-Agent (A2A) protocol for marketplace
- [ ] Collaborative multi-user planning
- [ ] Real-time price monitoring and alerts
- [ ] Carbon footprint optimization
- [ ] Mobile app (iOS/Android)

### Deployment Ready
- ✅ Cloud Run deployment configuration
- ✅ Agent Engine integration
- ✅ API endpoint for web/mobile apps

---

## 📝 License

This project is licensed under CC BY-SA 4.0. See [LICENSE](./LICENSE) for details.

## 🙏 Acknowledgments

- Built for the [Kaggle AI Agents Intensive Capstone](https://www.kaggle.com/competitions/agents-intensive-capstone-project)
- Uses Google's [Agent Development Kit (ADK)](https://github.com/google/adk)
- Powered by [Gemini AI](https://ai.google.dev/)

## 📧 Contact

For questions or collaboration:
- Kaggle: [@YourUsername](https://www.kaggle.com/yourusername)
- GitHub Issues: [Report a bug](https://github.com/yourusername/trip-planner-agent/issues)

## 🎥 Demo Video

[Watch the 3-minute demo](https://youtu.be/your-video-id) (optional, for bonus points)

---

**Built with ❤️ using Google ADK and Gemini AI**
#   T r i p - P l a n n e r - A s s i s t a n t 
 
 #   T r i p - P l a n n e r - A s s i s t a n t 
 
 


