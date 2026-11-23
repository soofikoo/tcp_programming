import logging
import pika
from messaging import RABBITMQ_URL, EXCHANGE

log = logging.getLogger(__name__)

def publish_event(routing_key: str, body: str) -> None:
    try:
        conn = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
        try:
            ch = conn.channel()
            ch.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)
            ch.basic_publish(
                exchange=EXCHANGE,
                routing_key=routing_key,
                body=body.encode(),
                properties=pika.BasicProperties(
                    content_type="application/json",
                    delivery_mode=pika.DeliveryMode.Persistent,
                ),
            )
            print(f"[API] -> RabbitMQ {routing_key}: {body}")
        finally:
            conn.close()
    except pika.exceptions.AMQPError as e:
        log.error("Не удалось опубликовать событие %s: %s", routing_key, e)
