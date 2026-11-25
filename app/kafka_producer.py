
import json
import logging
from aiokafka import AIOKafkaProducer
from app.core.config import settings



logger = logging.getLogger("uvicorn.error")


producer: AIOKafkaProducer | None = None


async def start_producer():
    
    global producer

    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BROKERS
    )
    await producer.start()

    logger.info("Kafka Producer успешно запущен")



async def stop_producer():

    global producer
    if producer:
        await producer.stop()
        logger.info("Kafka Producer остановлен")



async def send_event(topic:str, payload:dict):

    if not producer:
        logger.error("kafka producer не инициализирован!")
        return
    

    try:
        value = json.dumps(payload).encode("utf-8")
        await producer.send_and_wait(topic=topic, value=value)

        logger.info(f"Событие отправлено в топик {topic}: {payload}")

    except Exception as e:
        logger.error(f"Ошибка отправки события в Kafka: {e}")
