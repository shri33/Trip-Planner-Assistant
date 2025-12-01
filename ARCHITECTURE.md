# Trip Planner Assistant - Architecture Design

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
│                  (CLI / Notebook Interface)                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Coordinator Agent (ADK)                     │
│  - Manages conversation flow                                 │
│  - Routes to specialist agents                               │
│  - Synthesizes final itinerary                               │
│  - Session & Memory management                               │
└──────┬──────────────┬──────────────┬───────────────────────┘
       │              │              │
       │ Parallel     │ Execution    │
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐
│ Itinerary   │ │   Budget    │ │    Booking          │
│   Planner   │ │  Analyzer   │ │     Helper          │
│   Agent     │ │   Agent     │ │     Agent           │
└──────┬──────┘ └──────┬──────┘ └──────┬──────────────┘
       │               │               │
       │ Uses Tools    │ Uses Tools    │ Uses Tools
       ▼               ▼               ▼
┌─────────────────────────────────────────────────────────────┐
│                        Tool Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Google Search│  │Code Execution│  │ Custom API Tools │  │
│  │    Tool      │  │     Tool     │  │  (Travel APIs)   │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   Memory & State Layer                       │
│  - InMemorySessionService (conversation state)               │
│  - Memory Bank (user preferences, past trips)                │
│  - Context compaction for long sessions                      │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Observability Layer                         │
│  - Structured logging (Python logging)                       │
│  - Tracing (agent decision paths)                            │
│  - Metrics (latency, token usage, constraint satisfaction)   │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Coordinator Agent
- **Role**: Main orchestrator powered by Gemini LLM
- **Responsibilities**:
  - Parse user requirements (destination, dates, budget, preferences)
  - Delegate to specialist agents in parallel
  - Aggregate results and resolve conflicts
  - Iterate based on user feedback
- **Key Features**:
  - Sequential flow management
  - Session state persistence
  - Context engineering (compaction when token limit approaches)

### 2. Itinerary Planner Agent
- **Role**: Creates day-by-day activity schedule
- **Tools**:
  - Google Search: Find attractions, restaurants, events
  - Code Execution: Calculate travel times between locations
- **Outputs**: 
  - List of activities per day with times
  - Geographic routing optimization
  - Backup options for weather contingencies

### 3. Budget Analyzer Agent
- **Role**: Ensures financial constraints are met
- **Tools**:
  - Code Execution: Sum costs, calculate per-day breakdown
  - Custom budget optimizer tool
- **Outputs**:
  - Total trip cost estimate
  - Per-category breakdown (lodging, food, activities, transport)
  - Savings recommendations

### 4. Booking Helper Agent
- **Role**: Finds real-time pricing and booking options
- **Tools**:
  - Google Search: Hotel/flight prices (simulated API in demo)
  - Custom booking tool (stubbed for demo, can integrate real APIs)
- **Outputs**:
  - Top 3 hotel options with prices
  - Flight recommendations
  - Booking links

## Data Flow

1. **User Input** → Coordinator parses into structured requirements
2. **Parallel Execution** → All 3 agents run simultaneously with shared context
3. **Result Aggregation** → Coordinator merges outputs, checks constraints
4. **Validation** → Budget analyzer verifies total cost ≤ budget
5. **User Feedback** → Refinement iteration (max 3 iterations)
6. **Final Output** → JSON + formatted itinerary with all details

## Technology Stack

- **Framework**: Google ADK-Python
- **LLM**: Gemini 1.5 Pro (with fallback to Gemini 1.5 Flash for speed)
- **Session Management**: InMemorySessionService
- **Memory**: Custom Memory Bank implementation
- **Tools**: 
  - Built-in: Google Search, Code Execution
  - Custom: Budget calculator, Travel API wrapper (stubbed)
- **Observability**: Python `logging` + custom tracing decorator
- **Deployment**: Local (with optional Cloud Run deployment)

## Key Course Features Demonstrated

1. **Multi-agent system**: ✅
   - Parallel agents (3 specialists)
   - Sequential coordinator
   - Agent-to-agent communication

2. **Tools**: ✅
   - Built-in: Google Search, Code Execution
   - Custom tools: Budget optimizer
   
3. **Sessions & Memory**: ✅
   - InMemorySessionService for state
   - Memory Bank for user preferences
   - Context compaction

4. **Observability**: ✅
   - Structured logging
   - Decision tracing
   - Performance metrics

5. **Agent Evaluation**: ✅
   - Automated test scenarios
   - Constraint satisfaction scoring
   - User feedback simulation

## Scalability Considerations

- **Token Management**: Context compaction kicks in at 80% of model limit
- **Cost Optimization**: Use Flash for routine queries, Pro for complex planning
- **Caching**: Store common destinations/prices in Memory Bank
- **Rate Limiting**: Respect tool API limits with exponential backoff
