"""Route planning logic for AI Travel Routes."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterable, List, Sequence

from .data import POI, POI_INDEX, CATEGORY_LABELS


@dataclass
class Preferences:
    city: str
    days: int
    interests: Sequence[str]
    pace: str = "balanced"  # slow | balanced | fast


@dataclass
class Visit:
    poi: POI
    start_time: datetime
    end_time: datetime
    travel_minutes: int

    @property
    def label(self) -> str:
        category = CATEGORY_LABELS.get(self.poi.category, self.poi.category.title())
        return f"{self.poi.name} — {category}"


@dataclass
class DayPlan:
    day_index: int
    weather: str
    visits: List[Visit]

    @property
    def total_visit_minutes(self) -> int:
        return sum(v.poi.duration_minutes for v in self.visits)

    @property
    def total_travel_minutes(self) -> int:
        return sum(v.travel_minutes for v in self.visits)


class RoutePlanner:
    START_HOUR = 9
    END_HOUR = 18
    DEFAULT_TRAVEL = 30
    PACE_MULTIPLIER = {"slow": 0.8, "balanced": 1.0, "fast": 1.2}

    def __init__(self, pois: Iterable[POI] = POI_INDEX) -> None:
        self.pois = list(pois)

    def generate(self, preferences: Preferences, weather_by_day: Sequence[str]) -> List[DayPlan]:
        self._validate_inputs(preferences, weather_by_day)
        filtered = self._filter_pois(preferences)
        plans: List[DayPlan] = []

        for day in range(preferences.days):
            weather = weather_by_day[day] if day < len(weather_by_day) else "sunny"
            day_start = datetime.combine(datetime.today().date(), datetime.min.time())
            day_start = day_start.replace(hour=self.START_HOUR, minute=0)
            visits = self._build_day(filtered, day_start, weather, preferences.pace)
            plans.append(DayPlan(day_index=day + 1, weather=weather, visits=visits))
        return plans

    def _validate_inputs(self, preferences: Preferences, weather_by_day: Sequence[str]) -> None:
        if preferences.days < 1 or preferences.days > 5:
            raise ValueError("Days must be between 1 and 5 for the MVP scope.")
        if not preferences.interests:
            raise ValueError("At least one interest must be provided.")
        if preferences.city.lower() not in {p.city.lower() for p in self.pois}:
            raise ValueError("City is not available in the POI index.")
        if preferences.pace not in self.PACE_MULTIPLIER:
            raise ValueError("Pace must be slow, balanced, or fast.")
        if not weather_by_day:
            raise ValueError("Weather forecast is required for at least one day.")

    def _filter_pois(self, preferences: Preferences) -> List[POI]:
        city_pois = [p for p in self.pois if p.city.lower() == preferences.city.lower()]
        preferred = [p for p in city_pois if p.category in preferences.interests]
        if len(preferred) < 3:
            # Backfill with diverse options to keep the route cohesive.
            fallback = [p for p in city_pois if p.category not in preferences.interests]
            preferred.extend(fallback[: max(0, 3 - len(preferred))])
        return preferred

    def _build_day(
        self, pois: List[POI], start: datetime, weather: str, pace: str
    ) -> List[Visit]:
        visits: List[Visit] = []
        current_time = start
        available_pois = sorted(pois, key=lambda p: p.open_from)
        weather_sensitive = [p for p in available_pois if p.is_indoor]
        weather_friendly = available_pois if weather == "sunny" else weather_sensitive

        for poi in weather_friendly:
            travel_buffer = int(self.DEFAULT_TRAVEL / self.PACE_MULTIPLIER[pace])
            visit_start = max(current_time + timedelta(minutes=travel_buffer), self._time_at_hour(current_time, poi.open_from))
            visit_end = visit_start + timedelta(minutes=poi.duration_minutes)

            if visit_end.hour >= poi.open_to:
                continue
            if visit_end.hour >= self.END_HOUR:
                break

            visits.append(
                Visit(
                    poi=poi,
                    start_time=visit_start,
                    end_time=visit_end,
                    travel_minutes=travel_buffer,
                )
            )
            current_time = visit_end

        return visits

    def _time_at_hour(self, base_time: datetime, hour: int) -> datetime:
        return base_time.replace(hour=hour, minute=0)
