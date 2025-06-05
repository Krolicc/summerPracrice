import json

from fastapi_users.exceptions import InvalidVerifyToken
from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends, Query
from aiokafka import AIOKafkaConsumer
from sqlalchemy.orm import Mapped
from starlette import status


from api.dependecies.backend import get_database_strategy
from core.authentication.user_manager import get_user_manager
from core.models import User

router = APIRouter()

# Это хранилище для активных WebSocket-соединений.
# В реальном приложении это будет более сложная структура для сопоставления с чатами/пользователями.
active_connections: dict[Mapped[int], WebSocket] = {}


async def get_websocket_user(
    websocket: WebSocket,
    token: str = Query(..., alias="Authorization"),
    strategy=Depends(get_database_strategy),
    user_manager=Depends(get_user_manager),
) -> User | None:
    """
    Зависимость для аутентификации пользователя в WebSocket соединении.
    Ожидает JWT токен в Query параметре 'Authorization'.
    """
    try:
        # Пытаемся получить AccessToken из стратегии
        user = await strategy.read_token(token, user_manager)

        if user and user.is_active:
            return user
        else:
            raise InvalidVerifyToken("User is not active or not found.")
    except InvalidVerifyToken as e:
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION, reason=f"Authentication failed: {e}"
        )
        raise
    except Exception as e:
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION, reason=f"Authentication error: {e}"
        )
        raise


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    user: User | None = Depends(get_websocket_user),
):
    if User is None:
        return

    print(user.is_active, user.id)

    await websocket.accept()
    active_connections[user.id] = websocket
    print(f"WebSocket connected for user: {user.id}")

    # Запускаем Kafka Consumer в фоновом режиме для этого пользователя
    # В реальном приложении, потребитель будет читать из топика,
    # куда отправляются сообщения для этого пользователя/чата
    consumer = AIOKafkaConsumer(
        "chat_messages",  # Топик, из которого читаем
        bootstrap_servers="kafka:9092",
        group_id="chat_consumers",  # Группа потребителей. Важно для Kafka.
    )

    await consumer.start()
    print(f"Kafka Consumer started for user {user.id}")

    try:
        async for msg in consumer:
            # Декодируем сообщение из Kafka (это зашифрованный фрагмент)
            # В реальном приложении вы не будете его декодировать,
            # а просто перешлете как есть или с минимальной оберткой.
            # Здесь для примера мы просто передаем JSON как текст.
            received_fragment = json.loads(msg.value.decode("utf-8"))
            print(
                f"Received fragment from Kafka for user {user.id}: {received_fragment}"
            )

            # Если фрагмент предназначен этому пользователю (или чату, в котором он состоит)
            # Для простоты примера, просто отправляем всем подключенным.
            # В реальном приложении будет логика маршрутизации по chat_id/user_id
            if (
                received_fragment.get("chat_id") == "test_chat_id"
            ):  # Пример простой фильтрации
                # Отправляем зашифрованный фрагмент через WebSocket
                await websocket.send_text(json.dumps(received_fragment))

    except WebSocketDisconnect:
        print(f"WebSocket disconnected for user: {user.id}")
    except Exception as e:
        print(f"Error in WebSocket for user {user.id}: {e}")
    finally:
        del active_connections[user.id]
        await consumer.stop()
        print(f"Kafka Consumer stopped for user {user.id}")
