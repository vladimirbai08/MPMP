import asyncio
import random
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%H:%M:%S')

class FlightTelemetrySystem:
    def __init__(self, max_alt=500):
        self.data_queue = asyncio.Queue(maxsize=5)
        self.emergency_event = asyncio.Event()
        self.max_altitude = max_alt

    async def altimeter_sensor(self):
        """Продюсер: імітація датчика висоти."""
        try:
            while not self.emergency_event.is_set():
                altitude = random.randint(100, 600)
                logging.info(f"[Sensor] Зчитано висоту: {altitude} м")
                
                # Додавання в чергу з очікуванням, якщо вона повна
                await self.data_queue.put(altitude)
                await asyncio.sleep(0.8)
        except asyncio.CancelledError:
            logging.info("[Sensor] Роботу датчика припинено.")

    async def flight_controller(self):
        """Споживач: аналіз даних та контроль безпеки."""
        try:
            while not self.emergency_event.is_set():
                alt = await self.data_queue.get()
                
                if alt > self.max_altitude:
                    logging.warning(f"[Controller] ПЕРЕВИЩЕННЯ: {alt}м > {self.max_altitude}м!")
                    self.emergency_event.set()
                else:
                    logging.info(f"[Controller] Висота в нормі: {alt}м")
                
                self.data_queue.task_done()
                await asyncio.sleep(0.2)
        except asyncio.CancelledError:
            logging.info("[Controller] Контролер зупинено.")

    async def emergency_system(self):
        """Монітор подій: чекає на сигнал аварії."""
        await self.emergency_event.wait()
        logging.critical("[Emergency] ПРОТОКОЛ АВАРІЙНОЇ ПОСАДКИ АКТИВОВАНО!")

async def main():
    uav = FlightTelemetrySystem()
    logging.info("--- Старт бортових систем ---")

    # Створення тасків
    tasks = [
        asyncio.create_task(uav.altimeter_sensor()),
        asyncio.create_task(uav.flight_controller()),
        asyncio.create_task(uav.emergency_system())
    ]

    # Чекаємо на активацію події
    event_wait_task = asyncio.create_task(uav.emergency_event.wait())
    
    # Використовуємо FIRST_COMPLETED для реакції на подію
    await asyncio.wait([event_wait_task], return_when=asyncio.FIRST_COMPLETED)

    # Graceful shutdown
    logging.info("Main: Зупинка всіх процесів...")
    for t in tasks:
        t.cancel()
    
    await asyncio.gather(*tasks, return_exceptions=True)
    logging.info("--- Системи вимкнено. БПЛА на землі. ---")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass