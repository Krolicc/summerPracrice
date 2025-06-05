from sqlalchemy import Table, Column, Integer, ForeignKey

from core.models import Base

character_chronology = Table(
    "character_chronology",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("character_id", ForeignKey("character.id"), nullable=False),
    Column("chronology_id", ForeignKey("chronology.id"), nullable=False),
)
