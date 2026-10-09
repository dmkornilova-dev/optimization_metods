from helping.var9 import f1 as f
from methods.lab3.fibonacci import fibonacci_method
from methods.lab3.golden_section import golden_section_method
from methods.lab3.dichotomy import dichotomy_method
from helping.print_tables import print_summary_table

# параметры запуска
A0, B0 = -4, 6  # начальный отрезок
VERBOSE = False
METHODS = {
    "Дихотомия": dict(func=dichotomy_method, l=0.01, eps=0.005),
    "Золотое сечение": dict(func=golden_section_method, l=1),
    "Фибоначчи": dict(func=fibonacci_method, l=1, eps=0.05),
}


def run_method(name, params):
    params = dict(params)
    method = params.pop("func")

    print(f"{name}: f(x) = x^2 + 4x + 6; [{A0}; {B0}]; параметры: {params}")
    res = method(f, A0, B0, verbose=VERBOSE, **params)

    print_summary_table(res.history)
    print(f"Найденный отрезок: [{res.a:.6f}; {res.b:.6f}]")
    print(f"Найденный минимум: x* = {res.x:.6f}, f(x*) = {f(res.x):.6f}")
    print(f"Длина интервала: {res.delta:.12f}")
    print(f"Вычислений функции: {res.n_evals}")


    if "R" in res.extra:
        print(f"Требуемое (ожидаемое) отношение итогового отрезка к начальному: "
              f"R(N) = {res.extra['R']:.12f}")
    if "R_fact" in res.extra:
        print(f"Фактическое отношение итогового отрезка к начальному: "
              f"R_fact = {res.extra['R_fact']:.12f}")
    if "R_ok" in res.extra:
        word = "не более" if res.extra["R_ok"] else "БОЛЬШЕ"
        print(f"Разница между предполагаемой и фактической длиной отрезка {word} eps")
    print("\n")
    return res


if __name__ == "__main__":
    results = {name: run_method(name, params) for name, params in METHODS.items()}
    print("Сравнение методов")
    print(f"{'Метод':<18} | {'x*':>10} | {'f(x*)':>10} | {'Длина':>10} | {'Вычислений':>10}")
    for name, res in results.items():
        print(f"{name:<18} | {res.x:>10.6f} | {f(res.x):>10.6f} | "
              f"{res.delta:>10.6f} | {res.n_evals:>10}")
