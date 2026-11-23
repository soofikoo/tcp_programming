import aio_pika

from api.schemas.notification import TrackCreatedEvent
from messaging import RABBITMQ_URL, EXCHANGE, NOTIFICATIONS_QUEUE, TRACK_CREATED

async def consume(on_event):
    conn = await aio_pika.connect_robust(RABBITMQ_URL)
    ch = await conn.channel()
    exchange = await ch.declare_exchange(EXCHANGE, aio_pika.ExchangeType.TOPIC, durable=True)
    queue = await ch.declare_queue(NOTIFICATIONS_QUEUE, durable=True)
    await queue.bind(exchange, routing_key=TRACK_CREATED)
    print(f"[NS] слушаю очередь {NOTIFICATIONS_QUEUE}")

    async with queue.iterator() as messages:
        async for message in messages:
            async with message.process():          # ack, если блок прошёл без исключения
                event = TrackCreatedEvent.model_validate_json(message.body)
                print(f"[NS] ← {event.event}: track_id={event.track_id}, получателей {len(event.subscriber_ids)}")
                await on_event(event)

if __name__ == "__main__":
    import asyncio
    async def just_print(event): pass
    asyncio.run(consume(just_print))
