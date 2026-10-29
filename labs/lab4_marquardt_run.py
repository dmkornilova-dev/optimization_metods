from math import sqrt
from helping.print_tables import print_table_multivar
from helping.var9 import f2 as f, grad_f2 as grad, hess_f2 as hess, X0, X_MIN, A, B, C, D, E, F
from methods.lab4.marquardt import marquardt_method

# параметры запуска
EPS1, M = 0.0001, 1000000
# mu0 - минимум на порядок больше наибольшего элемента H(x0) = [[14, -1], [-1, 2]]
MU0 = 140
VERBOSE = False


def run_method():
    print(f"Метод Марквардта: f(x) = {A}*x1^2 + {B}*x2^2 + {C}*x1*x2 + {D}*x1 + {E}*x2 + {F}; x0 = {X0}; "
          f"eps1 = {EPS1}, M = {M}, mu0 = {MU0}\n")
    res = marquardt_method(f, grad, hess, X0, EPS1, M, MU0, verbose=VERBOSE)

    if res.history:
        print_table_multivar(res.history)
    print(f"Найденная точка: x* = ({res.x[0]:.8f}; {res.x[1]:.8f}), f(x*) = {res.f_x:.8f}")
    if res.extra["reason"] == "step4":
        print("Причина остановки: выполнен критерий ||grad f|| <= eps1 (шаг 4)")
    else:
        print("Причина остановки: достигнуто предельное число итераций k >= M (шаг 5)")
    print(f"Итераций: {res.n_iter}")
    print(f"Вычислений функции: {res.n_evals}")
    return res

if __name__ == "__main__":
    res = run_method()
    f_min = f(*X_MIN)
    print(f"\nАналитический минимум: x_min = ({X_MIN[0]:.8f}; {X_MIN[1]:.8f}), f(x_min) = {f_min:.8f}")
    print(f"||x* - x_min|| = {sqrt((res.x[0] - X_MIN[0]) ** 2 + (res.x[1] - X_MIN[1]) ** 2):.2e}, "
          f"|f(x*) - f_min| = {abs(res.f_x - f_min):.2e}")
