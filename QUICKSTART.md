# 🚀 Quick Start Guide

## Trip Planner Assistant - 5 Minute Setup

### Option 1: Instant Demo (No Installation Required)

**Fastest way to see the agent in action:**

```powershell
cd trip-planner-agent
python demo_simple.py
```

**What you'll see:**
- Multi-agent system planning a Paris trip
- 3-day itinerary with activities and costs
- Budget analysis and booking options
- JSON export of the itinerary

**Time:** ~30 seconds

---

### Option 2: Full Installation (With Dependencies)

**For complete features including evaluation and tests:**

1. **Create virtual environment:**
```powershell
python -m venv venv
venv\Scripts\activate
```

2. **Install dependencies:**
```powershell
pip install -r requirements.txt
```

3. **Run the main demo:**
```powershell
cd src
python trip_planner_agent.py
```

4. **Run evaluation suite:**
```powershell
python evaluation.py
```

5. **Run tests:**
```powershell
cd ..
pytest tests/ -v --cov=src
```

**Time:** ~5 minutes

---

### Option 3: Interactive Notebook

**For hands-on experimentation:**

1. **Install Jupyter:**
```powershell
pip install jupyter
```

2. **Launch notebook:**
```powershell
jupyter notebook notebooks/demo.ipynb
```

3. **Run cells interactively** to:
   - Plan custom trips
   - Modify parameters
   - See agent decisions step-by-step

**Time:** ~10 minutes

---

### Option 4: Upload to Kaggle Notebook

**To run in Kaggle's environment:**

1. Go to https://www.kaggle.com/code
2. Click "New Notebook"
3. Upload `notebooks/demo.ipynb`
4. Upload `src/trip_planner_agent.py` and `src/evaluation.py`
5. Run the notebook cells

**No local installation needed!**

---

## 📋 What Each File Does

| File | Purpose | When to Use |
|------|---------|-------------|
| `demo_simple.py` | Standalone demo, no deps | Quick test |
| `src/trip_planner_agent.py` | Full implementation | Main development |
| `src/evaluation.py` | Evaluation metrics | Quality testing |
| `tests/test_trip_planner.py` | Unit tests | Validation |
| `notebooks/demo.ipynb` | Interactive tutorial | Learning |

---

## 🎯 Usage Examples

### Example 1: Plan a Trip

```python
from trip_planner_agent import CoordinatorAgent, TripRequirements

# Create request
trip = TripRequirements(
    destination="Tokyo, Japan",
    start_date="2025-08-01",
    end_date="2025-08-03",
    budget=2500.0,
    num_travelers=2,
    interests=["food", "culture", "technology"]
)

# Get itinerary
coordinator = CoordinatorAgent()
itinerary = coordinator.process_request(trip)

# Display
print(format_itinerary(itinerary))
```

### Example 2: Run Evaluation

```python
from evaluation import AgentEvaluator

evaluator = AgentEvaluator()
result = evaluator.evaluate_scenario("My Trip", trip)

print(f"Score: {result.overall_score*100:.1f}%")
print(f"Status: {'PASS' if result.passed else 'FAIL'}")
```

### Example 3: Check Memory

```python
# View past trips
for trip in coordinator.memory.past_trips:
    print(f"{trip.requirements.destination} - ${trip.budget.total}")

# Store preference
coordinator.memory.store_preference("favorite_city", "Paris")
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'structlog'"

**Solution:** Use the simplified demo instead:
```powershell
python demo_simple.py
```

Or install dependencies:
```powershell
pip install -r requirements.txt
```

### "No such file or directory"

**Solution:** Make sure you're in the right directory:
```powershell
cd c:\Users\shris\Downloads\KAGGLE\trip-planner-agent
```

### Tests fail with import errors

**Solution:** Run tests from project root:
```powershell
cd trip-planner-agent
pytest tests/ -v
```

---

## 📚 Next Steps

1. ✅ **Run Demo**: Start with `demo_simple.py`
2. 📖 **Read Docs**: Check out `README.md`
3. 🏗️ **Explore Code**: Look at `src/trip_planner_agent.py`
4. 🧪 **Run Tests**: Execute `pytest tests/`
5. 📊 **View Results**: Check evaluation metrics
6. 🎨 **Customize**: Modify for your use case
7. 🚀 **Deploy**: Optional Cloud Run deployment

---

## 🎓 Learning Path

**Beginner:**
1. Run `demo_simple.py`
2. Read `PITCH.md`
3. Explore notebook

**Intermediate:**
1. Run full `trip_planner_agent.py`
2. Read `ARCHITECTURE.md`
3. Modify agent behavior

**Advanced:**
1. Add real API integration
2. Extend with new agents
3. Deploy to production

---

## 💡 Tips

- **Start Simple**: Use `demo_simple.py` first
- **No API Keys**: Demo works without any configuration
- **Customize Later**: Get it running, then modify
- **Check Logs**: Look for INFO messages to see agent decisions
- **Read Comments**: Code has extensive inline documentation

---

## 🆘 Help

**Need Help?**
- Check `README.md` for full documentation
- Review `ARCHITECTURE.md` for design details
- See `SUBMISSION.md` for project writeup
- Look at `PROJECT_SUMMARY.md` for overview

**Issues?**
- Ensure Python 3.9+ is installed
- Try `demo_simple.py` for dependency-free demo
- Check you're in the right directory

---

## ✅ Verify Installation

Run this to check everything works:

```powershell
# Test simple demo
python demo_simple.py

# Should output:
# - Trip planning logs
# - Complete itinerary
# - Budget breakdown
# - "✓ Itinerary saved to trip_itinerary_simple.json"
```

**Success!** You're ready to explore the Trip Planner Assistant.

---

*Questions? Check the docs or run `python demo_simple.py` to get started!*
