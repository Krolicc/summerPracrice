from sqlalchemy import Table, Column, Integer, ForeignKey

from core.models import Base

image_filter = Table(
    "image_filter",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("image_id", ForeignKey("image.id"), nullable=False),
    Column("filter_id", ForeignKey("filter.id"), nullable=False),
)
