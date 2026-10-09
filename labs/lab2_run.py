from helping.var9 import f1 as f
from methods.lab2.svenn import svenn_method
from helping.types import NotUnimodalError

# параметры запуска
X0, T = 1, 1
X0_VALUES = [round(-12 + 1.0 * i, 2) for i in range(21)]      # от -12 до 8 с шагом 1
T_VALUES = [round(0.2 + 0.2 * i, 2) for i in range(10)]  # от 0.2 до 2.0 с шагом 0.2
COL_WIDTH = 30


def run_step_by_step():
    print("Метод Свенна для f(x) = x^2 + 4x + 6. Пошаговая иллюстрация")
    res = svenn_method(f, X0, T, verbose=True)
    print(f"Итог: [{res.a}, {res.b}], вычислений функции: {res.n_evals}")


def create_table():
    results = {}
    for x0 in X0_VALUES:
        for t in T_VALUES:
            try:
                results[(x0, t)] = svenn_method(f, x0, t, verbose=False)
            except NotUnimodalError:
                results[(x0, t)] = None
    return results


def print_table(results):
    print("\nСводная таблица результатов: строки - x0, столбцы - t")
    print("Ячейка: [a, b] L = длина отрезка, n = число вычислений функции")
    print(f"{'x0 \\ t':>8}", end="")
    for t in T_VALUES:
        print(f"{t:>{COL_WIDTH}}", end="")
    print()
    print("-" * (8 + COL_WIDTH * len(T_VALUES)))

    for x0 in X0_VALUES:
        print(f"{x0:>8}", end="")
        for t in T_VALUES:
            r = results[(x0, t)]
            if r is None:
                cell = "не унимодальна"
            else:
                cell = f"[{r.a:.2f}, {r.b:.2f}] L={r.delta:.2f} n={r.n_evals}"
            print(f"{cell:>{COL_WIDTH}}", end="")
        print()


if __name__ == "__main__":
    run_step_by_step()
    print_table(create_table())
