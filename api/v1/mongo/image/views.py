from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from core.db.mongo_helper import mongo_helper
from core.models import Profile
from core.models.mongo.base import PyObjectId
from .schemas import ImageCreate, ImageInDB, ImageUpdate
from ...profile.dependencies import get_profile_by_id

router = APIRouter(prefix="/image", tags=["Image_mongo"])


async def get_image_collection():
    return mongo_helper.database.images


@router.post("/", response_model=ImageInDB, status_code=status.HTTP_201_CREATED)
async def create_image(
    image_data: ImageCreate,
    images_collection=Depends(get_image_collection),
    profile: Profile = Depends(get_profile_by_id),
):
    user_id = profile.user_id

    existing_image = await images_collection.find_one(
        {"author": user_id, "url": image_data.url}
    )
    if existing_image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image with this url already exists",
        )

    insert_data = image_data.model_dump(by_alias=True)
    insert_data["author"] = user_id
    insert_data["created_at"] = datetime.now()
    insert_data["updated_at"] = datetime.now()

    # Преобразуем модель в dict, чтобы вставить в MongoDB
    # model_dump_json() - для Pydantic v2+
    insert_result = await images_collection.insert_one(
        insert_data,
    )

    image_in_db = ImageInDB(**insert_data)
    image_in_db.id = insert_result.inserted_id

    return image_in_db


@router.get("/own", response_model=List[ImageInDB])
async def get_user_image(
    image_collection=Depends(get_image_collection),
    profile: Profile = Depends(get_profile_by_id),
):
    images = []

    async for image in image_collection.find({"author": profile.user_id}):
        images.append(ImageInDB(**image))

    return images


@router.get("/", response_model=List[ImageInDB])
async def get_all_images(images_collection=Depends(get_image_collection)):
    images = []
    async for image in images_collection.find():
        images.append(ImageInDB(**image))
    return images


@router.get("/{image_id}", response_model=ImageInDB)
async def get_image_by_id(
    image_id: str,
    image_collection=Depends(get_image_collection),
):
    image = await image_collection.find_one({"_id": PyObjectId(image_id)})
    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )
    return ImageInDB(**image)


@router.put("/{image_id}", response_model=ImageInDB)
async def update_image(
    image_id: str,
    image_update_data: ImageUpdate,
    image_collection=Depends(get_image_collection),
):
    update_data = image_update_data.model_dump(exclude_unset=True, by_alias=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data to update"
        )

    update_data["updated_at"] = datetime.now()

    result = await image_collection.update_one(
        {"_id": PyObjectId(image_id)},
        {"$set": update_data},
    )
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )

    updated_image = await image_collection.find_one({"_id": PyObjectId(image_id)})
    return ImageInDB(**updated_image)


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(image_id: str, image_collection=Depends(get_image_collection)):
    result = await image_collection.delete_one({"_id": PyObjectId(image_id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )
    return {"message": "Image deleted successfully"}
