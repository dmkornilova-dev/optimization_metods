from math import sqrt
from helping.log import make_logger
from helping.types import MultivarResult
from helping.line_search import line_search


def newton_method(f, grad, hess, x0, eps1, eps2, M, step_method, svenn_t, verbose=False):
    if eps1 <= 0 or eps2 <= 0:
        raise ValueError("eps1 и eps2 должны быть положительными числами")
    if M <= 0:
        raise ValueError("M должно быть положительным числом")
    if svenn_t <= 0:
        raise ValueError("Шаг метода Свенна должен быть положительным числом")
    if len(x0) != 2:
        raise ValueError("Реализация рассчитана на функцию двух переменных")

    log = make_logger(verbose)

    # шаг 1
    x = list(x0)
    log("Метод Ньютона - подробное решение\n")
    log("Шаг 1. Задаём:")
    log(f"x0 = {x}")
    log(f"eps1 = {eps1}")
    log(f"eps2 = {eps2}")
    log(f"M = {M}")

    # шаг 2
    k = 0
    log("\nШаг 2. Положим k = 0.")

    fx = f(*x)  # для критерия 2 в шаге 11
    n_evals = 1  # f(x0)
    prev_ok = False  # выполнены ли оба условия шага 11 на предыдущей итерации
    history = []

    while True:
        # шаг 3
        g = grad(*x) # частные производные при данном x=(x1;x2)
        log(f"\nШаг 3 (итерация k = {k}). x{k} = {x}, f(x{k}) = {fx:.6f}")
        log(f"grad f(x{k}) = {g}")

        # шаг 4
        norm_g = sqrt(sum(gi ** 2 for gi in g))
        log(f"\nШаг 4. ||grad f(x{k})|| = {norm_g:.6f}")
        if norm_g <= eps1:
            reason = "step4"
            log(f"{norm_g:.6f} <= eps1 = {eps1} - алгоритм завершён, x* = x{k}.")
            break
        log(f"{norm_g:.6f} > eps1 = {eps1} - переходим к шагу 5.")

        # шаг 5
        if k >= M:
            reason = "step5"
            log(f"\nШаг 5. k = {k} >= M = {M} - алгоритм завершён, x* = x{k}.")
            break
        log(f"\nШаг 5. k = {k} < M = {M} - переходим к шагу 6.")

        # шаг 6 - матрица Гессе
        (h11, h12), (h21, h22) = hess(*x)
        log(f"\nШаг 6. H(x{k}) = [[{h11}, {h12}], [{h21}, {h22}]]")

        # шаг 7 - обратная матрица H^-1 = 1/|H| * (H*)^T
        det = h11 * h22 - h12 * h21
        log(f"\nШаг 7. |H| = {h11}*{h22} - ({h12})*({h21}) = {det}")
        if det != 0:
            H_inv = [[h22 / det, -h12 / det],
                     [-h21 / det, h11 / det]]
            log(f"H^-1(x{k}) = 1/{det} * [[{h22}, {-h12}], [{-h21}, {h11}]] = {H_inv}")
        else:
            H_inv = None
            log("|H| = 0 - обратной матрицы не существует.")

        # шаг 8 - H^-1 > 0 (критерий Сильвестра для симметричной матрицы 2x2)
        if H_inv is not None:
            i11, i12 = H_inv[0]
            i21, i22 = H_inv[1]
            det_inv = i11 * i22 - i12 * i21
            positive = i11 > 0 and det_inv > 0
            log(f"\nШаг 8. Проверяем H^-1(x{k}) > 0: h11 = {i11:.6f}, |H^-1| = {det_inv:.6f}")
        else:
            positive = False
            log(f"\nШаг 8. H^-1(x{k}) не существует, условие H^-1 > 0 не выполнено.")

        if positive: # случай а шага 8
            # шаг 9
            log(f"H^-1(x{k}) > 0 - переходим к шагу 9.")
            d = [-(i11 * g[0] + i12 * g[1]),
                 -(i21 * g[0] + i22 * g[1])]
            log(f"\nШаг 9. d{k} = -H^-1(x{k}) * grad f(x{k}) = {d}")

            # шаг 10а: t_k = 1
            t = 1.0
            n_line = 0
            direction = "Ньютон"
            log(f"\nШаг 10. Направление Ньютона, поэтому t{k} = 1.")
        else: # случай б шага 8
            # шаг 8б -> шаг 10б: d_k = -grad f, шаг t_k подбираем
            d = [-gi for gi in g]
            direction = "градиент"
            log(f"H^-1(x{k}) > 0 не выполнено - переходим к шагу 10, d{k} = -grad f(x{k}) = {d}")

            def phi(t, x=x, d=d):
                return f(*[xi + t * di for xi, di in zip(x, d)]) # phi(tk) = f(xk-tk*grad(xk)) - ищем точку минимума phi
            t, n_line = line_search(phi, step_method, svenn_t, verbose=verbose)
            log(f"\nШаг 10. t{k} = {t:.6f} (вычислений функции при поиске шага: {n_line})")

        # шаг 10 - новая точка
        x_new = [xi + t * di for xi, di in zip(x, d)]
        f_new = f(*x_new)
        n_evals += n_line + 1  # ОБЩЕЕ количество вычислений функции
        log(f"x{k + 1} = x{k} + t{k} * d{k} = {x_new}")
        log(f"f(x{k + 1}) = {f_new:.6f}")

        # шаг 11 - проверка двух критериев
        norm_x = sqrt(sum((a - b) ** 2 for a, b in zip(x_new, x)))
        mod_fx = abs(f_new - fx)
        ok = norm_x < eps2 and mod_fx < eps2
        log(f"\nШаг 11. ||x{k + 1} - x{k}|| = {norm_x:.6f}, |f(x{k + 1}) - f(x{k})| = {mod_fx:.6f}")

        history.append({
            "k": k,
            "x_k": x,
            "f_xk": fx,
            "grad_norm": norm_g,
            "direction": direction,
            "t_k": t,
            "x_k1": x_new,
            "norm_x": norm_x,
            "mod_fx": mod_fx,
            "ok": ok,
        })

        x, fx = x_new, f_new

        if ok and prev_ok:
            reason = "step11"
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
