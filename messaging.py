import os

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
EXCHANGE = "music.events"
TRACK_CREATED = "track.created"
NOTIFICATIONS_QUEUE = "notifications.track_created"