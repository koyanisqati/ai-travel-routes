"""Sample POI data and helper utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class POI:
    name: str
    city: str
    category: str
    duration_minutes: int
    open_from: int  # 24h int
    open_to: int
    is_indoor: bool
    neighborhood: str


POI_INDEX: List[POI] = [
    POI(
        name="Louvre Museum",
        city="Paris",
        category="art",
        duration_minutes=180,
        open_from=9,
        open_to=18,
        is_indoor=True,
        neighborhood="Center",
    ),
    POI(
        name="Musée d'Orsay",
        city="Paris",
        category="art",
        duration_minutes=120,
        open_from=9,
        open_to=18,
        is_indoor=True,
        neighborhood="Left Bank",
    ),
    POI(
        name="Luxembourg Gardens",
        city="Paris",
        category="park",
        duration_minutes=90,
        open_from=7,
        open_to=21,
        is_indoor=False,
        neighborhood="Left Bank",
    ),
    POI(
        name="Eiffel Tower",
        city="Paris",
        category="landmark",
        duration_minutes=90,
        open_from=9,
        open_to=23,
        is_indoor=False,
        neighborhood="7th",
    ),
    POI(
        name="Tokyo National Museum",
        city="Tokyo",
        category="art",
        duration_minutes=150,
        open_from=9,
        open_to=17,
        is_indoor=True,
        neighborhood="Ueno",
    ),
    POI(
        name="Ueno Park",
        city="Tokyo",
        category="park",
        duration_minutes=120,
        open_from=5,
        open_to=23,
        is_indoor=False,
        neighborhood="Ueno",
    ),
    POI(
        name="Tsukiji Outer Market",
        city="Tokyo",
        category="food",
        duration_minutes=90,
        open_from=7,
        open_to=15,
        is_indoor=False,
        neighborhood="Chuo",
    ),
    POI(
        name="Meiji Shrine",
        city="Tokyo",
        category="landmark",
        duration_minutes=90,
        open_from=6,
        open_to=18,
        is_indoor=False,
        neighborhood="Shibuya",
    ),
    POI(
        name="Metropolitan Museum of Art",
        city="New York",
        category="art",
        duration_minutes=180,
        open_from=10,
        open_to=17,
        is_indoor=True,
        neighborhood="Upper East Side",
    ),
    POI(
        name="Central Park",
        city="New York",
        category="park",
        duration_minutes=150,
        open_from=6,
        open_to=1,
        is_indoor=False,
        neighborhood="Manhattan",
    ),
    POI(
        name="Chelsea Market",
        city="New York",
        category="food",
        duration_minutes=90,
        open_from=8,
        open_to=21,
        is_indoor=True,
        neighborhood="Chelsea",
    ),
    POI(
        name="Brooklyn Museum",
        city="New York",
        category="art",
        duration_minutes=120,
        open_from=11,
        open_to=18,
        is_indoor=True,
        neighborhood="Brooklyn",
    ),
]


CATEGORY_LABELS: Dict[str, str] = {
    "art": "Museums & galleries",
    "food": "Markets & dining",
    "park": "Parks & gardens",
    "landmark": "Iconic landmarks",
}
