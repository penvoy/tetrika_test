from solution import sum_two

def test_strict_decorator():
    assert sum_two(0, 0) == 0  # Корректные типы

    try:
        kwargs = {"a": 1, "b": True}
        sum_two(**kwargs) == 3  # Корректные типы
    except TypeError as e:
        assert str(e) == "Аргумент 'b' должен быть типа int, а не bool"

    try:
        sum_two(1, 2.4)  # Неправильный тип: float вместо int
    except TypeError as e:
        assert str(e) == "Аргумент 'b' должен быть типа int, а не float"

    try:
        sum_two("1", 2)  # Неправильный тип: str вместо int
    except TypeError as e:
        assert str(e) == "Аргумент 'a' должен быть типа int, а не str"

    try:
        sum_two(1, 2, 3)  # Слишком много аргументов
    except TypeError as e:
        assert str(e) == "Некорректное число аргументов"

    print("Все тесты пройдены!")

# Запустим тесты
test_strict_decorator()