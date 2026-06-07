from kanren import run, var, membero, lall, eq

# Допоміжна функція для визначення відношення "праворуч від" (a знаходиться праворуч від b)
def right_of(a, b, developers):
    return membero((a, b), list(zip(developers[1:], developers)))

# Створюємо змінні для трьох програмістів (кожен — це кортеж)
p1, p2, p3 = var(), var(), var()
developers = (p1, p2, p3)

# Описуємо правила
rules = lall(
    # Кожен програміст це кортеж: (Мова_програмування, Напій, Гаджет)
    (membero, (var(), var(), var()), developers),
    (membero, (var(), var(), var()), developers),
    (membero, (var(), var(), var()), developers),

    # 1. Програміст на Python п'є еспресо
    (membero, ('Python', 'Еспресо', var()), developers),

    # 2. Власник механічної клавіатури сидить праворуч від того, хто п'є лате
    (right_of, (var(), var(), 'Механічна клавіатура'), (var(), 'Лате', var()), developers),

    # 3. Той, хто пише на JS, використовує трекпад
    (membero, ('JS', var(), 'Трекпад'), developers),

    # Додаткові умови для визначення решти сутностей.
    # За умовою в офісі пишуть на Python, JS, С++
    (membero, ('C++', var(), var()), developers),

    # Нехай третій гаджет - Macbook
    (membero, (var(), var(), 'Macbook'), developers),
    
    # В задачі запитується, хто п'є Капучино? (Тобто капучино в офісі точно хтось п'є)
    (membero, (var(), 'Капучино', var()), developers)

    # Створення логічного протиріччя
    # Той, хто пише на JS, використовує механічну клавіатуру
    # (membero, ('JS', var(), 'Механічна клавіатура'), developers),

    # Порушення просторових обмежень
    # (right_of, ('Python', var(), var()), (var(), 'Капучино', var()), developers),
    # (right_of, ('JS', var(), var()), ('C++', var(), var()), developers)

    # Не залишається варіантів для Капучино
    # (right_of, (var(), 'Мак-кава', 'Механічна клавіатура'), (var(), 'Лате', var()), developers)
)

solutions = list(run(0, developers, rules))

if solutions:
    for s in solutions:
        for p in s:
            print(f"Мова програмування: {p[0]}, Напій: {p[1]}, Гаджет: {p[2]}")
        print();
else:
    print("Розв'язок не існує.")