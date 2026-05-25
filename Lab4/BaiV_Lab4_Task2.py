# task2_decorators.py
import time

# --- Частина 1: Декоратор ---

def execution_logger(func):
    """Декоратор, що логує ім'я функції, її аргументи та час виконання."""

    def wrapper(*args, **kwargs):
        # Фіксація часу початку
        start_time = time.time()

        print(f"[LOG] Виклик функції '{func.__name__}' "
              f"з аргументами: args={args}, kwargs={kwargs}")

        # Виклик оригінальної функції
        result = func(*args, **kwargs)

        # Час завершення
        end_time = time.time()

        print(f"Функція завершила роботу. "
              f"Час виконання: {end_time - start_time:.4f} сек.")

        return result

    return wrapper

@execution_logger
def complex_calculation(x, y, delay=1):
    """Тестова функція для перевірки декоратора"""
    time.sleep(delay)  # Імітація довгої роботи
    return (x ** y) + sum(range(10000))


# --- Частина 2: Замикання (Closure) ---

def make_config_multiplier(base_rate):
    """Функція-фабрика, що демонструє замикання."""

    def multiplier(value):
        return value * base_rate

    return multiplier

def main():
    print("=== Тестування Декоратора ===")

    # Виклик функції з декоратором
    res1 = complex_calculation(2, 10, delay=0.5)
    print(f"Результат обчислення: {res1}\n")
    print("=== Тестування Замикання ===")

    # Створення функцій на основі замикання
    tax_calculator = make_config_multiplier(1.30)
    discount_calculator = make_config_multiplier(0.95)

    # Тестові значення
    value = 1000

    print(f"Початкове значення: {value}")
    print(f"Tax calculation: {tax_calculator(value)}")
    print(f"Discount calculation: {discount_calculator(value)}")


if __name__ == "__main__":
    main()