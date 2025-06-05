import json

from fastapi import APIRouter, HTTPException, Depends

from api.v1.user.fastapi_users import current_active_user
from core.kafka.kafka_helper import kafka_helper

router = APIRouter(tags=["Kafka"])


@router.post("/send_fragment/")
async def send_message_fragment(
    chat_id: str,
    fragment_data: dict,
    user=Depends(current_active_user),
    producer=Depends(kafka_helper.get_kafka_producer),
):
    print("1")

    # В реальном приложении fragment_data будет уже зашифрованным фрагментом от клиента
    # и содержать все необходимые поля (encrypted_payload, hmac, etc.)
    # Здесь мы просто отправляем dict в Kafka
    try:

        value_bytes = json.dumps(fragment_data).encode("utf-8")

        print("2")

        # Отправляем в топик 'chat_messages' с chat_id в качестве ключа
        key_bytes = chat_id.encode("utf-8")
        print("Отправил данные")
        await producer.send_and_wait("chat_messages", value=value_bytes, key=key_bytes)
        print(f"Sent fragment to chat {chat_id}: {fragment_data}")
        return {"status": "fragment sent", "chat_id": chat_id}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to send message fragment: {e}"
        )
