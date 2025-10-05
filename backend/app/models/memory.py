"""Pydantic models for memory set entities."""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class StageType(str, Enum):
    """Supported stage types based on gakumas-tools data."""

    CONTEST = "contest"
    EVENT = "event"


class StagePlan(str, Enum):
    """Supported stage plans based on gakumas-tools data."""

    FREE = "free"
    SENSE = "sense"
    LOGIC = "logic"
    ANOMALY = "anomaly"


class ClearRank(str, Enum):
    """Supported clear ranks."""

    A_PLUS = "A+"
    S = "S"
    S_PLUS = "S+"


class SkillCardRarity(str, Enum):
    """Skill card rarities based on gakumas-tools data."""

    N = "N"
    R = "R"
    SR = "SR"
    SSR = "SSR"


class SkillCardType(str, Enum):
    """Skill card types based on gakumas-tools data."""

    ACTIVE = "active"
    MENTAL = "mental"
    TROUBLE = "trouble"


class PItemRarity(str, Enum):
    """P-Item rarities based on gakumas-tools data."""

    R = "R"
    SR = "SR"
    SSR = "SSR"


class PItemMode(str, Enum):
    """P-Item modes based on gakumas-tools data."""

    PRODUCE = "produce"
    STAGE = "stage"


class PItemSourceType(str, Enum):
    """P-Item source types based on gakumas-tools data."""

    SUPPORT = "support"
    PRODUCE = "produce"
    P_IDOL = "pIdol"


class PItem(BaseModel):
    """P-Item model for memory sets."""

    name: str = Field(..., description="P-Item name")
    rarity: Optional[PItemRarity] = Field(None, description="P-Item rarity")
    plan: Optional[StagePlan] = Field(None, description="P-Item plan type")
    mode: Optional[PItemMode] = Field(None, description="P-Item mode")
    source_type: Optional[PItemSourceType] = Field(
        None, description="P-Item source type"
    )
    effects: Optional[str] = Field(
        None, description="P-Item effects description"
    )
    is_guaranteed: bool = Field(
        default=False, description="Whether this P-Item is guaranteed"
    )


class SkillCard(BaseModel):
    """Skill card model for memory sets."""

    name: str = Field(..., description="Skill card name")
    rarity: SkillCardRarity = Field(..., description="Skill card rarity")
    type: SkillCardType = Field(..., description="Skill card type")
    plan: StagePlan = Field(..., description="Skill card plan")
    effects: Optional[str] = Field(None, description="Skill card effects")
    cost: Optional[str] = Field(None, description="Skill card cost")
    enhancement_level: int = Field(default=1, ge=1, le=10, description="Enhancement level (1-10)")
    is_guaranteed: bool = Field(default=False, description="Whether this skill card is guaranteed")


class MemorySetCreate(BaseModel):
    """Input payload when creating a memory set."""

    title: str = Field(..., min_length=1, max_length=100, description="Memory set title")
    stage_type: StageType = Field(..., description="Stage type (contest/event)")
    stage_plan: StagePlan = Field(..., description="Stage plan (free/sense/logic/anomaly)")
    p_idol_id: int = Field(..., description="P-Idol ID from gakumas-tools data")
    clear_rank: ClearRank = Field(..., description="Clear rank achieved")
    p_items: List[PItem] = Field(default=[], description="P-Items used (can be empty)")
    skill_cards: List[SkillCard] = Field(..., description="Skill cards used (minimum 1 required)")
    notes: Optional[str] = Field(default="", max_length=1000, description="Additional notes")

    @field_validator('skill_cards')
    @classmethod
    def validate_skill_cards_not_empty(cls, v):
        """Ensure at least one skill card is provided."""
        if not v or len(v) == 0:
            raise ValueError("At least one skill card is required")
        return v


class MemorySetUpdate(BaseModel):
    """Input payload when updating a memory set."""

    title: Optional[str] = Field(None, min_length=1, max_length=100, description="Memory set title")
    stage_type: Optional[StageType] = Field(None, description="Stage type (contest/event)")
    stage_plan: Optional[StagePlan] = Field(None, description="Stage plan (free/sense/logic/anomaly)")
    p_idol_id: Optional[int] = Field(None, description="P-Idol ID from gakumas-tools data")
    clear_rank: Optional[ClearRank] = Field(None, description="Clear rank achieved")
    p_items: Optional[List[PItem]] = Field(None, description="P-Items used (can be empty)")
    skill_cards: Optional[List[SkillCard]] = Field(None, description="Skill cards used (minimum 1 required)")
    notes: Optional[str] = Field(None, max_length=1000, description="Additional notes")

    @field_validator('skill_cards')
    @classmethod
    def validate_skill_cards_not_empty(cls, v):
        """Ensure at least one skill card is provided when updating skill cards."""
        if v is not None and len(v) == 0:
            raise ValueError("At least one skill card is required")
        return v


class MemorySetInDB(BaseModel):
    """Representation of a memory set stored in MongoDB."""

    id: str
    user_id: str
    title: str
    stage_type: StageType
    stage_plan: StagePlan
    p_idol_id: int
    clear_rank: ClearRank
    p_items: List[PItem]
    skill_cards: List[SkillCard]
    notes: str
    created_at: datetime
    updated_at: datetime


class MemorySetPublic(BaseModel):
    """Public-facing memory set information returned to clients."""

    id: str
    user_id: str
    title: str
    stage_type: StageType
    stage_plan: StagePlan
    p_idol_id: int
    clear_rank: ClearRank
    p_items: List[PItem]
    skill_cards: List[SkillCard]
    notes: str
    created_at: datetime
    updated_at: datetime


class MemorySetListResponse(BaseModel):
    """Response model for paginated memory set lists."""

    items: List[MemorySetPublic] = Field(..., description="List of memory sets")
    total: int = Field(..., description="Total count of items matching the query")
    skip: int = Field(..., description="Number of items skipped")
    limit: int = Field(..., description="Maximum number of items returned")


class IdolInfo(BaseModel):
    """Idol information for reference."""

    id: int
    name: str


class PIdolInfo(BaseModel):
    """P-Idol information for reference."""

    id: int
    idol_id: int
    title: str
    rarity: SkillCardRarity
    plan: StagePlan
    recommended_effect: Optional[str] = None


class StageInfo(BaseModel):
    """Stage information for reference."""

    id: int
    name: str
    plan: StagePlan
    type: StageType