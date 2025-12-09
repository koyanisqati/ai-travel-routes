"""Minimal HTTP server to expose the planner over the web."""
from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict, List
from urllib.parse import parse_qs, urlparse

from .planner import Preferences, RoutePlanner


class PlannerAPI:
    """Thin wrapper to create JSON-friendly itineraries."""

    def __init__(self) -> None:
        self.planner = RoutePlanner()

    def plan_route(
        self,
        *,
        city: str,
        days: int,
        interests: List[str],
        weather: List[str],
        pace: str = "balanced",
    ) -> Dict:
        preferences = Preferences(city=city, days=days, interests=interests, pace=pace)
        plans = self.planner.generate(preferences, weather)

        return {
            "city": city,
            "days": days,
            "pace": pace,
            "itinerary": [self._serialize_day(day) for day in plans],
        }

    def _serialize_day(self, day_plan) -> Dict:
        return {
            "day": day_plan.day_index,
            "weather": day_plan.weather,
            "visits": [self._serialize_visit(v) for v in day_plan.visits],
        }

    def _serialize_visit(self, visit) -> Dict:
        payload = asdict(visit.poi)
        payload.update(
            {
                "label": visit.label,
                "start_time": self._format_dt(visit.start_time),
                "end_time": self._format_dt(visit.end_time),
                "travel_minutes": visit.travel_minutes,
            }
        )
        return payload

    def _format_dt(self, value: datetime) -> str:
        return value.isoformat(timespec="minutes")


class PlannerHandler(BaseHTTPRequestHandler):
    api = PlannerAPI()

    def do_GET(self):  # noqa: N802 (http server signature)
        parsed = urlparse(self.path)
        if parsed.path in {"/", ""}:
            return self._serve_index()
        if parsed.path == "/plan":
            return self._serve_plan(parsed.query)
        self._send_json(404, {"error": "Not found"})

    def _serve_index(self) -> None:
        message = (
            "<h1>AI Travel Routes</h1>"
            "<p>Use <code>/plan</code> with query params:</p>"
            "<ul>"
            "<li><b>city</b>: Paris, Tokyo, or New York</li>"
            "<li><b>days</b>: 1-5</li>"
            "<li><b>interests</b>: comma-separated categories (art, food, park, landmark)</li>"
            "<li><b>weather</b>: comma-separated daily weather (e.g., sunny,rainy)</li>"
            "<li><b>pace</b>: slow, balanced, or fast (optional)</li>"
            "</ul>"
            "<p>Example: <a href=\"/plan?city=Paris&days=2&interests=art,food&weather=sunny,rainy\">"
            "/plan?city=Paris&days=2&interests=art,food&weather=sunny,rainy</a></p>"
        )
        self._send_html(message)

    def _serve_plan(self, query: str) -> None:
        params = parse_qs(query)
        try:
            city = self._get_param(params, "city")
            days = int(self._get_param(params, "days"))
            interests = self._split_values(self._get_param(params, "interests"))
            weather = self._split_values(self._get_param(params, "weather"))
            pace = params.get("pace", ["balanced"])[0]
            payload = self.api.plan_route(
                city=city, days=days, interests=interests, weather=weather, pace=pace
            )
            self._send_json(200, payload)
        except ValueError as exc:
            self._send_json(400, {"error": str(exc)})

    def _get_param(self, params: Dict[str, List[str]], key: str) -> str:
        values = params.get(key)
        if not values or not values[0].strip():
            raise ValueError(f"Missing required query parameter: {key}")
        return values[0].strip()

    def _split_values(self, raw: str) -> List[str]:
        return [part.strip() for part in raw.replace(";", ",").replace(" ", ",").split(",") if part.strip()]

    def _send_json(self, status: int, payload: Dict) -> None:
        body = json.dumps(payload, indent=2)
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body.encode("utf-8"))))
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def _send_html(self, body: str) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body.encode("utf-8"))))
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def log_message(self, format, *args):  # noqa: A003 (base signature)
        return


def run(host: str = "0.0.0.0", port: int = 8000) -> None:
    server = HTTPServer((host, port), PlannerHandler)
    print(f"Serving AI Travel Routes at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
