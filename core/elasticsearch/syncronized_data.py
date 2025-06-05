import asyncio

from elasticsearch import AsyncElasticsearch
from typing import Dict, List

from fastapi.params import Depends

from api.v1.mongo.image.views import get_image_collection
from core.config import settings
from core.elasticsearch.get_elastic_search import get_elastic_search


async def run_data_periodically(
    batch_size: int = 1000,
    interval: int = 20,
    # es: AsyncElasticsearch = Depends(get_elastic_search),
):
    """Запускает sync_data каждые `interval` секунд."""

    # print("Начало синхронизации.")
    es: AsyncElasticsearch = await get_elastic_search()
    image_collection = await get_image_collection()

    while True:
        try:
            await sync_data(es, image_collection, batch_size)
            # print("Данные успешно синхронизированы!")
        except Exception as e:
            print(f"Ошибка синхронизации: {e}")

        await asyncio.sleep(interval)


async def sync_data(
    es: AsyncElasticsearch,
    image_collection,
    batch_size: int,
) -> None:
    """Переносит данные из MongoDB в Elasticsearch."""

    if not await es.indices.exists(index=settings.ELASTIC_INDEX):
        await es.indices.create(index=settings.ELASTIC_INDEX)

    documents = []

    async for doc in image_collection.find({}):
        doc["_id"] = str(doc["_id"])
        documents.append(doc)

        print(len(documents), batch_size)

        if len(documents) >= batch_size:
            await bulk_index(documents, es)
            documents = []

    if documents:
        await bulk_index(documents, es)


async def bulk_index(documents: List[Dict], es: AsyncElasticsearch) -> None:
    """Массово добавляет документы в Elasticsearch."""
    from datetime import datetime

    bulk_actions = []

    for doc in documents:
        doc_body = doc.copy()
        doc_id = str(doc_body.pop("_id"))

        for meta_field in ["_index", "_type", "_version"]:
            doc_body.pop(meta_field, None)

        for field in ["created_at", "updated_at"]:
            if field in doc and isinstance(doc[field], datetime):
                doc[field] = doc[field].isoformat()

        bulk_actions.append(
            {
                "index": {
                    "_index": settings.ELASTIC_INDEX,
                    "_id": doc_id,
                }
            }
        )
        bulk_actions.append(doc_body)

    # print("Bulk actions sample:", bulk_actions[:2])

    try:
        response = await es.bulk(operations=bulk_actions)

        if response["errors"]:
            print("Некоторые документы не были индексированы:")
            for item in response["items"]:
                if "error" in item["index"]:
                    print(
                        f"Ошибка для ID {item['index']['_id']}: {item['index']['error']}"
                    )
        else:
            # print(
            #     f"Bulk response summary: {response['took']}ms, {len(response['items'])} items"
            # )
            # print("Sample item response:", response["items"][0])  # Первый результат
            count = await es.count(index=settings.ELASTIC_INDEX)
            # print(f"Всего документов в индексе: {count['count']}")

    except Exception as e:
        print(f"Ошибка при выполнении bulk-запроса: {e}")
        raise
