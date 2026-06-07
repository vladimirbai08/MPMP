from kanren import run, var, membero, lall

def right_of(a, b, developers):
    return membero((a, b), list(zip(developers[1:], developers)))

p1, p2, p3, p4, p5 = var(), var(), var(), var(), var()
developers = (p1, p2, p3, p4, p5)

rules = lall(
    # 1. Француз пише на C++ і має кота
    membero(('C++', var(), var(), 'француз', 'кіт'), developers),

    # 2. У італійця домашній улюбленець - собака
    membero((var(), var(), var(), 'італієць', 'собака'), developers),

    # 3. Італієць сидить праворуч від українця
    right_of((var(), var(), var(), 'італієць', var()), 
             (var(), var(), var(), 'українець', var()), developers),

    # 4. Британка сидить праворуч від італійця
    right_of((var(), var(), var(), 'британка', var()), 
             (var(), var(), var(), 'італієць', var()), developers),

    # 5. Британка пише на SQL
    membero(('SQL', var(), var(), 'британка', var()), developers),

    # 6. Програміст на Python п'є еспресо
    membero(('Python', 'еспресо', var(), var(), var()), developers),

    # 7. Той, хто пише на JS, використовує трекпад
    membero(('JS', var(), 'трекпад', var(), var()), developers),

    # 8. Власник механічної клавіатури сидить праворуч від того, хто п'є лате
    right_of((var(), var(), 'Механічна клавіатура', var(), var()), 
             (var(), 'лате', var(), var(), var()), developers),

    # 9. У того, хто п'є мак-каву, є папуга
    membero((var(), 'мак-кава', var(), var(), 'папуга'), developers),

    # 10. У того, хто пише на C#, є рибки
    membero(('C#', var(), var(), var(), 'рибки'), developers),

    # Задамо інші умови
    membero((var(), 'кола', var(), var(), var()), developers),
    membero((var(), var(), 'Macbook', var(), var()), developers),
    membero((var(), var(), var(), 'норвежець', var()), developers),
    # membero((var(), var(), var(), 'японець', var()), developers),

    # Хто п'є капучино?
    membero((var(), 'капучино', var(), var(), var()), developers)
)

solutions = list(run(3, developers, rules)) # будемо виводити лише перші 3 розв'язки

if solutions:
    for s in solutions:
        for p in s:
            print(f"Мова програмування: {p[0]}, Напій: {p[1]}, Гаджет: {p[2]}, Національність: {p[3]}, Тварина: {p[4]}")
        print();
else:
    print("Розв'язок не існує.")
