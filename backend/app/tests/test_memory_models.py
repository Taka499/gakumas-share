"""Tests for memory set models and validation rules."""

import pytest
from pydantic import ValidationError

from app.models.memory import (
    MemorySetCreate,
    MemorySetUpdate,
    PItem,
    SkillCard,
    StageType,
    StagePlan,
    ClearRank,
    SkillCardRarity,
    SkillCardType,
)


class TestPItem:
    """Test PItem model."""

    def test_p_item_creation(self):
        """Test basic P-Item creation."""
        p_item = PItem(
            name="テストアイテム",
            rarity="R",
            plan="sense",
            effects="test effect"
        )
        assert p_item.name == "テストアイテム"
        assert p_item.rarity == "R"
        assert p_item.is_guaranteed is False

    def test_p_item_minimal(self):
        """Test P-Item with minimal required fields."""
        p_item = PItem(name="最小アイテム")
        assert p_item.name == "最小アイテム"
        assert p_item.rarity is None
        assert p_item.is_guaranteed is False


class TestSkillCard:
    """Test SkillCard model."""

    def test_skill_card_creation(self):
        """Test basic skill card creation."""
        skill_card = SkillCard(
            name="テストカード",
            rarity=SkillCardRarity.SR,
            type=SkillCardType.ACTIVE,
            plan=StagePlan.SENSE,
            effects="test effect"
        )
        assert skill_card.name == "テストカード"
        assert skill_card.rarity == SkillCardRarity.SR
        assert skill_card.enhancement_level == 1
        assert skill_card.is_guaranteed is False

    def test_skill_card_enhancement_level_validation(self):
        """Test skill card enhancement level validation."""
        # Valid enhancement level
        skill_card = SkillCard(
            name="テストカード",
            rarity=SkillCardRarity.SR,
            type=SkillCardType.ACTIVE,
            plan=StagePlan.SENSE,
            enhancement_level=5
        )
        assert skill_card.enhancement_level == 5

        # Invalid enhancement level (too low)
        with pytest.raises(ValidationError):
            SkillCard(
                name="テストカード",
                rarity=SkillCardRarity.SR,
                type=SkillCardType.ACTIVE,
                plan=StagePlan.SENSE,
                enhancement_level=0
            )

        # Invalid enhancement level (too high)
        with pytest.raises(ValidationError):
            SkillCard(
                name="テストカード",
                rarity=SkillCardRarity.SR,
                type=SkillCardType.ACTIVE,
                plan=StagePlan.SENSE,
                enhancement_level=11
            )


class TestMemorySetCreate:
    """Test MemorySetCreate model and validation rules."""

    def create_valid_skill_card(self):
        """Helper to create a valid skill card."""
        return SkillCard(
            name="テストカード",
            rarity=SkillCardRarity.SR,
            type=SkillCardType.ACTIVE,
            plan=StagePlan.SENSE
        )

    def create_valid_p_item(self):
        """Helper to create a valid P-Item."""
        return PItem(name="テストアイテム")

    def test_memory_set_creation_with_empty_p_items(self):
        """Test that memory set can be created with empty p_items array."""
        memory_set = MemorySetCreate(
            title="テスト編成",
            stage_type=StageType.CONTEST,
            stage_plan=StagePlan.SENSE,
            p_idol_id=1,
            clear_rank=ClearRank.S,
            p_items=[],  # Empty array should be allowed
            skill_cards=[self.create_valid_skill_card()]
        )
        assert len(memory_set.p_items) == 0
        assert len(memory_set.skill_cards) == 1

    def test_memory_set_creation_with_p_items(self):
        """Test that memory set can be created with p_items."""
        memory_set = MemorySetCreate(
            title="テスト編成",
            stage_type=StageType.CONTEST,
            stage_plan=StagePlan.SENSE,
            p_idol_id=1,
            clear_rank=ClearRank.S,
            p_items=[self.create_valid_p_item()],
            skill_cards=[self.create_valid_skill_card()]
        )
        assert len(memory_set.p_items) == 1
        assert len(memory_set.skill_cards) == 1

    def test_memory_set_requires_at_least_one_skill_card(self):
        """Test that at least one skill card is required."""
        with pytest.raises(ValidationError, match="At least one skill card is required"):
            MemorySetCreate(
                title="テスト編成",
                stage_type=StageType.CONTEST,
                stage_plan=StagePlan.SENSE,
                p_idol_id=1,
                clear_rank=ClearRank.S,
                p_items=[],
                skill_cards=[]  # Empty skill cards should fail
            )

    def test_memory_set_multiple_skill_cards(self):
        """Test memory set with multiple skill cards."""
        memory_set = MemorySetCreate(
            title="テスト編成",
            stage_type=StageType.CONTEST,
            stage_plan=StagePlan.SENSE,
            p_idol_id=1,
            clear_rank=ClearRank.S,
            p_items=[],
            skill_cards=[
                self.create_valid_skill_card(),
                self.create_valid_skill_card()
            ]
        )
        assert len(memory_set.skill_cards) == 2

    def test_memory_set_title_validation(self):
        """Test title validation."""
        # Valid title
        memory_set = MemorySetCreate(
            title="有効なタイトル",
            stage_type=StageType.CONTEST,
            stage_plan=StagePlan.SENSE,
            p_idol_id=1,
            clear_rank=ClearRank.S,
            skill_cards=[self.create_valid_skill_card()]
        )
        assert memory_set.title == "有効なタイトル"

        # Empty title should fail
        with pytest.raises(ValidationError):
            MemorySetCreate(
                title="",
                stage_type=StageType.CONTEST,
                stage_plan=StagePlan.SENSE,
                p_idol_id=1,
                clear_rank=ClearRank.S,
                skill_cards=[self.create_valid_skill_card()]
            )

    def test_memory_set_notes_validation(self):
        """Test notes field validation."""
        # Valid notes
        memory_set = MemorySetCreate(
            title="テスト編成",
            stage_type=StageType.CONTEST,
            stage_plan=StagePlan.SENSE,
            p_idol_id=1,
            clear_rank=ClearRank.S,
            skill_cards=[self.create_valid_skill_card()],
            notes="テストメモ"
        )
        assert memory_set.notes == "テストメモ"

        # Default empty notes
        memory_set = MemorySetCreate(
            title="テスト編成",
            stage_type=StageType.CONTEST,
            stage_plan=StagePlan.SENSE,
            p_idol_id=1,
            clear_rank=ClearRank.S,
            skill_cards=[self.create_valid_skill_card()]
        )
        assert memory_set.notes == ""


class TestMemorySetUpdate:
    """Test MemorySetUpdate model and validation rules."""

    def create_valid_skill_card(self):
        """Helper to create a valid skill card."""
        return SkillCard(
            name="テストカード",
            rarity=SkillCardRarity.SR,
            type=SkillCardType.ACTIVE,
            plan=StagePlan.SENSE
        )

    def test_memory_set_update_empty_skill_cards_validation(self):
        """Test that updating with empty skill cards fails."""
        with pytest.raises(ValidationError, match="At least one skill card is required"):
            MemorySetUpdate(skill_cards=[])

    def test_memory_set_update_valid_skill_cards(self):
        """Test that updating with valid skill cards works."""
        memory_set_update = MemorySetUpdate(
            skill_cards=[self.create_valid_skill_card()]
        )
        assert len(memory_set_update.skill_cards) == 1

    def test_memory_set_update_none_skill_cards(self):
        """Test that skill_cards can be None in updates."""
        memory_set_update = MemorySetUpdate(
            title="更新されたタイトル"
        )
        assert memory_set_update.skill_cards is None
        assert memory_set_update.title == "更新されたタイトル"