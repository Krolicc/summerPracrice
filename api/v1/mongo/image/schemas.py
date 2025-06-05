from datetime import datetime
from typing import Optional, List, Union, Annotated
from core.models.mongo.base import BaseMongoModel, PyObjectId
from pydantic import BaseModel, Field


class ImageExtraData(BaseModel):
    """
    Дополнительные данные для изображения.
    """

    licence: Optional[str] = Field(
        None, description="Лицензия изображения (например, Creative Commons)"
    )
    tags: Optional[List[str]] = Field(
        None, description="Список тегов, описывающих изображение"
    )

    # model_config = {'extra': 'allow'} # Для Pydantic v2+


class ImageMainData(BaseModel):
    """
    Основные метаданные изображения.
    """

    description: Optional[str] = Field(
        None, description="Подробное описание изображения"
    )


class ImageBase(BaseMongoModel):
    url: Union[str, None] = Field(
        ...,
        description="URL изображения или ссылка на файловое хранилище. Может быть null, если изображение еще не загружено, но метаданные существуют.",
    )
    name: Union[str, None] = Field(
        None, description="Имя файла изображения. Может быть null, если не указано."
    )
    hide_author: bool = Field(
        False, description="Флаг, указывающий, нужно ли скрывать автора"
    )
    AI: Optional[bool] = Field(
        None, description="Флаг, указывающий, сгенерировано ли изображение ИИ"
    )
    width: int = Field(..., description="Ширина изображения в пикселях")
    height: int = Field(..., description="Высота изображения в пикселях")

    main: ImageMainData = Field(
        default_factory=ImageMainData, description="Основные метаданные изображения"
    )
    extra: ImageExtraData = Field(
        default_factory=ImageExtraData, description="Дополнительные данные изображения"
    )


class ImageCreate(ImageBase):
    pass


class ImageInDB(ImageBase):
    id: Annotated[PyObjectId, Field(alias="_id")] = Field(default_factory=PyObjectId)
    author: int = Field(..., description="ID автора изображения")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Дата и время создания записи"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        description="Дата и время последнего обновления записи",
    )


class ImageUpdate(ImageBase):
    name: Optional[Union[str, None]] = Field(None, description="Имя файла изображения")
    hide_author: Optional[bool] = Field(None, description="Скрывать автора")
    AI: Optional[bool] = Field(None, description="Сгенерировано ИИ")
    width: Optional[int] = Field(None, description="Ширина изображения")
    height: Optional[int] = Field(None, description="Высота изображения")

    # Если вы хотите обновлять отдельные поля внутри 'main' или 'extra',
    # вам нужно будет либо определить отдельные update-модели для них, либо управлять этим вручную в логике API.
    main: Optional[ImageMainData] = Field(
        None, description="Основные метаданные для обновления"
    )
    extra: Optional[ImageExtraData] = Field(
        None, description="Дополнительные данные для обновления"
    )
