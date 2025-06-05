from sqlalchemy import Table, Column, Integer, ForeignKey

from core.models import Base

character_chapter = Table(
    "character_chapter",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("character_id", ForeignKey("character.id"), nullable=False),
    Column("chapter_id", ForeignKey("chapter.id"), nullable=False),
)
