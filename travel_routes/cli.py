"""Simple CLI for generating AI travel routes."""

from __future__ import annotations

import argparse
from typing import List

from .planner import Preferences, RoutePlanner


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a realistic, preference-aware travel route.")
    parser.add_argument("--city", required=True, help="City to plan (Paris, Tokyo, New York)")
    parser.add_argument("--days", type=int, default=1, help="Number of days (1-5)")
    parser.add_argument(
        "--interests",
        nargs="+",
        required=True,
        help="Interest categories (art, food, park, landmark)",
    )
    parser.add_argument(
        "--weather",
        nargs="+",
        required=True,
        help="Daily weather outlook (e.g., sunny rainy cloudy). Provide one per day.",
    )
    parser.add_argument(
        "--pace",
        default="balanced",
        choices=["slow", "balanced", "fast"],
        help="Travel pace to adjust transit buffers.",
    )
    return parser.parse_args()


def format_plan(plan) -> str:
    output: List[str] = []
    for day in plan:
        output.append(f"Day {day.day_index} — Weather: {day.weather}")
        for visit in day.visits:
            start = visit.start_time.strftime("%H:%M")
            end = visit.end_time.strftime("%H:%M")
            output.append(
                f"  • {start}–{end} ({visit.travel_minutes}m travel) {visit.label}"
            )
        if not day.visits:
            output.append("  • No feasible visits found. Try broader interests or another city.")
        output.append("")
    return "\n".join(output).strip()


def main() -> None:
    args = parse_args()
    preferences = Preferences(
        city=args.city,
        days=args.days,
        interests=args.interests,
        pace=args.pace,
    )
    planner = RoutePlanner()
    plan = planner.generate(preferences, args.weather)
    print(format_plan(plan))


if __name__ == "__main__":
    main()
