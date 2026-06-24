import asyncio
import random
import logging
from datetime import datetime
from collections import deque

# Налаштування логування для наочності
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)

class AsyncMonitor:
    def __init__(self, threshold=85.0, window_size=5):
        self.queue = asyncio.Queue(maxsize=10)
        self.critical_event = asyncio.Event()
        self.threshold = threshold
        self.window_size = window_size
        self.history = deque(maxlen=window_size)

    async def producer(self):
        """Емулятор джерела даних: генерує показники температури."""
        try:
            while not self.critical_event.is_set():
                # Генерація випадкового значення (імітація датчика)
                temp = round(random.uniform(40.0, 95.0), 2)
                
                try:
                    # Non-blocking put: чекає, якщо черга повна
                    await asyncio.wait_for(self.queue.put(temp), timeout=1.0)
                    logging.info(f"Producer: Відправлено значення {temp}°C")
                except asyncio.TimeoutError:
                    logging.warning("Producer: Черга переповнена, дані втрачено")

                # Випадкова затримка між вимірюваннями
                await asyncio.sleep(random.uniform(0.5, 1.5))
        except asyncio.CancelledError:
            logging.info("Producer: Зупинка генерації даних")

    async def consumer(self):
        """Обробник: розрахунок ковзного середнього."""
        try:
            while not self.critical_event.is_set():
                # Отримання даних з черги
                temp = await self.queue.get()
                self.history.append(temp)
                
                if len(self.history) == self.window_size:
                    avg_temp = sum(self.history) / self.window_size
                    logging.info(f"Consumer: Середня температура за останні {self.window_size} кроків: {avg_temp:.2f}°C")
                    
                    # Перевірка умови для активації Event
                    if avg_temp > self.threshold:
                        logging.error(f"Watcher: КРИТИЧНИЙ ПОРІГ ПЕРЕВИЩЕНО (> {self.threshold}°C)!")
                        self.critical_event.set()
                
                self.queue.task_done()
                await asyncio.sleep(0.1) # Імітація часу обробки
        except asyncio.CancelledError:
            logging.info("Consumer: Завершення обробки даних")

    async def watchdog(self):
        """Монітор: чекає на активацію події для екстреної зупинки системи."""
        await self.critical_event.wait()
        logging.critical("Watchdog: Отримано сигнал тривоги! Ініціалізація зупинки системи...")

async def main():
    # Параметри: поріг 85 градусів, вікно аналізу - 5 значень
    monitor = AsyncMonitor(threshold=85.0, window_size=5)

    logging.info("Система моніторингу запущена. Очікування даних...")

    # Створення та запуск тасків
    tasks = [
        asyncio.create_task(monitor.producer()),
        asyncio.create_task(monitor.consumer()),
        asyncio.create_task(monitor.watchdog())
    ]

    # Чекаємо, поки активується подія або таски завершаться
    # Спочатку створюємо таск
    event_wait_task = asyncio.create_task(monitor.critical_event.wait())

    # Тепер передаємо його у wait
    done, pending = await asyncio.wait(
        [event_wait_task], 
        return_when=asyncio.FIRST_COMPLETED
    )

    # Graceful shutdown: скасовуємо всі запущені таски
    logging.info("Main: Завершення роботи всіх компонентів...")
    for task in tasks:
        task.cancel()
    
    # Чекаємо остаточного завершення тасків
    await asyncio.gather(*tasks, return_exceptions=True)
    logging.info("Main: Програму успішно зупинено.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass