from math import sqrt
from helping.print_tables import print_table_multivar
from helping.var9 import f2 as f, grad_f2 as grad, hess_f2 as hess, X0, X_MIN, A, B, C, D, E, F
from methods.lab3.fibonacci import fibonacci_method
from methods.lab3.golden_section import golden_section_method
from methods.lab3.dichotomy import dichotomy_method
from methods.lab4.newton import newton_method

# параметры запуска
EPS1, EPS2, M = 0.10, 0.15, 5
SVENN_T = 0.1  # шаг метода Свенна (нужен только на шаге 10б, если H^-1 не положительно определена)
VERBOSE = True
STEP_METHODS = {
    "Дихотомия": dict(func=dichotomy_method, l=0.0001, eps=0.00001),
    "Золотое сечение": dict(func=golden_section_method, l=0.0001),
    "Фибоначчи": dict(func=fibonacci_method, l=0.0001, eps=0.00001),
}

def run_method(name):
    params = {k: v for k, v in STEP_METHODS[name].items() if k != "func"}
    print(f"Метод Ньютона: f(x) = {A}*x1^2 + {B}*x2^2 + {C}*x1*x2 + {D}*x1 + {E}*x2 + {F}; x0 = {X0}; "
          f"eps1 = {EPS1}, eps2 = {EPS2}, M = {M}")
    print(f"Поиск шага (только при d = -grad f): Свенн (t = {SVENN_T}) + {name}, параметры: {params}\n")
    res = newton_method(f, grad, hess, X0, EPS1, EPS2, M,
                        step_method=STEP_METHODS[name],
                        svenn_t=SVENN_T, verbose=VERBOSE)

    if res.history:
        print_table_multivar(res.history)
    print(f"Найденная точка: x* = ({res.x[0]:.6f}; {res.x[1]:.6f}), f(x*) = {res.f_x:.6f}")
    if res.extra["reason"] == "step4":
        print("Причина остановки: выполнен критерий ||grad f|| <= eps1 (шаг 4)")
    elif res.extra["reason"] == "step5":
        print("Причина остановки: достигнуто предельное число итераций k >= M (шаг 5)")
    else:
        print("Причина остановки: оба условия шага 11 выполнены на двух итерациях подряд")
    print(f"Итераций: {res.n_iter}")
    print(f"Вычислений функции: {res.n_evals}")
    return res


if __name__ == "__main__":
    # для функции с положительно определённым гессианом линейный поиск не вызывается,
    # поэтому метод поиска шага не влияет на результат
    name = "Золотое сечение"
    res = run_method(name)
    f_min = f(*X_MIN)
    print(f"\nАналитический минимум: x_min = ({X_MIN[0]:.6f}; {X_MIN[1]:.6f}), f(x_min) = {f_min:.6f}")
    print(f"||x* - x_min|| = {sqrt((res.x[0] - X_MIN[0]) ** 2 + (res.x[1] - X_MIN[1]) ** 2):.2e}, "
          f"|f(x*) - f_min| = {abs(res.f_x - f_min):.2e}")
