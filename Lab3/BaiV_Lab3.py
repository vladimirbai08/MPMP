import csv
import json
import os

# Реалізація класів Product, Customer та Store
class Product:
    def __init__(self, title, author, isbn, price, quantity):
        self._title = title
        self._author = author
        self._isbn = isbn
        self._price = price
        self._quantity = quantity

    @property
    def isbn(self):
        return self._isbn

    @property
    def quantity(self):
        return self._quantity

    @property
    def price(self):
        return self._price

    @property
    def title(self):
        return self._title

    def reduce_quantity(self, amount):
        self._quantity -= amount

    def increase_quantity(self, amount):
        self._quantity += amount

    def get_info(self):
        return (f"ISBN: {self._isbn} | "
                f"{self._title} - {self._author} | "
                f"Ціна: {self._price} грн | "
                f"Кількість: {self._quantity}")

    def __str__(self):
        return self.get_info()


class Customer:
    def __init__(self, name, customer_id):
        self._name = name
        self._customer_id = customer_id
        self._purchase_history = []

    @property
    def customer_id(self):
        return self._customer_id

    @property
    def purchase_history(self):
        return self._purchase_history

    def add_purchase(self, product_title):
        self._purchase_history.append(product_title)

    def get_info(self):
        history = ", ".join(self._purchase_history)

        if history == "":
            history = "Покупок немає"

        return (f"Клієнт: {self._name} "
                f"(ID: {self._customer_id}) | "
                f"Історія покупок: {history}")

    def __str__(self):
        return self.get_info()


class Store:
    def __init__(self):
        self._products = []
        self._customers = []

    def add_product(self, product):
        self._products.append(product)

    def find_product_by_isbn(self, isbn):
        for product in self._products:
            if product.isbn == isbn:
                return product
        return None

    def show_all_products(self):
        if len(self._products) == 0:
            print("Товарів немає.")
            return

        for product in self._products:
            print(product)

    def register_customer(self, customer):
        self._customers.append(customer)

    def find_customer_by_id(self, customer_id):
        for customer in self._customers:
            if customer.customer_id == customer_id:
                return customer
        return None

    def show_all_customers(self):
        if len(self._customers) == 0:
            print("Клієнтів немає.")
            return

        for customer in self._customers:
            print(customer)

    def buy_product(self, isbn, customer_id, amount):
        product = self.find_product_by_isbn(isbn)
        customer = self.find_customer_by_id(customer_id)

        # Перевірка наявності товару та клієнта
        if not product:
            print("Товар не знайдено.")
            return

        if not customer:
            print("Клієнта не знайдено.")
            return

        if product.quantity < amount:
            print("Недостатньо товару на складі.")
            return

        # Оформлення покупки
        product.reduce_quantity(amount)

        for _ in range(amount):
            customer.add_purchase(product.title)

        total_price = product.price * amount

        print("--------------------------")
        print("Покупку оформлено успішно.")
        print(f"Сума покупки: {total_price} грн")


    # ЗБЕРЕЖЕННЯ ТОВАРІВ У CSV
    def save_products_to_csv(self, filename):
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                "title",
                "author",
                "isbn",
                "price",
                "quantity"
            ])

            for product in self._products:
                writer.writerow([
                    product._title,
                    product._author,
                    product._isbn,
                    product._price,
                    product._quantity
                ])

        print("Товари збережено у CSV.")


    # ЗАВАНТАЖЕННЯ ТОВАРІВ З CSV
    def load_products_from_csv(self, filename):
        if not os.path.exists(filename):
            return

        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                product = Product(
                    row["title"],
                    row["author"],
                    row["isbn"],
                    float(row["price"]),
                    int(row["quantity"])
                )

                self.add_product(product)


    # Збереження клієнтів у JSON
    def save_customers_to_json(self, filename):
        customers_data = []

        for customer in self._customers:
            customers_data.append({
                "name": customer._name,
                "customer_id": customer._customer_id,
                "purchase_history": customer.purchase_history
            })

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(customers_data, file,
                      ensure_ascii=False,
                      indent=4)

        print("Клієнтів збережено у JSON.")

    # Завантаження клієнтів з JSON
    def load_customers_from_json(self, filename):
        if not os.path.exists(filename):
            return

        with open(filename, "r", encoding="utf-8") as file:
            customers_data = json.load(file)

            for item in customers_data:
                customer = Customer(
                    item["name"],
                    item["customer_id"]
                )

                customer._purchase_history = item["purchase_history"]

                self.register_customer(customer)


# Реалізація основної програми (меню задач)

menu = """
1. Додати товар
2. Зареєструвати клієнта
3. Купити книгу
4. Показати всі товари
5. Показати всіх клієнтів
6. Зберегти дані
7. Вийти
"""

def main():
    store = Store()

    # Завантаження даних
    store.load_products_from_csv("products.csv")
    store.load_customers_from_json("customers.json")

    while True:
        print(menu)
        choice = input("Оберіть пункт меню: ")

        if choice == "1":
            print("\n[ДОДАВАННЯ ТОВАРУ]")
            title = input("Назва книги: ")
            author = input("Автор: ")
            isbn = input("ISBN: ")
            price = float(input("Ціна: "))
            quantity = int(input("Кількість: "))
            product = Product(title, author, isbn, price, quantity)
            store.add_product(product)
            print("Товар додано.")

        elif choice == "2":
            print("\n[РЕЄСТРАЦІЯ КЛІЄНТА]")
            name = input("Ім'я: ")
            customer_id = input("ID клієнта: ")
            customer = Customer(name, customer_id)
            store.register_customer(customer)
            print("Клієнта зареєстровано.")

        elif choice == "3":
            print("\n[ПОКУПКА КНИГИ]")

            isbn = input("ISBN книги: ")
            customer_id = input("ID клієнта: ")
            amount = int(input("Кількість: "))

            store.buy_product(isbn, customer_id, amount)

        elif choice == "4":
            print("\n[СПИСОК ТОВАРІВ]")
            store.show_all_products()

        elif choice == "5":
            print("\n[СПИСОК КЛІЄНТІВ]")
            store.show_all_customers()

        elif choice == "6":
            store.save_products_to_csv("products.csv")
            store.save_customers_to_json("customers.json")

        elif choice == "7":

            # Автозбереження перед виходом
            store.save_products_to_csv("products.csv")
            store.save_customers_to_json("customers.json")

            print("Завершення роботи.")
            break

        else:
            print("Невірний вибір.")


if __name__ == "__main__":
    main()