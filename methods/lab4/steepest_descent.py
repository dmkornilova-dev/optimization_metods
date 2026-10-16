from math import sqrt
from helping.log import make_logger
from helping.types import MultivarResult
from helping.line_search import line_search


def steepest_descent_method(f, grad, x0, eps1, eps2, M, step_method, svenn_t, verbose=False):
    if eps1 <= 0 or eps2 <= 0:
        raise ValueError("eps1 и eps2 должны быть положительными числами")
    if M <= 0:
        raise ValueError("M должно быть положительным числом")
    if svenn_t <= 0:
        raise ValueError("Шаг метода Свенна должен быть положительным числом")

    log = make_logger(verbose)

    # шаг 1
    x = list(x0)
    log("Метод наискорейшего спуска - подробное решение\n")
    log("Шаг 1. Задаём:")
    log(f"x0 = {x}")
    log(f"eps1 = {eps1}")
    log(f"eps2 = {eps2}")
    log(f"M = {M}")

    # шаг 2
    k = 0
    log("\nШаг 2. Положим k = 0.")

    fx = f(*x) # для критерия 2 в шаге 8
    n_evals = 1  # f(x0)
    prev_ok = False  # выполнены ли оба условия шага 8 на предыдущей итерации
    history = []

    while True:
        # шаг 3
        g = grad(*x) # частные производные при данном x=(x1;x2)
        log(f"\nШаг 3 (итерация k = {k}). x{k} = {x}, f(x{k}) = {fx:.6f}")
        log(f"grad f(x{k}) = {g}")

        # шаг 4
        norm_g = sqrt(sum(gi ** 2 for gi in g))
        log(f"\nШаг 4. ||grad f(x{k})|| = {norm_g:.6f}")
        if norm_g < eps1:
            reason = "step4"
            log(f"{norm_g:.6f} < eps1 = {eps1} - алгоритм завершён, x* = x{k}.")
            break
        log(f"{norm_g:.6f} >= eps1 = {eps1} - переходим к шагу 5.")

        # шаг 5
        if k >= M:
            reason = "step5"
            log(f"\nШаг 5. k = {k} >= M = {M} - алгоритм завершён, x* = x{k}.")
            break
        log(f"\nШаг 5. k = {k} < M = {M} - переходим к шагу 6.")

        # шаг 6 - phi(t) = f(x_k - t * grad f(x_k)) -> min
        def phi(t, x=x, g=g):
            return f(*[xi - t * gi for xi, gi in zip(x, g)])  # phi(tk) = f(xk-tk*grad(xk)) - ищем точку минимума phi
        t, n_line = line_search(phi, step_method, svenn_t, verbose=verbose)
        log(f"\nШаг 6. t{k}* = {t:.6f} (вычислений функции при поиске шага: {n_line})")

        # шаг 7 - вычисление координат новой точки и значения функции в ней
        x_new = [xi - t * gi for xi, gi in zip(x, g)]
        f_new = f(*x_new)
        n_evals += n_line + 1 # ОБЩЕЕ количество вычислений функции
        log(f"\nШаг 7. x{k + 1} = x{k} - t{k}* * grad f(x{k}) = {x_new}")
        log(f"f(x{k + 1}) = {f_new:.6f}")

        # шаг 8 - проверка двух критериев
        norm_x = sqrt(sum((a - b) ** 2 for a, b in zip(x_new, x)))
        mod_fx = abs(f_new - fx)
        ok = norm_x < eps2 and mod_fx < eps2
        log(f"\nШаг 8. ||x{k + 1} - x{k}|| = {norm_x:.6f}, |f(x{k + 1}) - f(x{k})| = {mod_fx:.6f}")

        history.append({
            "k": k,
            "x_k": x,
            "f_xk": fx,
            "grad_norm": norm_g,
            "t_k": t,
            "x_k1": x_new,
            "f_xk1": f_new,
            "norm_x": norm_x,
            "mod_fx": mod_fx,
            "ok": ok,
        })

        x, fx = x_new, f_new

        if ok and prev_ok:
            reason = "step8"
            log(f"Оба условия выполнены при k = {k} и k = {k - 1} - алгоритм завершён, "
                f"x* = x{k + 1}.")
            break
        if ok:
            log(f"Оба условия выполнены при k = {k}, но не при k = {k - 1} - "
                f"полагаем k = {k + 1} и переходим к шагу 3.")
        else:
            log(f"Хотя бы одно условие не выполнено - полагаем k = {k + 1} "
                f"и переходим к шагу 3.")
        prev_ok = ok
        k += 1

    log(f"\nx* = {x}, f(x*) = {fx:.6f}")

    return MultivarResult(
        x=x, f_x=fx,
        n_iter=len(history),
        n_evals=n_evals,
        history=history,
        extra={"reason": reason},
    )
