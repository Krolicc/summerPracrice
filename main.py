import asyncio
from contextlib import asynccontextmanager

import uvicorn
from aiokafka.errors import KafkaConnectionError

# from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

# from pymongo.errors import ConnectionFailure, OperationFailure
from starlette.middleware.cors import CORSMiddleware

# from api.v1.user.actions.create_superuser import create_superuser
from core.config import settings

# from core.db.mongo_helper import mongo_helper
# from core.elasticsearch.syncronized_data import run_data_periodically
from core.kafka.kafka_helper import kafka_helper
from core.models.db_helper import db_helper

from api.v1 import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startapp

    # await create_superuser()

    # try:
    #     await mongo_helper.connect(max_attempts=15, delay=3)
    # except (ConnectionFailure, OperationFailure, Exception) as e:
    #     print(
    #         f"FATAL: Could not connect to MongoDB. Application will not start. Error: {e}"
    #     )
    #     raise RuntimeError("Failed to connect to MongoDB, exiting.") from e

    # task = asyncio.create_task(run_data_periodically())

    for i in range(10):
        try:
            await kafka_helper.connect()
            print("Kafka Producer started successfully!")
            break
        except KafkaConnectionError as e:
            print(
                f"Attempt {i + 1}/10: Unable to connect to Kafka. Retrying in 5 seconds... Error: {e}"
            )
            await asyncio.sleep(5)
    else:
        print(f"Failed to connect to Kafka after 10 retries. Application will exit.")
        exit(1)

    yield
    # shutdown

    await kafka_helper.disconnect()
    # task.cancel()
    # try:
    #     await task
    # except asyncio.CancelledError:
    #     print("Фоновая синхронизация остановлена")

    await db_helper.dispose()
    # await mongo_helper.dispose()


application = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

application.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

application.include_router(
    router=api_router,
    prefix="/api",
)

if __name__ == "__main__":
    uvicorn.run("main:application", reload=True)
