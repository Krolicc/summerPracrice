from elasticsearch import AsyncElasticsearch

from core.config import settings


async def get_elastic_search():
    es = AsyncElasticsearch(
        [f"http://{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}/"]
    )

    return es
