import asyncio
import random
import logging

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)


class SmartParkingSystem:
    def __init__(self, max_places=50):
        # Черга з обмеженим розміром (backpressure)
        self.data_queue = asyncio.Queue(maxsize=5)

        # Подія критичної ситуації
        self.full_parking_event = asyncio.Event()

        # Загальна кількість місць
        self.max_places = max_places

    async def parking_sensor(self):
        """
        Producer: генерує кількість зайнятих місць.
        """
        try:
            occupied_places = 0

            while not self.full_parking_event.is_set():
                # Імітуємо прибуття/виїзд автомобілів
                change = random.randint(-3, 5)
                occupied_places += change

                # Не допускаємо виходу за межі
                occupied_places = max(0, min(occupied_places, self.max_places))

                logging.info(
                    f"[Sensor] Зайнято місць: "
                    f"{occupied_places}/{self.max_places}"
                )

                # Якщо черга повна - producer чекатиме
                await self.data_queue.put(occupied_places)

                await asyncio.sleep(1)

        except asyncio.CancelledError:
            logging.info("[Sensor] Роботу датчика завершено.")

    async def parking_controller(self):
        """
        Consumer: обчислює відсоток заповненості.
        """
        try:
            while not self.full_parking_event.is_set():
                occupied = await self.data_queue.get()

                occupancy_percent = (
                    occupied / self.max_places * 100
                )

                logging.info(
                    f"[Controller] Заповненість: "
                    f"{occupancy_percent:.1f}%"
                )

                # Критична подія
                if occupied == self.max_places:
                    logging.warning(
                        "[Controller] ПАРКІНГ ПОВНІСТЮ ЗАПОВНЕНИЙ!"
                    )
                    self.full_parking_event.set()

                self.data_queue.task_done()

                await asyncio.sleep(0.3)

        except asyncio.CancelledError:
            logging.info("[Controller] Контролер зупинено.")

    async def parking_monitor(self):
        """
        Monitor: очікує на критичну подію.
        """
        await self.full_parking_event.wait()

        logging.critical(
            "[Monitor] УВАГА! Вільних місць більше немає!"
        )


async def main():
    parking = SmartParkingSystem(max_places=50)

    logging.info("--- Запуск системи розумного паркінгу ---")

    tasks = [
        asyncio.create_task(parking.parking_sensor()),
        asyncio.create_task(parking.parking_controller()),
        asyncio.create_task(parking.parking_monitor())
    ]

    # Очікуємо спрацювання події
    event_task = asyncio.create_task(
        parking.full_parking_event.wait()
    )

    await asyncio.wait(
        [event_task],
        return_when=asyncio.FIRST_COMPLETED
    )

    # Graceful shutdown
    logging.info("Main: Завершення роботи системи...")

    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)

    logging.info(
        "--- Систему розумного паркінгу вимкнено ---"
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Програму завершено користувачем.")