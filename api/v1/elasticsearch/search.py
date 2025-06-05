import hashlib
import json
from typing import List, cast

from elasticsearch.dsl import Q, AsyncSearch
from fastapi import APIRouter, Depends, Query, HTTPException, Body
from redis.asyncio import Redis

from api.v1.mongo.image.schemas import ImageInDB
from core.config import settings
from core.elasticsearch.get_elastic_search import get_elastic_search
from core.redis.get_redis import get_redis

router = APIRouter(prefix="/search", tags=["Search"])


@router.post("/", response_model=List[ImageInDB])
async def search_by_tags_and_query(
    query: str = Body(""),
    tags: List[str] = Body([]),
    size: int = 10,
    es=Depends(get_elastic_search),
    redis: Redis = Depends(get_redis),
) -> List[ImageInDB]:
    cache_key = f"search:{query}:{':'.join(sorted(tags))}:{size}"
    cache_key = f"search:{hashlib.md5(cache_key.encode()).hexdigest()}"

    cached_data = await redis.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    s: AsyncSearch = AsyncSearch(using=es, index=settings.ELASTIC_INDEX)

    queries = []

    if len(tags) > 0:
        queries.append(Q("terms", extra__tags=tags))

    if len(query) > 0:
        queries.append(
            Q(
                "multi_match",
                query=query,
                fields=[
                    "name^3",
                    "main.description^2",
                    "extra.tags",
                ],
            )
        )

    if queries:
        s.query = Q("bool", must=queries)

    s = cast(AsyncSearch, s.sort("_score")[:size])

    try:
        response = await s.execute()

        results = [hit.to_dict() for hit in response.hits]

        await redis.zincrby("popular_searches", 1, cache_key)

        popular = await redis.zrevrange("popular_searches", 0, 100)
        if cache_key in popular:
            await redis.setex(cache_key, 20, json.dumps(results))

        return response.hits

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Elasticsearch error: {str(e)}")
