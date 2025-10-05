"""Constants and reference data for the Gakumas Share application."""

import json
from pathlib import Path
from typing import Dict, List, Optional

# Get the data directory path
DATA_DIR = Path(__file__).parent.parent / "data" / "json"


def load_json_data(filename: str) -> List[Dict]:
    """Load JSON data from file."""
    file_path = DATA_DIR / filename
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Could not load {filename}: {e}")
        return []


# Load game data from JSON files
IDOLS: List[Dict] = load_json_data("idols.json")
P_IDOLS: List[Dict] = load_json_data("p_idols.json")
P_ITEMS: List[Dict] = load_json_data("p_items.json")
SKILL_CARDS: List[Dict] = load_json_data("skill_cards.json")
STAGES: List[Dict] = load_json_data("stages.json")

# Create lookup dictionaries
IDOLS_BY_ID: Dict[int, Dict] = {idol["id"]: idol for idol in IDOLS}
IDOLS_BY_NAME: Dict[str, Dict] = {idol["name"]: idol for idol in IDOLS}

P_IDOLS_BY_ID: Dict[int, Dict] = {pidol["id"]: pidol for pidol in P_IDOLS}
P_ITEMS_BY_ID: Dict[int, Dict] = {item["id"]: item for item in P_ITEMS}
SKILL_CARDS_BY_ID: Dict[int, Dict] = {card["id"]: card for card in SKILL_CARDS}
STAGES_BY_ID: Dict[int, Dict] = {stage["id"]: stage for stage in STAGES}

# Stage plan types and their display names
STAGE_PLAN_DISPLAY = {
    "free": "フリー",
    "sense": "センス",
    "logic": "ロジック",
    "anomaly": "アノマリー"
}

# Stage type display names
STAGE_TYPE_DISPLAY = {
    "contest": "コンテスト",
    "event": "イベント"
}

# Skill card rarity display
SKILL_CARD_RARITY_DISPLAY = {
    "N": "N",
    "R": "R",
    "SR": "SR",
    "SSR": "SSR"
}

# P-Item rarity display
P_ITEM_RARITY_DISPLAY = {
    "R": "R",
    "SR": "SR",
    "SSR": "SSR"
}

# Clear rank display
CLEAR_RANK_DISPLAY = {
    "A+": "A+",
    "S": "S",
    "S+": "S+"
}

def get_idol_by_id(idol_id: int) -> Optional[Dict]:
    """Get idol data by ID."""
    return IDOLS_BY_ID.get(idol_id)

def get_idol_name_by_id(idol_id: int) -> str:
    """Get idol name by ID."""
    idol = IDOLS_BY_ID.get(idol_id)
    return idol["name"] if idol else "Unknown Idol"

def get_p_idol_by_id(p_idol_id: int) -> Optional[Dict]:
    """Get P-Idol data by ID."""
    return P_IDOLS_BY_ID.get(p_idol_id)

def get_p_item_by_id(item_id: int) -> Optional[Dict]:
    """Get P-Item data by ID."""
    return P_ITEMS_BY_ID.get(item_id)

def get_skill_card_by_id(card_id: int) -> Optional[Dict]:
    """Get skill card data by ID."""
    return SKILL_CARDS_BY_ID.get(card_id)

def get_stage_by_id(stage_id: int) -> Optional[Dict]:
    """Get stage data by ID."""
    return STAGES_BY_ID.get(stage_id)

def validate_idol_id(idol_id: int) -> bool:
    """Validate if idol ID exists."""
    return idol_id in IDOLS_BY_ID

def validate_p_idol_id(p_idol_id: int) -> bool:
    """Validate if P-Idol ID exists."""
    return p_idol_id in P_IDOLS_BY_ID

def validate_p_item_id(item_id: int) -> bool:
    """Validate if P-Item ID exists."""
    return item_id in P_ITEMS_BY_ID

def validate_skill_card_id(card_id: int) -> bool:
    """Validate if skill card ID exists."""
    return card_id in SKILL_CARDS_BY_ID

def validate_stage_id(stage_id: int) -> bool:
    """Validate if stage ID exists."""
    return stage_id in STAGES_BY_ID