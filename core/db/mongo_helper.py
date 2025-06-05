import asyncio

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure, OperationFailure

from core.config import settings


class MongoHelper:
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.database: AsyncIOMotorDatabase = None

    async def connect(
        self,
        max_attempts: int = 10,
        delay: float = 2,
    ):
        print("Try connect to Mongo")
        for attempt in range(1, max_attempts + 1):
            try:
                self.client = AsyncIOMotorClient(settings.MONGO_DB_URL)

                await self.client.admin.command("ping")
                self.database = self.client[settings.MONGO_DB_NAME]

                # print(f"Connected to MongoDB successfully after {attempt} attempt(s)!")
            except (ConnectionFailure, OperationFailure) as e:
                # print(f"Attempt {attempt} failed to connect to MongoDB: {e}")
                if attempt < max_attempts:
                    # print(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                else:
                    # print(
                    #     f"Failed to connect to MongoDB after {max_attempts} attempts."
                    # )
                    raise
            except Exception as e:
                # print(f"An unexpected error occurred during MongoDB connection: {e}")
                raise

    async def dispose(self):
        if self.client:
            self.client.close()

            print("MongoDB connection closed.")


mongo_helper = MongoHelper()
