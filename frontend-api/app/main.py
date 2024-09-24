from fastapi import FastAPI
import routers, database, consumer
import threading

app = FastAPI()

database.init_db()

app.include_router(routers.router)

# Start RabbitMQ consumer in a separate thread
def start_rabbitmq_consumer():
    consumer.start_consumer()

threading.Thread(target=start_rabbitmq_consumer, daemon=True).start()

