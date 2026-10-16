from dataclasses import dataclass, field


@dataclass
class IntervalResult:
    a: float #левый край отрезка
    b: float #правый край отрезка
    x: float #найденный приближенный x_res
    n_evals: int #количество вычислений функции
    history: list = field(default_factory=list) #для таблицы: не обязательна в методе Свенна
    extra: dict = field(default_factory=dict) #уникальные для метода значения

    @property
    def delta(self): #длина отрезка
        return self.b - self.a


class NotUnimodalError(ValueError):
    pass

@dataclass
class MultivarResult:
    x: list #найденная точка x*
    f_x: float #значение функции в x*
    n_iter: int #количество выполненных итераций
    n_evals: int #количество вычислений функции (включая поиск шага)
    history: list = field(default_factory=list) #для таблицы
    extra: dict = field(default_factory=dict) #уникальные для метода значения
