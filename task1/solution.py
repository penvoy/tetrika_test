def strict(func):
    def wrapper(*args, **kwargs):
        # Получаем аннотации типов из функции
        annotations = func.__annotations__

        # Проверяем количество аргументов
        if len(args) + len(kwargs) != len(annotations)-1:
            raise TypeError("Некорректное число аргументов")

        # Создаем список всех аргументов, чтобы можно было их проверить
        all_args = list(args) + [kwargs[k] for k in annotations if k in kwargs]

        # Проверяем соответствие типов
        for arg_name, arg_value in zip(annotations.keys(), all_args):
            expected_type = annotations[arg_name]
            if type(arg_value) != expected_type:
                raise TypeError(f"Аргумент '{arg_name}' должен быть типа {expected_type.__name__}, а не {type(arg_value).__name__}")

        # Вызываем оригинальную функцию, если все типы корректны
        return func(*args, **kwargs)

    return wrapper

@strict
def sum_two(a: int, b: int) -> int:
    return a + b

