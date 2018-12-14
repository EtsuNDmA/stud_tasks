# -*- coding: utf-8 -*-


def task_5(accounts):
    help_msg = """
        Формат команд:
            <operation> <name> <num>
            <operation> <name> <name> <num>

            1 <name> <num> – пополнение счета клиента
            2 <name> <num> – снятие денег со счета
            3 <name> – запрос остатка средств на счете
            4 <name_from> <name_to> <num> – перевод денег между счетами клиентов
            5 <num> – начисление процентов всем клиентам
            6 – завершение работы с программой
        <name> - имя аккаунта
        <num> - целое число
        """
    print(help_msg)

    def top_up(name, num):
        num = int(num)
        accounts[name] = accounts.get(name, 0) + num

    def withdraw(name, num):
        num = int(num)
        accounts[name] = accounts.get(name, 0) - num

    def get_balance(name):
        print(accounts.get(name, 0))

    def transfer(name_from, name_to, num):
        num = int(num)
        accounts[name_from] = accounts.get(name_from, 0) - num
        accounts[name_to] = accounts.get(name_to, 0) + num

    def interest(percent):
        percent = int(percent)
        for name, value in accounts.items():
            if value > 0:
                accounts[name] = int(value * (1 + percent/100))

    def exit(*args):
        for name, value in accounts.items():
            print(name, ': ', value)

    commands = {
        1: top_up,
        2: withdraw,
        3: get_balance,
        4: transfer,
        5: interest,
        6: exit,
    }

    operation = 0
    while operation != 6:
        command = input('=> ').split()
        operation = int(command[0])
        try:
            commands[operation](*command[1:])
        except:
            print("Error in command")


if __name__ == '__main__':
    print("=" * 20, "task 5", "=" * 20)
    accounts = {}
    task_5(accounts)