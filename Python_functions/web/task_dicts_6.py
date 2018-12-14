# -*- coding: utf-8 -*-


def task_6():
    help_msg = """
        Введите данные в виде: Покупатель Товар Количество
        Для выхода введите пустую строку
        """
    print(help_msg)

    data = []
    while True:
        try:
            string = input('=> ')
            if string == '':
                break
            str_data = string.split()
            str_data[2] = int(str_data[2])
            data.append(str_data)
        except:
            print("Ошибка ввода")
    print("Товары:", ', '.join({item[1] for item in data}))
    print("Покупатели:", ', '.join({item[0] for item in data}))

    purchases = {}
    for name, product, num in data:
        products = purchases.get(name, {})
        products[product] = products.get(product, 0) + int(num)
        purchases[name] = products
    print("Товары покупателей:", purchases)


if __name__ == '__main__':
    print("=" * 20, "task 6", "=" * 20)
    task_6()
