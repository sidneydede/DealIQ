from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.domain.enums import DealSource, DeckStatus, SocialNetwork, Stage


class SocialProfileIn(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    network: SocialNetwork
    value: str = Field(min_length=1, max_length=500)


class SocialProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    network: str
    value: str


class DealBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    name: str = Field(min_length=1, max_length=200)
    sector: str = Field(min_length=1, max_length=100)
    stage: Stage
    country: str = Field(min_length=2, max_length=2)

    founders: str | None = None
    description: str | None = Field(default=None, max_length=280)
    deal_source: DealSource | None = None
    deal_source_other: str | None = Field(default=None, max_length=120)
    website_url: str | None = Field(default=None, max_length=500)
    deck_status: DeckStatus | None = None
    what_i_know: str | None = Field(default=None, max_length=500)

    @field_validator("country")
    @classmethod
    def _upper_country(cls, v: str) -> str:
        return v.upper()


class DealCreate(DealBase):
    socials: list[SocialProfileIn] = Field(default_factory=list)


class DealUpdate(BaseModel):
    """PATCH : tous les champs sont optionnels. Seuls les champs fournis sont modifiés."""

    model_config = ConfigDict(use_enum_values=True)

    name: str | None = Field(default=None, min_length=1, max_length=200)
    sector: str | None = Field(default=None, min_length=1, max_length=100)
    stage: Stage | None = None
    country: str | None = Field(default=None, min_length=2, max_length=2)
    founders: str | None = None
    description: str | None = Field(default=None, max_length=280)
    deal_source: DealSource | None = None
    deal_source_other: str | None = Field(default=None, max_length=120)
    website_url: str | None = Field(default=None, max_length=500)
    deck_status: DeckStatus | None = None
    what_i_know: str | None = Field(default=None, max_length=500)
    socials: list[SocialProfileIn] | None = None

    @field_validator("country")
    @classmethod
    def _upper_country(cls, v: str | None) -> str | None:
        return v.upper() if v else v


class ActivityBannerOut(BaseModel):
    network: str | None = None
    last_activity_at: datetime | None = None
    stale: bool = False


class DealOut(DealBase):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: int
    completeness_score: int
    # Champs calculés (renseignés par la couche service/route)
    score_band: str = ""
    data_zero_mode: bool = False
    data_zero_hint: str | None = None
    activity: ActivityBannerOut | None = None
    created_at: datetime
    updated_at: datetime
    socials: list[SocialProfileOut] = Field(default_factory=list)


class DealListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    sector: str
    stage: str
    country: str
    completeness_score: int
    updated_at: datetime


class DealNoteCreate(BaseModel):
    content: str = Field(min_length=1, max_length=1000)


class DealNoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    created_at: datetime


class ChangeLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    field: str
    old_value: str | None
    new_value: str | None
    changed_at: datetime
