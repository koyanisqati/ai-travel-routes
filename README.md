# AI Travel Routes

## Overview
AI Travel Routes is an AI assistant that builds realistic, personalized travel plans and supports travelers on the go. The product focuses on making trips simple, smart, and predictable by combining user preferences with verified local data.

## Vision
Create an assistant that delivers feasible, preference-matched routes within 40 seconds and adapts automatically to weather and day-of changes.

## Problem
Travelers spend 5–30 hours planning, juggling many sources, and risk logistical errors. Existing route generators often ignore realistic distances, opening hours, weather, and user interests, producing chaotic daily plans.

## Target Audience
Digital travelers aged 20–45 who value speed, control, and predictability, starting with millennial and Gen Z early adopters planning trips in Europe, Japan, and the United States.

## Jobs to Be Done
- **Primary JTBD:** When I plan a trip, I want a personalized, realistic route in under a minute to save time and avoid mistakes.
- **Secondary JTBDs:** Adapt routes to weather and last-minute changes; deliver quick in-city recommendations.

## MVP Focus
- **Scenario:** Build a realistic route for 1–5 days.
- **Included:** Preference onboarding, route generation, point editing, map + timeline, weather adaptation, nearby recommendations.
- **Excluded:** Tickets, hotels, documents, budgeting, journaling.

## Route Quality Criteria
- **Feasibility:** Realistic distances and transition times; locations open at scheduled times; visit durations fit the day.
- **Relevance:** At least 70% of points align with user preferences.
- **Cohesion:** Logical day flow.
- **Adaptivity:** Correctly adjusts plans for weather changes.
- **Correction rate:** No more than 1.5 replacements per route day.

## Product Aha Moments
1. A feasible, logical, personalized plan appears within 40 seconds.
2. The route auto-adapts to weather and changing context without manual replanning.

## Architecture (High Level)
Hybrid AI Travel Engine:
1. **LLM layer** for interpreting preferences.
2. **Graph planner** for routing and time calculations.
3. **POI Index** curated for 20 cities.
4. **Weather layer** for forecast-aware adjustments.
5. **Validation rules** to prevent hallucinations and infeasible plans.

## Metrics
- **North Star:** Number of realistic and used routes.
- **Activation:** User received a route and opened the map.
- **Retention:** Route used for at least two consecutive days; user returns after 30 days.
- **Quality:** Feasibility score, correction rate, preference-match score, weather-adaptation success.

## Monetization (post-MVP)
Subscription-first model with optional commissions from local activities. MVP focuses solely on proving value (no monetization at launch).

## Risks and Mitigations
- **AI hallucinations:** Validation rules plus proprietary POI index.
- **High generation costs:** Hybrid model with caching.
- **Integration risk:** MVP excludes tickets and hotels.
- **Differentiation risk:** Emphasize realistic, adaptive routing quality.

## Go-to-Market (MVP)
- **Regions:** Europe, Japan, United States.
- **Channels:** TikTok and Instagram travel creators; SEO for “plan X days” searches; shareable routes to drive organic growth.
- **Goal:** Users share their routes.

## 6-Week Roadmap
- **Weeks 1–2:** Preference onboarding, POI index, prototype LLM + graph planner.
- **Weeks 3–4:** Route generation, weather adaptation, point editing, map and timeline.
- **Weeks 5–6:** UX polish, quality validation, beta test, soft launch.

## MVP Deliverables
- Realistic multi-day routes with preference fit.
- Interactive map and timeline.
- Weather-aware rerouting and nearby recommendations.
- Basic editing of points and day logic.

## Local prototype

This repository includes a lightweight CLI prototype that turns the product brief into a working experience: it selects points of interest for Paris, Tokyo, and New York; sequences them into feasible day plans with opening hours and travel buffers; and adapts to weather by favoring indoor venues on rainy days.

### Quick start

```bash
python -m travel_routes.cli --city Paris --days 2 --interests art food --weather sunny rainy
```

Flags:
- `--city`: Paris, Tokyo, or New York (based on the sample POI index)
- `--days`: number of days to plan (1–5 in the MVP scope)
- `--interests`: one or more categories (`art`, `food`, `park`, `landmark`)
- `--weather`: daily outlooks (e.g., `sunny rainy cloudy`); used to bias indoor picks on bad-weather days
- `--pace`: `slow`, `balanced`, or `fast`; adjusts travel buffers

The output lists each day with start/end times, travel buffers, and human-readable labels for every stop. If no feasible visits are found for the chosen preferences, the CLI prompts you to widen interests or pick another city.

### Web link (local)

Start the built-in HTTP server and open the app in your browser:

```bash
python -m travel_routes.web
```

Then visit: http://localhost:8000/

Example plan endpoint:

```
http://localhost:8000/plan?city=Paris&days=2&interests=art,food&weather=sunny,rainy
```
