# Бай Володимир, ІКМ-224а, лабораторна робота №2, Варіант 1
# main.py
# Основна програма для обробки показників системи "Розумний офіс"

import sensors as sm # підключення пакету sensors

### TODO: основну програму можна написати однією функцією main(), або окремі задачі розділити на окремі підпрограми, наприклад наступним чином:

def parse_input(input_str):
    """Перетворює введений рядок на список дійсних чисел (з перевіркою)."""
    ### TODO: обробляє введені користувачем числові дані показників; дані передаються єдиним рядком, розділяються, перевіряються та перетворюються на дійсні числа;
    ### програма повертає список числових значень, якщо значення перетворити неможливо - видається повідомлення 
    try:
        return [float(x) for x in input_str.split()]
    except ValueError:
        print("Помилка: введіть лише числа!")
        return []

def create_data_dict(lum_list, temp_list, cons_list):
    """Формує словник даних з мітками часу."""
    ### TODO: на основі списків з показниками температури, вологості та тиску повітря формується словник зі словників (структура приведена у завданні),
    ### мітки часу задаються без конкретних значень (наприклад, Т1, Т2, ..); програма повертає створений словник
    def create_subdict(values):
        return {f"T{i+1}": values[i] for i in range(len(values))}

    return {
        "luminosity": create_subdict(lum_list),
        "temperature": create_subdict(temp_list),
        "consumption": create_subdict(cons_list)
    }

def process_measurements(title, data_dict, threshold):
    """Виводить таблицю та статистику для заданого виду даних."""
    ### TODO: програма викликає функції з підключеного модуля та обчислює основні статистичні параметри для переданого у аргументах показника (функція може бути універсальною: застосовуватись для температури, вологості та тиску повітря), також виконується пошук різких перепадів і виводиться інформація про них, якщо такі були знайдені; в параметрах передаються назва показника, словник з його значеннями, порогове значення для визначення різких перепадів; програма нічого не повертає, але друкує на екран повідомлення про обчислені значення характеристик
    sm.show_table(data_dict, title)

    print(f"\nСереднє: {sm.get_average(data_dict):.2f}")
    print(f"Мінімум: {sm.get_min(data_dict)}")
    print(f"Максимум: {sm.get_max(data_dict)}")
    print(f"Медіана: {sm.get_median(data_dict)}")

    jumps = sm.find_jumps(data_dict, threshold)

    if jumps:
        print("Різкі перепади:")
        for j in jumps:
            print(" ", j)
    else:
        print("Різкі перепади: не виявлено")

def main():
    print("=== Обробка показів системи 'Розумний офіс' ===")

    ### TODO: 1) запит у користувача значень для температури, волгості та тиску повітря
    lum_str = input("Введіть освітленість (лк): ")
    temp_str = input("Введіть температуру (°C): ")
    cons_str = input("Введіть споживання (Вт): ")

    ### TODO: 2) обробка отриманих показників: застосування функції parse_input(input_str) для кожного виду показників
    lum_list = parse_input(lum_str)
    temp_list = parse_input(temp_str)
    cons_list = parse_input(cons_str)

    if not (lum_list and temp_list and cons_list):
        return
    
    ### TODO: 3) створення загального словника з показами: застосування функції create_data_dict(temp_list, hum_list, pres_list)
    data = create_data_dict(lum_list, temp_list, cons_list)

    ### TODO: 4) обробка показів температури, вологості та тиску повітря: обчислення статистичних характеристик та виведення результатів на екран (застосування функції process_measurements(title, data_dict, threshold) для кожного виду показників)
    process_measurements("Освітленість", data["luminosity"], 1000)
    process_measurements("Температура", data["temperature"], 5)
    process_measurements("Споживання", data["consumption"], 200)

if __name__ == "__main__":
    main()