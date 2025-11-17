# Trip Planner Assistant - Project Pitch

## Track
**Concierge Agents**

## Problem Statement
Planning a multi-day trip is overwhelming and time-consuming. Travelers must juggle multiple concerns simultaneously: finding attractions that match their interests, staying within budget, booking accommodations, and creating a realistic day-by-day schedule. This often requires switching between dozens of websites, spreadsheets, and manual calculations. The process can take 10-20 hours for a single trip, leading to decision fatigue and suboptimal choices.

## Proposed Solution
The **Trip Planner Assistant** is a multi-agent system that automates the entire trip planning workflow. It consists of three specialized agents working in parallel:

1. **Itinerary Planner Agent**: Researches destinations, finds attractions, and creates day-by-day schedules based on user preferences
2. **Budget Analyzer Agent**: Tracks costs across accommodations, activities, and meals; suggests optimizations to stay within budget
3. **Booking Helper Agent**: Finds real-time prices for hotels and flights, provides booking recommendations

These agents collaborate through a coordinator that maintains session memory of user preferences (budget, interests, dietary restrictions, travel dates) and synthesizes their outputs into a cohesive 3-day itinerary.

## Key Features (Competition Requirements)
- **Multi-agent system**: Parallel agents (planner, budgeter, booking helper) with sequential coordinator
- **Tools**: Google Search for attractions/prices, Code Execution for budget calculations, custom API tools for travel data
- **Sessions & Memory**: InMemorySessionService maintains user preferences across iterations; context compaction for long conversations
- **Observability**: Structured logging, tracing of agent decisions, metrics on iteration count and budget accuracy
- **Agent Evaluation**: Automated scoring on constraint satisfaction (budget adherence, day coverage, preference matching)

## Value Proposition
- **Time Savings**: Reduces planning time from 10-20 hours to 30 minutes (3 iterations with the agent)
- **Better Decisions**: Parallel processing ensures budget and preferences are considered simultaneously
- **Personalization**: Memory of past trips and preferences improves recommendations over time
- **Transparency**: Full visibility into agent reasoning and trade-offs through observability layer

## Success Metrics
- Generate complete 3-day itinerary in ≤3 user iterations
- Stay within ±5% of user's stated budget
- Include ≥8 activities matching user preferences per day
- User satisfaction score ≥4/5 in evaluation scenarios
